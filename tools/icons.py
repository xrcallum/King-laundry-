"""Laundrylegends icon sprite — 24px grid, 1.75 stroke, currentColor.

One symbol per icon. Presentation attributes sit on the <symbol> so they are
inherited by the paths through the shadow tree, which keeps each <use> site to
a single element. Authored to replace every emoji in the file (Dossier v2,
Part 8). Geometry is drawn on a 24x24 box with a 2px optical margin.
"""

ICONS = {
    # ---- tab bar -------------------------------------------------------
    "home": '<path d="M4 10.9 12 4.2l8 6.7V19.2a1.4 1.4 0 0 1-1.4 1.4h-3.7v-6h-5.8v6H5.4A1.4 1.4 0 0 1 4 19.2z"/>',
    "list": '<path d="M9.2 6.2h10.6M9.2 12h10.6M9.2 17.8h10.6"/><path d="M4.6 6.2h.01M4.6 12h.01M4.6 17.8h.01"/>',
    "plus-circle": '<circle cx="12" cy="12" r="8.6"/><path d="M12 8.2v7.6M8.2 12h7.6"/>',
    "chat": '<path d="M20.2 12a7.3 7.3 0 0 1-7.3 7.3H8.4l-4.6 3v-4.9A7.3 7.3 0 0 1 3.8 12a7.3 7.3 0 0 1 7.3-7.3h1.8A7.3 7.3 0 0 1 20.2 12z"/>',
    "settings": '<path d="M4.4 20.8v-6.4M4.4 10.6V3.2M12 20.8v-8.4M12 8.6V3.2M19.6 20.8v-4.4M19.6 12.6V3.2"/><path d="M1.8 14.4h5.2M9.4 8.6h5.2M17 16.4h5.2"/>',

    # ---- service and flow ---------------------------------------------
    "truck": '<path d="M3.2 16.8V7.2a1.2 1.2 0 0 1 1.2-1.2h8.8a1.2 1.2 0 0 1 1.2 1.2v9.6"/><path d="M14.4 9.6h3.4l2.8 3.4v3.8"/><path d="M3.2 16.8h1.6M9.2 16.8h3.2M18.4 16.8h2.2"/><circle cx="6.6" cy="18.2" r="1.6"/><circle cx="16.4" cy="18.2" r="1.6"/>',
    "basket": '<path d="M4.6 9.2h14.8l-1.3 9.4a1.8 1.8 0 0 1-1.8 1.6H7.7a1.8 1.8 0 0 1-1.8-1.6z"/><path d="M9 9.2 12 3.6l3 5.6"/><path d="M9.8 13v3.4M14.2 13v3.4"/>',
    "shirt": '<path d="M8.6 3.4 4 6l2 4.3 2.2-1.1v11.4h7.6V9.2l2.2 1.1L20 6l-4.6-2.6a3.4 3.4 0 0 1-6.8 0z"/>',
    "hanger": '<path d="M12 9.8v-.9a2.1 2.1 0 1 1 2.1-2.1"/><path d="M12 9.8 3.4 17.9a1.1 1.1 0 0 0 .7 1.9h15.8a1.1 1.1 0 0 0 .7-1.9z"/>',
    "scale": '<circle cx="12" cy="4.2" r="1.4"/><path d="M12 5.6v14.2M8.4 19.8h7.2M4.6 8.2h14.8"/><path d="M4.6 8.2 2.2 14a2.9 2.9 0 0 0 4.8 0z"/><path d="M19.4 8.2 21.8 14a2.9 2.9 0 0 1-4.8 0z"/>',
    "box": '<path d="M3.4 8.4 12 4.2l8.6 4.2v7.2L12 19.8l-8.6-4.2z"/><path d="M3.4 8.4 12 12.6l8.6-4.2M12 12.6v7.2"/>',
    "calendar": '<rect x="3.6" y="5.6" width="16.8" height="14.8" rx="1.6"/><path d="M3.6 10.4h16.8M8.4 3.4v4.2M15.6 3.4v4.2"/>',
    "clock": '<circle cx="12" cy="12" r="8.6"/><path d="M12 7.2V12l3.2 1.9"/>',
    "pin": '<path d="M12 20.8c3.7-3.9 5.6-7.1 5.6-9.6a5.6 5.6 0 1 0-11.2 0c0 2.5 1.9 5.7 5.6 9.6z"/><circle cx="12" cy="10.9" r="2.2"/>',

    # ---- account and money --------------------------------------------
    "user": '<circle cx="12" cy="8.2" r="3.6"/><path d="M4.8 20.4a7.2 7.2 0 0 1 14.4 0"/>',
    "users": '<circle cx="9.6" cy="8.4" r="3.2"/><path d="M3.4 20.4a6.2 6.2 0 0 1 12.4 0"/><path d="M16.4 5.6a3.2 3.2 0 0 1 0 6.2M18 14.8a5 5 0 0 1 3.4 4.6"/>',
    "receipt": '<path d="M6.2 3.4h11.6a1 1 0 0 1 1 1v16.2l-2.7-1.6-2.5 1.6-2.4-1.6-2.4 1.6-2.6-1.6V4.4a1 1 0 0 1 1-1z"/><path d="M8.6 8.4h6.8M8.6 12h6.8M8.6 15.4h4"/>',
    "card": '<rect x="2.8" y="5.4" width="18.4" height="13.2" rx="1.8"/><path d="M2.8 10.2h18.4M6.6 14.8h3.4"/>',
    "bank": '<path d="M3 9.8 12 4.2l9 5.6"/><path d="M5.4 9.8v8.4M9.8 9.8v8.4M14.2 9.8v8.4M18.6 9.8v8.4M3 20.2h18"/>',
    "doc": '<path d="M13.8 3.4H7.4a1.2 1.2 0 0 0-1.2 1.2v14.8a1.2 1.2 0 0 0 1.2 1.2h9.2a1.2 1.2 0 0 0 1.2-1.2V7.6z"/><path d="M13.8 3.4v4.2h4M9 12.4h6M9 16h6"/>',
    "lock": '<rect x="4.4" y="10.2" width="15.2" height="10.4" rx="1.8"/><path d="M8 10.2V7.4a4 4 0 0 1 8 0v2.8"/>',
    "shield": '<path d="M12 3.4 5.2 6.2v5.4c0 4.2 2.8 7.9 6.8 9.1 4-1.2 6.8-4.9 6.8-9.1V6.2z"/><path d="M9.3 11.9l2 2 3.5-3.6"/>',

    # ---- system --------------------------------------------------------
    "check": '<path d="M4.6 12.4 9.6 17.4 19.4 6.8"/>',
    "check-circle": '<circle cx="12" cy="12" r="8.6"/><path d="M8.2 12.2 10.9 15 16 9.6"/>',
    "x": '<path d="M6.2 6.2 17.8 17.8M17.8 6.2 6.2 17.8"/>',
    "arrow-right": '<path d="M4.4 12h14.4M13.2 6.4 18.8 12l-5.6 5.6"/>',
    "chevron-right": '<path d="M9.4 5.6 15.8 12l-6.4 6.4"/>',
    "refresh": '<path d="M20.4 12a8.4 8.4 0 1 1-2.5-6"/><path d="M20.6 3.8v5.4h-5.4"/>',
    "info": '<circle cx="12" cy="12" r="8.6"/><path d="M12 11.2v5.4M12 7.8h.01"/>',
    "alert": '<path d="M12 4.2 21.4 20.4H2.6z"/><path d="M12 10v4.6M12 17.6h.01"/>',
    "help": '<circle cx="12" cy="12" r="8.6"/><path d="M9.5 9.5a2.6 2.6 0 0 1 5.1.8c0 1.7-2.6 2.2-2.6 4"/><path d="M12 17.6h.01"/>',
    "plus": '<path d="M12 5.2v13.6M5.2 12h13.6"/>',
    "pencil": '<path d="M4.2 19.8 5 16l10.6-10.6a2 2 0 0 1 2.9 2.9L7.9 18.9z"/><path d="M14.2 6.9l2.9 2.9"/>',
    "link": '<path d="M10.6 13.4a3.8 3.8 0 0 0 5.4 0l2.8-2.8a3.8 3.8 0 0 0-5.4-5.4l-1.6 1.6"/><path d="M13.4 10.6a3.8 3.8 0 0 0-5.4 0l-2.8 2.8a3.8 3.8 0 0 0 5.4 5.4l1.6-1.6"/>',
    "star": '<path d="M12 3.6 14.6 9l5.8.9-4.2 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8L3.6 9.9 9.4 9z"/>',
    "crown": '<path d="M3.2 8.2 7 11.4 12 4.4l5 7 3.8-3.2-1.7 10.6a1.1 1.1 0 0 1-1.1.9H6a1.1 1.1 0 0 1-1.1-.9z"/>',
    "sparkle": '<path d="M10.4 3.6 12 8.2l4.6 1.6L12 11.4l-1.6 4.6-1.6-4.6L4.2 9.8l4.6-1.6z"/><path d="M17.6 14.6l.9 2.3 2.3.9-2.3.9-.9 2.3-.9-2.3-2.3-.9 2.3-.9z"/>',
    "clipboard": '<path d="M9.2 4.8H7.4a1.2 1.2 0 0 0-1.2 1.2v13.4a1.2 1.2 0 0 0 1.2 1.2h9.2a1.2 1.2 0 0 0 1.2-1.2V6a1.2 1.2 0 0 0-1.2-1.2h-1.8"/><path d="M9.2 4.8a1.2 1.2 0 0 1 1.2-1.2h3.2a1.2 1.2 0 0 1 1.2 1.2v1.4H9.2z"/>',
    "phone": '<rect x="6.2" y="3.4" width="11.6" height="17.2" rx="1.8"/><path d="M10.4 17.6h3.2"/>',
    "mail": '<rect x="2.8" y="5.4" width="18.4" height="13.2" rx="1.6"/><path d="M3.4 6.6 12 13l8.6-6.4"/>',
    "headset": '<path d="M4.6 14.6v-2.4a7.4 7.4 0 0 1 14.8 0v2.4"/><path d="M4.6 13.2a2 2 0 0 1 2 2v2a2 2 0 0 1-4 0v-2a2 2 0 0 1 2-2zM19.4 13.2a2 2 0 0 1 2 2v2a2 2 0 0 1-4 0v-2a2 2 0 0 1 2-2z"/><path d="M19.4 17.4v.8a2.6 2.6 0 0 1-2.6 2.6h-2.2"/>',
    "megaphone": '<path d="M4.2 10.4v3.2a1.2 1.2 0 0 0 1.2 1.2h2.8l7.6 4.4V4.8L8.2 9.2H5.4a1.2 1.2 0 0 0-1.2 1.2z"/><path d="M18.4 9.4a3.8 3.8 0 0 1 0 5.2M8.2 14.8v4.4h2.6"/>',
    "chart": '<path d="M4.4 20V10.4M10.1 20V4.6M15.8 20v-6.8M21.5 20H2.5"/>',
    "worker": '<path d="M4.4 17.8h15.2"/><path d="M6.2 17.8v-3a5.8 5.8 0 0 1 11.6 0v3"/><path d="M9.8 9.2V5.4a1.1 1.1 0 0 1 1.1-1.1h2.2a1.1 1.1 0 0 1 1.1 1.1v3.8"/>',
    "chevron-down": '<path d="M5.6 9.4 12 15.8l6.4-6.4"/>',
    "chevron-left": '<path d="M14.6 5.6 8.2 12l6.4 6.4"/>',
    "minus": '<path d="M5.2 12h13.6"/>',
    "grid": '<rect x="3.6" y="3.6" width="7.2" height="7.2" rx="1.4"/><rect x="13.2" y="3.6" width="7.2" height="7.2" rx="1.4"/><rect x="3.6" y="13.2" width="7.2" height="7.2" rx="1.4"/><rect x="13.2" y="13.2" width="7.2" height="7.2" rx="1.4"/>',
    "gear": '<circle cx="12" cy="12" r="3.1"/><path d="M12 2.8v2.4M12 18.8v2.4M4.5 12H2.1M21.9 12h-2.4M6.7 6.7 5 5M19 19l-1.7-1.7M6.7 17.3 5 19M19 5l-1.7 1.7"/>',
}

# Tab-bar icons use the same grid but are referenced separately so a future
# change to the bar does not disturb the content icons.
SPRITE_ORDER = list(ICONS.keys())


def sprite_html():
    parts = ['<svg class="ic-sprite" aria-hidden="true" focusable="false" style="position:absolute;width:0;height:0;overflow:hidden"><defs>']
    for name in SPRITE_ORDER:
        parts.append(
            '<symbol id="ic-%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">%s</symbol>'
            % (name, ICONS[name])
        )
    parts.append("</defs></svg>")
    return "".join(parts)


def use(name, cls="ic"):
    return '<svg class="%s" aria-hidden="true"><use href="#ic-%s"/></svg>' % (cls, name)
