#!/usr/bin/env python3
"""Turn a saved Framer page into a single self-contained file in site/.

WHY THIS EXISTS
    This session cannot reach Framer. The environment's egress proxy runs an
    allowlist (github.com and the package registries are on it; framer.com,
    framer.app, framer.website and framerusercontent.com are not), and the
    proxy README forbids routing around a policy denial. So the bytes have to
    arrive from a person. This script is what turns those bytes into a repo
    artefact without hand-editing 2 MB of generated markup.

GETTING THE BYTES OUT OF FRAMER (either works)
    a. Framer editor, desktop: project menu -> Export -> download the ZIP.
    b. Any browser, on the published URL: Save Page As -> "Web Page, Complete".
       You get an .html plus a folder of assets next to it. Keep them together.

USAGE
    python3 tools/import_framer.py <input> -o site/linenlegends-site.html \
        [--rename "Laundry Hub=Linen Legends"] [--rename "old=new"] \
        [--max-inline-kb 400] [--keep-badge] [--dry-run]

    <input> may be a .zip, a directory, or a single .html file.

WHAT IT DOES
    1. Inlines local stylesheets, scripts, fonts and images so the result is
       one file that can be committed and published like the main artefact.
    2. Strips the Framer badge ("Made in Framer") and the FramerGeeks template
       promo layer (the "50% OFF FLASH SALE", "Get Figma & Framer",
       "Access All Template", "Template by FramerGeeks" stack).
    3. Applies brand renames.
    4. Reports every asset it could not inline, every remote host the page
       still depends on, and every compliance sentinel that is missing.

WHAT IT DOES NOT DO
    It does not invent content and it does not fetch anything over the
    network. Remote assets stay remote and are listed in the report so the
    decision to vendor them is yours.
"""
import argparse
import base64
import html
import mimetypes
import os
import re
import shutil
import sys
import tempfile
import zipfile
from urllib.parse import unquote, urlparse

# Assets larger than the cap stay as-is; base64 costs ~33% on top of the file.
DEFAULT_MAX_INLINE_KB = 400

# Compliance sentinels the AU site must carry. Sourced from verify/preflight.py.
COMPLIANCE_SENTINELS = ["NDIS", "AS/NZS 4146", "ABN", "GST", "Australian Consumer Law"]

# Template furniture that must not ship on a real business site.
PROMO_PATTERNS = [
    r"50%\s*OFF\s*FLASH\s*SALE",
    r"Get\s+Figma\s*&(?:amp;)?\s*Framer",
    r"Access\s+All\s+Template",
    r"Template\s+by\s+FramerGeeks",
    r"FramerGeeks",
]

MIME_FALLBACK = {
    ".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf",
    ".otf": "font/otf", ".svg": "image/svg+xml", ".webp": "image/webp",
    ".avif": "image/avif", ".mjs": "text/javascript", ".js": "text/javascript",
    ".css": "text/css",
}


def guess_mime(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in MIME_FALLBACK:
        return MIME_FALLBACK[ext]
    return mimetypes.guess_type(path)[0] or "application/octet-stream"


def is_remote(url):
    return bool(urlparse(url).scheme) or url.startswith("//")


VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
             "meta", "param", "source", "track", "wbr"}


def _close_of(doc, open_end, tag):
    """Index just past </tag> for the element whose open tag ends at open_end."""
    depth, pos, low = 1, open_end, tag.lower()
    pat = re.compile(r"<(/?)(%s)\b" % re.escape(low), re.I)
    while depth:
        m = pat.search(doc, pos)
        if not m:
            return None
        if m.group(1):
            depth -= 1
            if not depth:
                gt = doc.find(">", m.end())
                return gt + 1 if gt != -1 else None
        else:
            gt = doc.find(">", m.end())
            if gt == -1:
                return None
            if doc[gt - 1] != "/":
                depth += 1
        pos = m.end()
    return None


def enclosing_element(doc, i, j, limit=0.4):
    """Smallest element fully containing doc[i:j], as (start, end).

    Returns None rather than a span larger than `limit` of the document, so a
    stray match can never take the page with it.
    """
    pos = i
    while True:
        lt = doc.rfind("<", 0, pos)
        if lt == -1:
            return None
        pos = lt
        m = re.match(r"<([a-zA-Z][\w:-]*)", doc[lt:lt + 48])
        if not m:
            continue
        tag = m.group(1).lower()
        if tag in VOID_TAGS or tag in ("html", "body", "script", "style"):
            continue
        gt = doc.find(">", lt)
        if gt == -1 or doc[gt - 1] == "/":
            continue
        end = _close_of(doc, gt + 1, tag)
        if end is not None and end >= j and lt <= i:
            if (end - lt) > limit * len(doc):
                return None
            return (lt, end)


class Importer:
    def __init__(self, root, html_path, max_inline, keep_badge):
        self.root = root
        self.html_path = html_path
        self.base = os.path.dirname(html_path)
        self.max_inline = max_inline * 1024
        self.keep_badge = keep_badge
        self.inlined = []
        self.too_big = []
        self.missing = []
        self.remote_hosts = {}
        self.removed = []
        self.dropped_srcset = 0

    # -- asset resolution -------------------------------------------------
    def resolve(self, url, base=None):
        """Map a URL from the saved page onto a file on disk, or None.

        `base` is the directory the URL is relative to. For a URL found inside
        a stylesheet that is the stylesheet's own directory, not the page's --
        getting this wrong is why nested @import and url() targets go missing.
        """
        if not url or url.startswith(("data:", "#", "blob:", "javascript:", "mailto:", "tel:")):
            return None
        if is_remote(url):
            host = urlparse("https:" + url if url.startswith("//") else url).netloc
            self.remote_hosts[host] = self.remote_hosts.get(host, 0) + 1
            return None
        clean = unquote(url.split("?")[0].split("#")[0])
        if not clean:
            return None
        for cand in (os.path.join(base or self.base, clean),
                     os.path.join(self.base, clean),
                     os.path.join(self.root, clean.lstrip("/"))):
            cand = os.path.normpath(cand)
            if os.path.isfile(cand):
                return cand
        self.missing.append(url)
        return None

    def read_asset(self, url, base=None):
        path = self.resolve(url, base)
        if not path:
            return None
        size = os.path.getsize(path)
        if size > self.max_inline:
            self.too_big.append((url, round(size / 1024)))
            return None
        with open(path, "rb") as fh:
            return path, fh.read()

    def data_uri(self, url, base=None):
        got = self.read_asset(url, base)
        if not got:
            return None
        path, blob = got
        self.note_inlined(path, blob)
        return "data:%s;base64,%s" % (guess_mime(path), base64.b64encode(blob).decode())

    def note_inlined(self, path, blob):
        """Record an inlined asset once, counting repeat references."""
        key = os.path.basename(path)
        for i, (name, kb, n) in enumerate(self.inlined):
            if name == key:
                self.inlined[i] = (name, kb, n + 1)
                return
        self.inlined.append((key, round(len(blob) / 1024), 1))

    # -- CSS --------------------------------------------------------------
    def inline_css_urls(self, css, base=None, depth=0):
        if depth > 4:
            return css
        base = base or self.base

        def imp(m):
            got = self.read_asset(m.group(2), base)
            if not got:
                return m.group(0)
            self.note_inlined(got[0], got[1])
            return self.inline_css_urls(got[1].decode("utf-8", "replace"),
                                        os.path.dirname(got[0]), depth + 1)

        # @import first, so urls inside the imported sheet resolve against it.
        css = re.sub(r"@import\s+(?:url\()?(['\"])(.*?)\1\)?\s*;", imp, css)

        def sub(m):
            uri = self.data_uri(m.group(2).strip(), base)
            return "url(%s)" % uri if uri else m.group(0)

        return re.sub(r"url\((['\"]?)(.*?)\1\)", sub, css)

    # -- HTML -------------------------------------------------------------
    def run(self, doc):
        doc = self.inline_stylesheets(doc)
        doc = self.inline_scripts(doc)
        doc = self.inline_media(doc)
        doc = self.inline_style_attrs(doc)
        if not self.keep_badge:
            doc = self.strip_furniture(doc)
        return doc

    def inline_stylesheets(self, doc):
        def sub(m):
            tag = m.group(0)
            if "stylesheet" not in tag:
                return tag
            href = re.search(r'href=(["\'])(.*?)\1', tag)
            if not href:
                return tag
            got = self.read_asset(href.group(2))
            if not got:
                return tag
            self.note_inlined(got[0], got[1])
            css = self.inline_css_urls(got[1].decode("utf-8", "replace"), os.path.dirname(got[0]))
            return "<style>\n%s\n</style>" % css
        return re.sub(r"<link\b[^>]*>", sub, doc, flags=re.I)

    def inline_scripts(self, doc):
        def sub(m):
            tag = m.group(1)
            src = re.search(r'src=(["\'])(.*?)\1', tag)
            if not src:
                return m.group(0)
            got = self.read_asset(src.group(2))
            if not got:
                return m.group(0)
            js = got[1].decode("utf-8", "replace")
            if "</script" in js.lower():
                js = re.sub(r"</(script)", r"<\\/\1", js, flags=re.I)
            self.note_inlined(got[0], got[1])
            keep = re.sub(r'\s+src=(["\']).*?\1', "", tag)
            return "%s\n%s\n</script>" % (keep, js)
        return re.sub(r"(<script\b[^>]*>)\s*</script>", sub, doc, flags=re.I)

    def inline_media(self, doc):
        def sub(m):
            tag, attr, q, url = m.group(0), m.group(1), m.group(2), m.group(3)
            if attr.lower() == "srcset":
                # A data URI contains commas, and so does srcset's own syntax,
                # so an inlined srcset is ambiguous and browsers mis-parse it.
                # Drop the attribute instead; src carries the inlined image.
                if any(c.strip().startswith("data:") for c in url.split()):
                    return ""
                first = url.split(",")[0].strip().split(None, 1)
                if first and self.resolve(first[0]):
                    self.dropped_srcset += 1
                    return ""
                return tag
            uri = self.data_uri(url)
            return tag.replace("%s%s%s" % (q, url, q), "%s%s%s" % (q, uri, q)) if uri else tag
        doc = re.sub(r'\bsrcset=(["\'])([^"\']*)\1',
                     lambda m: sub(re.match(r'\b(srcset)=(["\'])([^"\']*)\2',
                                            m.group(0).lstrip())) or "", doc)
        return re.sub(r'\b(src|poster|href)=(["\'])([^"\']+)\2',
                      lambda m: sub(m) if not m.group(3).startswith("#") else m.group(0), doc)

    def inline_style_attrs(self, doc):
        return re.sub(r'style=(["\'])(.*?)\1',
                      lambda m: 'style=%s%s%s' % (m.group(1), self.inline_css_urls(m.group(2)), m.group(1)),
                      doc, flags=re.S)

    def strip_furniture(self, doc):
        """Remove the Framer badge and the template's promo layer."""
        before = len(doc)
        # "Made in Framer" badge: a link to framer.com carrying a referral param.
        doc = re.sub(r'<a\b[^>]*href=["\'][^"\']*framer\.com[^"\']*(?:via|utm)[^"\']*["\'][^>]*>.*?</a>',
                     "", doc, flags=re.I | re.S)
        for rx in (re.compile(r'<[a-z]+\b[^>]*id=["\'][^"\']*framer-badge', re.I),
                   re.compile(r'<[a-z]+\b[^>]*class=["\'][^"\']*framer-badge', re.I)):
            while True:
                m = rx.search(doc)
                if not m:
                    break
                span = enclosing_element(doc, m.start(), m.start() + 1)
                if not span:
                    break
                doc = doc[:span[0]] + doc[span[1]:]
                self.removed.append("Framer badge container")
        doc = re.sub(r'<div\b[^>]*class=["\'][^"\']*framer-badge[^"\']*["\'][^>]*>.*?</div>',
                     "", doc, flags=re.I | re.S)
        if len(doc) != before:
            self.removed.append("Framer badge")

        # Promo layer. Cut the smallest element that wraps each match, so the
        # markup goes with the words rather than leaving an empty shell.
        for pat in PROMO_PATTERNS:
            rx = re.compile(pat, re.I)
            cut = kept = 0
            while True:
                m = rx.search(doc)
                if not m:
                    break
                span = enclosing_element(doc, m.start(), m.end())
                if not span:
                    # Too large to cut safely, or no wrapper. Blank the text and
                    # flag it so a person looks, rather than silently leaving it.
                    doc = doc[:m.start()] + doc[m.end():]
                    kept += 1
                    continue
                doc = doc[:span[0]] + doc[span[1]:]
                cut += 1
            if cut or kept:
                self.removed.append(
                    "template promo /%s/: %d element(s) cut%s"
                    % (pat, cut, ", %d bare text run(s) deleted, REVIEW SURROUNDING MARKUP" % kept if kept else ""))
        return doc


def find_html(root, exclude=None):
    """Pick the page to import: index.html if present, else the largest.

    `exclude` keeps a previous run's output from being re-imported when the
    output path sits inside the input directory.
    """
    exclude = os.path.abspath(exclude) if exclude else None
    best = None
    for dirpath, _dirs, files in os.walk(root):
        for name in files:
            if not name.lower().endswith((".html", ".htm")):
                continue
            p = os.path.join(dirpath, name)
            if exclude and os.path.abspath(p) == exclude:
                continue
            score = (name.lower() in ("index.html", "index.htm"), os.path.getsize(p))
            if best is None or score > best[0]:
                best = (score, p)
    return best[1] if best else None


def main():
    ap = argparse.ArgumentParser(description="Import a saved Framer page into a single file.")
    ap.add_argument("input", help=".zip, directory, or .html saved from Framer")
    ap.add_argument("-o", "--out", required=True, help="output path, e.g. site/linenlegends-site.html")
    ap.add_argument("--rename", action="append", default=[], metavar="OLD=NEW",
                    help="literal string replacement, repeatable")
    ap.add_argument("--max-inline-kb", type=int, default=DEFAULT_MAX_INLINE_KB)
    ap.add_argument("--keep-badge", action="store_true", help="do not strip Framer/template furniture")
    ap.add_argument("--dry-run", action="store_true", help="report only, write nothing")
    args = ap.parse_args()

    tmp = None
    src = args.input
    if not os.path.exists(src):
        sys.exit("error: no such input: %s" % src)
    if zipfile.is_zipfile(src):
        tmp = tempfile.mkdtemp(prefix="framer-")
        with zipfile.ZipFile(src) as z:
            z.extractall(tmp)
        src = tmp

    if os.path.isdir(src):
        root = src
        page = find_html(src, args.out)
        if not page:
            sys.exit("error: no .html found under %s" % src)
    else:
        root = os.path.dirname(os.path.abspath(src)) or "."
        page = os.path.abspath(src)

    with open(page, "rb") as fh:
        doc = fh.read().decode("utf-8", "replace")
    original = len(doc)

    imp = Importer(root, page, args.max_inline_kb, args.keep_badge)
    doc = imp.run(doc)

    renames = []
    for pair in args.rename:
        if "=" not in pair:
            sys.exit("error: --rename needs OLD=NEW, got %r" % pair)
        old, new = pair.split("=", 1)
        n = doc.count(old)
        doc = doc.replace(old, new)
        renames.append((old, new, n))

    # ---- report ----
    print("source page      : %s" % page)
    print("size             : %.1f KB in -> %.1f KB out" % (original / 1024, len(doc) / 1024))
    print("assets inlined   : %d" % len(imp.inlined))
    for name, kb, n in imp.inlined[:12]:
        print("                   %-42s %5d KB%s" % (name[:42], kb, "  x%d refs" % n if n > 1 else ""))
    if len(imp.inlined) > 12:
        print("                   ... and %d more" % (len(imp.inlined) - 12))
    if imp.too_big:
        print("over --max-inline-kb (left on disk, vendor them by hand):")
        for url, kb in imp.too_big[:12]:
            print("                   %-42s %5d KB" % (url[-42:], kb))
    if imp.missing:
        print("UNRESOLVED local refs (%d) - the save is incomplete:" % len(imp.missing))
        for u in imp.missing[:12]:
            print("                   %s" % u[:76])
    if imp.remote_hosts:
        print("still loaded from the network:")
        for host, n in sorted(imp.remote_hosts.items(), key=lambda kv: -kv[1]):
            print("                   %-42s %d ref(s)" % (host, n))
    if imp.dropped_srcset:
        print("srcset dropped   : %d (image inlined into src; data URIs cannot live in srcset)"
              % imp.dropped_srcset)
    for item in imp.removed:
        print("removed          : %s" % item)
    for old, new, n in renames:
        print("renamed          : %r -> %r (%d occurrence%s)" % (old, new, n, "" if n == 1 else "s"))

    missing_sentinels = [s for s in COMPLIANCE_SENTINELS if s not in doc]
    if missing_sentinels:
        print("COMPLIANCE       : missing sentinel(s): %s" % ", ".join(missing_sentinels))
        print("                   AU compliance copy must be added before publish.")
    else:
        print("compliance       : all sentinels present")

    ids = re.findall(r'\sid="([^"]+)"', doc)
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        print("duplicate ids    : %d (%s)" % (len(dupes), ", ".join(dupes[:8])))

    blockers = bool(imp.missing) or bool(missing_sentinels)
    if args.dry_run:
        print("\nRESULT: DRY RUN, nothing written")
    else:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(doc)
        print("\nwrote %s" % args.out)
        print("RESULT: %s" % ("WRITTEN WITH WARNINGS" if blockers else "OK"))

    if tmp:
        shutil.rmtree(tmp, ignore_errors=True)
    return 1 if blockers else 0


if __name__ == "__main__":
    sys.exit(main())
