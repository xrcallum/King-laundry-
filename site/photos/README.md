# Journey photographs — shot list

The five steps in "How a collection actually goes" ship as hand-drawn SVG. They
are honest as drawings, but they are drawings, and a service whose whole pitch
is *nothing is hidden behind a phone call* reads stronger with photographs of
the actual operation.

Drop a photo in here and it replaces that step's drawing. Steps without a photo
keep the drawing, so this can be done one shot at a time.

## What to shoot

One real collection, start to finish. About 45 minutes on a phone, shot on a
round you are doing anyway. Portrait or landscape both work — the embed crops
to 4:3 from the centre.

| File | Step | The shot | Must be in frame |
|---|---|---|---|
| `jn-1.jpg` | 01 You put it out | A tied laundry bag sitting on a doorstep, gate or in a garage. No person. | The bag, the doorstep. Shoot it as the operator finds it — not staged neat. |
| `jn-2.jpg` | 02 Weighed at your door | Operator's hands holding the digital scale with the bag hanging from it, at the door. | The scale readout legible. Hands and torso only — no face unless you have the release below. |
| `jn-3.jpg` | 03 Into your operator's round | Bags going into the back of the vehicle, or the loaded vehicle on a suburban street. | The LK decal or a branded bag, so it is visibly yours. |
| `jn-4.jpg` | 04 Washed on its own cycle | One household's load going into a single machine — door open, one bag's worth. | One load, one machine. This shot is the proof of the claim, so do not fake a full wall of machines you do not have. |
| `jn-5.jpg` | 05 Back on your doormat | Folded stack in the LK bag, tagged with the reference, back on the doorstep. | The reference tag readable enough to look real, but not a real customer's job number. |

## Rules that make these usable

- **No identifiable customer, house number or number plate** unless you have a
  signed release on file. Frame them out, or shoot at your own place. A blurred
  plate reads as a blurred plate; better to not have it in shot.
- **Anyone recognisable in frame needs a written release** — including an
  operator, who is a contractor, not an employee. One line by email, kept in
  `LEG02`, is enough. Faces are not needed for any of these five shots.
- **Shoot it real.** These sit under sentences making specific promises
  ("~90 seconds", "never mixed with another household"). A staged photo that
  contradicts the copy is worse than the drawing — that is an Australian
  Consumer Law misleading-conduct question, not a design question.
- **Natural light, phone camera, no filter.** Slightly imperfect reads as
  genuine; over-produced reads as stock.
- Shoot a few frames of each and pick later. Storage is free, a second trip is not.

## How to put them in

1. Save the files here as `jn-1.jpg` … `jn-5.jpg`. Full resolution is fine —
   they get resized. `.jpeg`, `.png` and `.webp` also work.
2. Write the alt text for each one in `photos.json`. Describe what is in the
   frame. This is required: the embed refuses to run without it, because alt
   text for a photo has to be written by whoever saw the photo.
3. Embed and check:

   ```
   python3 tools/embed_photos.py site/laundrykings-site.html
   python3 verify/preflight.py site/laundrykings-site.html
   ```

4. Commit, publish, confirm on a phone — the normal workflow in the root README.

To pull them all back out again: `python3 tools/embed_photos.py
site/laundrykings-site.html --strip`. That restores the drawings exactly.

## Why the photos live inside the HTML

The site publishes as one self-contained file, so there is nowhere to put a
sibling image. Each photo is resized to 640x480, encoded as WebP and written in
as a data URI — roughly 35 KB each, about 175 KB for all five on a 420 KB page.
The originals stay here in the repo at full resolution; only the small versions
travel in the published file.
