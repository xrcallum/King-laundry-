# Journey photographs

The five steps in "How a collection actually goes" ship text-only: a numeral, a
heading, a line of copy. The hand-drawn illustrations that used to sit above
that text were removed — they read as clip art, not craft, and a placeholder
picture was worse than none. Drop a photo in here and it fills that step's slot;
a step with no photo yet just stays text-only, so this can be done one at a time.

Decision of 19 September 2026: **licensed stock first**, own photographs when a
round can be shot. Both routes use the same slots and the same command.

---

## Route A — licensed stock (current plan)

### Where to get them

| Library | Licence | Attribution | Search at |
|---|---|---|---|
| Unsplash | Unsplash License — free commercial use | Not required | unsplash.com |
| Pexels | Pexels License — free commercial use | Not required | pexels.com |
| Pixabay | Pixabay Content License — free commercial use | Not required | pixabay.com |
| Openverse | Mixed (CC0, CC-BY, CC-BY-SA) — **check each** | Varies | openverse.org |

Prefer Unsplash or Pexels. Openverse mixes licences and some require
attribution or share-alike, which is more admin than it's worth for five
thumbnails.

### What to search for, slot by slot

Each photo sits directly under a sentence making a specific claim, so it has to
match that claim, not just the general topic.

| File | Step | Search terms | Must show | Reject |
|---|---|---|---|---|
| `jn-1.jpg` | 01 You put it out | `laundry bag doorstep`, `canvas laundry bag floor`, `parcel on doorstep` | A closed bag of laundry sitting on a step or floor by a door | Anyone in shot; a plastic supermarket bag; a hamper indoors |
| `jn-2.jpg` | 02 Weighed at your door | `digital luggage scale`, `hanging scale bag`, `weighing bag hand` | Hands and a hand-held digital scale with something hanging from it | A bathroom scale; a kitchen scale; a visible face |
| `jn-3.jpg` | 03 Into your operator's round | `white van suburban street`, `loading van boxes`, `delivery van rear doors open` | A plain small van, ideally loading, on a residential street | Any other company's livery or logo; a big rigid truck; a warehouse |
| `jn-4.jpg` | 04 Washed on its own cycle | `washing machine door open laundry`, `front loader single load` | **One** machine, door open, one load going in | A laundromat wall of machines — it contradicts "not a warehouse" |
| `jn-5.jpg` | 05 Back on your doormat | `folded laundry stack`, `neatly folded towels`, `folded clothes pile` | A tidy folded stack, warm/neutral light | A retail shelf display; branded packaging |

### Rules

- **No other company's branding, signage, livery or logo in frame.** This is the
  one that bites — check the background of every candidate.
- **No recognisable faces.** A stock model is licensed, but a face makes the
  photo read as "our operator", which it isn't.
- **Nothing that contradicts the copy.** A row of twenty machines under "never
  mixed with another household" is a misleading-conduct problem, not a taste
  problem.
- **Landscape or square, at least 1200px wide.** The embed crops to 4:3 from the
  centre, so keep the subject centred.
- **Record the licence.** `photos.json` will not accept a non-own photo without
  a `licence` and a `url`. That record is the whole point of using licensed
  stock rather than whatever turns up in an image search.

### Honest limitation

Stock is someone else's laundry. It is reverse-image-searchable, and other
businesses will be using the same frames. It buys a more finished-looking page;
it does not buy proof. Treat it as the interim — Route B is what actually makes
the page evidence of anything. Don't caption stock as though it were a
LaundryKings job.

---

## Route B — your own photographs (the upgrade)

One real collection, start to finish. About 45 minutes on a phone, on a round
that's happening anyway.

| File | The shot | Must be in frame |
|---|---|---|
| `jn-1.jpg` | A tied laundry bag as the operator finds it — doorstep, gate, garage. | The bag and the step. Not staged neat. |
| `jn-2.jpg` | Operator's hands holding the scale, bag hanging, at the door. | The readout legible. Hands and torso only. |
| `jn-3.jpg` | Bags going into the back of the vehicle, or the loaded van on a street. | The LK decal or a branded bag, so it is visibly yours. |
| `jn-4.jpg` | One household's load going into a single machine. | One load, one machine. This is the proof of the claim. |
| `jn-5.jpg` | Folded stack in the LK bag, tagged, back on the doorstep. | Tag readable enough to look real, not a real job number. |

- **No identifiable customer, house number or number plate** without a signed
  release on file. Frame them out — a blurred plate reads as a blurred plate.
- **Anyone recognisable needs a written release**, including an operator, who is
  a contractor, not an employee. One line by email, kept in `LEG02`. None of
  these five shots need a face.
- Natural light, phone camera, no filter. Slightly imperfect reads as genuine.
- Shoot several frames of each. Storage is free; a second trip is not.

---

## How to put them in

1. Save the files here as `jn-1.jpg` … `jn-5.jpg`. Full resolution is fine —
   they get resized. `.jpeg`, `.png` and `.webp` also work.
2. Fill in `photos.json`: `alt` and `source` for every photo, plus `licence` and
   `url` for anything not shot by us. Alt text describes what is in the frame,
   not what the step is about.
3. Embed and check:

   ```
   python3 tools/embed_photos.py site/laundrykings-site.html
   python3 verify/preflight.py site/laundrykings-site.html
   ```

   The first command also regenerates `CREDITS.md` — the licence record. Commit it.

4. Commit, publish, confirm on a phone — the workflow in the root README.

To pull them all back out: `python3 tools/embed_photos.py
site/laundrykings-site.html --strip`. That returns every step to text-only.

## Why the photos live inside the HTML

The site publishes as one self-contained file, so there is nowhere to put a
sibling image. Each photo is resized to 640x480, encoded as WebP and written in
as a data URI — roughly 35 KB each, about 175 KB for all five on a 420 KB page.
The originals stay here at full resolution; only the small versions travel in
the published file.
