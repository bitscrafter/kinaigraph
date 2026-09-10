# Bio Journey — six steps of one life

A narrated portrait in under thirty seconds. Six moments arrive on a rising
sawtooth, each as its own sentence is spoken, so you read a life left to right at
the pace of the voice.

The subject is fictional: Dr. Jane Doe, a pediatrician.

## Running it

```sh
kinaigraph bio_journey_tts.yaml       # once — needs ELEVENLABS_API_KEY, costs credits
kinaigraph bio_journey_teaser.yaml
open ./bio_journey_teaser.mp4
```

The narration has to exist before the teaser will render: every step derives its
dwell from its own clip's probed `.duration`, so without the audio there is
nothing for the timeline to measure.

| File | What it is |
| ---- | ---------- |
| `bio_journey_tts.yaml` | Synthesis only. Turns the six scripts into the six clips. |
| `bio_journey_teaser.yaml` | The piece. Animation plus the composition that mixes the narration onto it. |
| `resource/scene/ladder.svg` | The artwork. Generated — see below. |
| `resource/style/theme_bio.css` | The palette and type. |
| `resource/script/part_NN_*.txt` | One sentence per step. |
| `resource/audio/part_NN_*.mp3` | The recordings, once generated. |

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

## Editing it

**The geometry is generated.** `resource/scene/ladder.svg` comes out of a local
script — edit its `NODES` table and re-run it rather than hand-editing coordinates:

```sh
python3 resource/temp/make_ladder_svg.py
```

`resource/temp/` is not published. It holds authoring tools and scratch.

⚠️ **`.seg` must never carry a `stroke-dasharray`.** The `reveal` property drives
that same attribute to draw a stroke on progressively, so revealing an
already-dashed line renders **nothing**, silently.

⚠️ **`synthesis.context.status` is section-wide.** Re-running the TTS document
regenerates all six clips and bills for all six, even if you edited one line.
