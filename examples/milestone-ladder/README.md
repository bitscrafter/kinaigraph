# Milestone Ladder — six steps of one life

A narrated portrait in under thirty seconds. Six moments arrive on a rising
sawtooth, each as its own sentence is spoken, so you read a life left to right at
the pace of the voice.

The subject is fictional: Dr. Jane Doe, a pediatrician.

## Running it

Two cuts of the same six steps. The **brief** tells the story; the **teaser**
compresses it to a single line per node.

```sh
kinaigraph milestone_ladder_teaser_tts.yaml   # once — needs ELEVENLABS_API_KEY, costs credits
kinaigraph milestone_ladder_teaser.yaml
open ./milestone_ladder_teaser.mp4
```

Swap `teaser` for `brief` to build the longer cut. Each length has its own
synthesis document so generating one does not bill for the other.

The narration has to exist before the teaser will render: every step derives its
dwell from its own clip's probed `.duration`, so without the audio there is
nothing for the timeline to measure.

| File | What it is |
| ---- | ---------- |
| `milestone_ladder_<cut>_tts.yaml` | Synthesis only. Turns that cut's six scripts into six clips. |
| `milestone_ladder_<cut>.yaml` | The piece. Animation plus the composition that mixes the narration onto it. |
| `resource/scene/ladder.svg` | The rails, discs and labels. Generated — see below. |
| `resource/scene/icons.svg` | The six glyphs, copied from the shared catalog. |
| `resource/scene/icon_layer.svg` | The glyphs, placed. Generated, stacked over the ladder. |
| `resource/scene/brand_layer.svg` | The brand mark, embedded as data. Generated from the PNG. |
| `resource/image/bitscrafter_logo.png` | Source of truth for the mark. |
| `resource/style/theme_ladder.css` | The palette and type. |
| `resource/script/<cut>/part_NN_*.txt` | The narration, one file per step. |
| `resource/audio/<cut>/part_NN_*.mp3` | The recordings, once generated. |

## What this example is a good place to notice

**The shape carries the argument.** Time runs left to right, always, so the order
is never in doubt. The zigzag is vertical only — it exists to keep six labels from
colliding, and to stop a life reading as a staircase. Two of the steps sit *lower*
than the one before: 2017 and 2022 were lateral moves, and a shape that only rises
would be lying about them.

**The palette is sequential, not categorical.** One hue brightening across the six
nodes, rather than six different colours. Six hues would say these are six *kinds*
of thing; one brightening hue says they are one thing getting further along.

**The ramp is on the ring, never the disc.** The icons are near-white, and white on
the bright end of the ramp measures about 2.2:1 — unreadable. A dark disc at every
step keeps the icon legible while the glow still carries the progression.

**Six clips, not one.** A single narration file would leave the timeline nothing to
measure per step. One clip per node is what lets each step hold for exactly its own
sentence and no longer.

**Three scenes, stacked.** The glyphs live in their own scene declared *after* the
ladder — declaration order is the render z-order — because in the brief they MOVE.
Each rides `move … along` over the very span that is drawing beneath it, so the
route the eye follows and the route the glyph travels are the same curve. A rider
has to be able to travel over the rail it rides, and that means being a separate
layer. The brand mark is a third, on top.

**The mark is embedded, not referenced — and not in the ladder.** A scene SVG is
inlined into the compiled page, so a relative `href` would resolve against
wherever that *page* lands, and `--outdir` can move it; data survives the move.
It gets its own file because the payload is ~60 KB of base64 — carried inside
`ladder.svg` it would be four fifths of the file and bury the geometry, which is
what happens in the architecture video it came from. The PNG stays the source of
truth and the generator does the encoding.

**Two themes, opposite ramps.** `dark` brightens toward 2025; `care` — the light
one — darkens. In both, further from the background means further along. Each
keeps the icon legible by holding the disc away from the ramp: dark disc with
near-white glyphs on `dark`, white disc with ramp-coloured glyphs on `care`.

**A scene opens on its own.** Each carries a `<style>` block holding the MAPPING —
which class takes which property from which variable — while `theme_ladder.css`
holds the VALUES. Every `var()` in a scene is emitted with the stylesheet's `.dark`
value as its fallback, so opening `ladder.svg` in a browser, an editor or a GitHub
preview shows the dark theme rather than unstyled shapes; whenever the stylesheet
is in scope, the theme wins.

Nothing is duplicated by that split: a mapping lives in the scene, a value lives in
the stylesheet. The one exception is deliberate — the `.dark` column appears twice,
once as values and once as fallbacks — and the generator READS the stylesheet to
produce them, so they cannot drift. A variable a scene uses but the stylesheet does
not define stops generation rather than emitting a fallback-less `var()`.

**Arial only, deliberately.** Nothing in the stylesheet may name a font that is
not installed by default on Windows, macOS and Linux — an example that renders
differently depending on who clones it is a broken example. Liberation Sans, the
Linux default, is metric-compatible with Arial, so a fallback shifts no layout.
There is no cross-platform cursive; a script face would have to be embedded.

**Names are the contract, not positions.** Every node carries a slug — `internship` —
and it is the SVG id suffix (`node-internship`, `seg-internship`, `label-internship`)
*and* the script filename suffix (`part_03_internship.txt`). Re-order the ladder and
nothing can silently pair a line with the wrong node.

## Editing it

**The geometry is generated.** `resource/scene/ladder.svg` comes out of a local
script — edit its `NODES` table and re-run it rather than hand-editing coordinates:

```sh
python3 resource/temp/make_ladder_svg.py   # rewrites ladder.svg AND icon_layer.svg
./resource/temp/make_preview.sh care       # a still, in either theme
```

**Icons come from a shared catalog**, not from here. The source of truth is
`tech-docs/internal/design/diagram/icon-catalog.svg` in the engine repo; this
example carries a six-symbol subset, and an edit belongs upstream first.

They are named for the SHAPE — `clock`, `graduate`, `stethoscope`, `heart`,
`hospital`, `group` — not for what this example means by them. A heart is a heart
wherever it is used; an "affinity" would only make sense here.

Colour comes from the catalog's class vocabulary (`icon-fill`, `icon-stroke`,
`icon-fill-dark`, …), which resolves against `--icon-*` custom properties that
`theme_ladder.css` binds per theme. So one drawing serves dark and light, and a
symbol drops in from the catalog unmodified.

kinaigraph does not consume cross-file `<use href="other.svg#id">`, so the
symbols are mirrored again into `icon_layer.svg` — but by the generator reading
this file, not by hand.

`resource/temp/` is not published. It holds authoring tools and scratch.

⚠️ **`.seg` must never carry a `stroke-dasharray`.** The `reveal` property drives
that same attribute to draw a stroke on progressively, so revealing an
already-dashed line renders **nothing**, silently.

⚠️ **`synthesis.context.status` is section-wide.** Re-running the TTS document
regenerates all six clips and bills for all six, even if you edited one line.
