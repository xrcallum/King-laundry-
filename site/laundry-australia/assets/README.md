# Client logo assets

The "It all comes out in the wash" strip on `home-laundry.html` shows five
client brand marks. They are third-party trademarks, so they are not redrawn
in the HTML — the page ships dashed placeholder tiles instead.

To finish the page, drop the real files here and swap each tile's inner
`<div class="placeholder">` for an `<img>`:

| Order on page | Client | Suggested filename |
|---|---|---|
| 1 | Italian Street Kitchen | `italian-street-kitchen.svg` |
| 2 | Louis Vuitton | `louis-vuitton.svg` |
| 3 | RNA (The Royal National Agricultural and Industrial Association of Queensland) | `rna.svg` |
| 4 | Australian Rugby | `australian-rugby.svg` |
| 5 | Brisbane Showgrounds | `brisbane-showgrounds.svg` |

Markup to use in place of a placeholder tile:

```html
<div class="client"><img src="assets/italian-street-kitchen.svg" alt="Italian Street Kitchen" /></div>
```

SVG preferred; PNG at 2x (about 240x168) is fine. The tile is 120x84 and the
image is capped at 64px tall with `object-fit: contain`.

Confirm you hold permission to display each mark before publishing.
