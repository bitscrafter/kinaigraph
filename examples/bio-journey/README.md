# Bio Journey — six steps of one life

A narrated portrait in under thirty seconds. Six moments arrive on a rising
sawtooth, each as its own sentence is spoken, so you read a life left to right at
the pace of the voice.

The subject is fictional: Dr. Jane Doe, a pediatrician.

## Running it

Two cuts of the same six steps. The **brief** tells the story; the **teaser**
compresses it to a single line per node.

```sh
kinaigraph bio_journey_teaser_tts.yaml   # once — needs ELEVENLABS_API_KEY, costs credits
kinaigraph bio_journey_teaser.yaml
open ./bio_journey_teaser.mp4
```

Swap `teaser` for `brief` to build the longer cut. Each length has its own
synthesis document so generating one does not bill for the other.

The narration has to exist before the teaser will render: every step derives its
dwell from its own clip's probed `.duration`, so without the audio there is
nothing for the timeline to measure.

| File | What it is |
| ---- | ---------- |
| `bio_journey_<cut>_tts.yaml` | Synthesis only. Turns that cut's six scripts into six clips. |
| `bio_journey_<cut>.yaml` | The piece. Animation plus the composition that mixes the narration onto it. |
| `resource/scene/ladder.svg` | The rails, discs and labels. Generated — see below. |
| `resource/scene/icons.svg` | The icon library. Source of truth for the six glyphs. |
| `resource/scene/icon_layer.svg` | The glyphs, placed. Generated, stacked over the ladder. |
| `resource/style/theme_bio.css` | The palette and type. |
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

**Two scenes, stacked.** The glyphs live in their own scene declared *after* the
ladder — declaration order is the render z-order — because in the brief they MOVE.
Each rides `move … along` over the very span that is drawing beneath it, so the
route the eye follows and the route the glyph travels are the same curve. A rider
has to be able to travel over the rail it rides, and that means being a separate
layer.

**Two themes, opposite ramps.** `dark` brightens toward 2025; `care` — the light
one — darkens. In both, further from the background means further along. Each
keeps the icon legible by holding the disc away from the ramp: dark disc with
near-white glyphs on `dark`, white disc with ramp-coloured glyphs on `care`.

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

Icons are edited in `resource/scene/icons.svg` and inlined into the layer by the
generator. kinaigraph does not consume cross-file `<use href="other.svg#id">`, so
the copy is unavoidable — but it is made by the script, not by hand, so the
library and the layer cannot drift.

`resource/temp/` is not published. It holds authoring tools and scratch.

⚠️ **`.seg` must never carry a `stroke-dasharray`.** The `reveal` property drives
that same attribute to draw a stroke on progressively, so revealing an
already-dashed line renders **nothing**, silently.

⚠️ **`synthesis.context.status` is section-wide.** Re-running the TTS document
regenerates all six clips and bills for all six, even if you edited one line.
