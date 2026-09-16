# Course Welcome — an instructor, puppeteered from the timeline

The first half-minute of an online course. An instructor greets the class from a
bubble in the corner while the practicalities arrive beside her: how many
modules, in what order, what each one ends with, where questions go.

It is the format every course, onboarding pack and internal announcement uses —
a talking head and a few lines of type — and it is normally cut by hand, keyframe
by keyframe. Here the whole thing is 22 seconds of declarations.

```sh
kinaigraph scene_00_tts_welcome.yaml   # once — costs credits; the recordings are committed
kinaigraph scene_01_welcome.yaml
```

The narration is in the repository, so a clone renders it with no key.

## A state change is two pulses written against each other

**No part of the language knows what a face is.** The drawing carries three mouth
shapes and two eye states stacked in the same place, all but one hidden. `pulse`
oscillates one property and returns it — so point two of them at two shapes in
opposite directions, over the same window with the same `cycles`, and they stay
phase-locked: as one arrives the other leaves, and exactly one is visible.

```yaml
- mouth_closed:
      - pulse:
            duration: "narration_1.duration"
            cycles: PHRASE_1_CYCLES
            opacity: { from: 1, to: 0 }
- mouth_open:
      - pulse:
            duration: "narration_1.duration"
            cycles: PHRASE_1_CYCLES
            opacity: { from: 0, to: 1 }
```

That is the whole technique, and it is not about faces: any drawing with two or
more states in one place — a switch, a signal, a valve, a character — can be
driven this way without the language having a concept for it.

⚠️ **The pair is held together by its numbers, not by a relationship.** Nothing
declares that these two actors belong to each other; equal `duration` and equal
`cycles` are what keep them in step. Change one and the other does not follow —
for part of every cycle both shapes will be visible, or neither.

## What makes it read as alive

- **Speech is phrases, not a flap.** One pulse across the whole talk gives a
  single rate with no silences, which is what reads as a machine. There are six
  phrases here, 1.4 s to 4.0 s, separated by pauses you can see, and the mouth
  SHAPE alternates between them: wide on the emphatic phrases, half-open on the
  quiet ones.
- **A phrase lasts as long as its recording.** Only the RATE is authored — how
  many times the mouth opens across the line. Re-record a sentence and its phrase
  re-times itself, the ones after it shift, and the flap stays at the same
  syllables per second because the cycle count travels with the line.
- **Blinks are irregular** — five of them, at gaps of 2.2, 4.6, 3.1, 5.2 and
  4.4 s. Evenly spaced blinks read as a metronome. Each lasts 150 ms, long enough
  to see and short enough not to look like a wince.
- **Two idle cycles that do not divide into each other.** The bubble breathes
  (scale, 8 cycles) and sways (rotation, 3 cycles) across the same window, so it
  never returns to the same pose on a beat. ⚠️ A rotation target must sit in
  `[0, 360)`, so the sway rocks from upright to 1.6° rather than either side of
  centre.
- **One line of type per phrase**, arriving as that phrase opens, so a viewer
  reads a glance while the instructor keeps talking.

⚠️ **`hold.before` is measured from the BOOKMARK, not from the entry above it.**
Sub-actions of the same type chain inside one entry — which is why the mouth's
waits are gaps — but separate actors each start at the bookmark. The six lines are
six actors, so each states the whole elapsed time. Write a gap there instead and
line 3 appears before line 2, with nothing to say it is wrong.

## The voice, and what it is not

Each phrase takes its length from `narration_N.duration`, and the animation is
captured silent before a `composition` lays the six lines over it — each mix
placed at the same expression the timeline used, which is what keeps a mouth and
its voice on the same instant.

⚠️ **This is a puppet, not lip-sync.** A mouth driven by `cycles` matches the
RHYTHM of speech and never the syllables. That is enough at this size, and it is
why re-recording a line needs no re-authoring: the new clip is longer or shorter,
the same number of flaps spread across it, and nothing looks wrong.

⚠️ **The spoken lines are not the lines on screen.** The type carries the fact in
as few words as possible, to be read at a glance; the voice says it the way a
person would. A voice that reads the screen aloud finishes second, because the
viewer is faster.

## Files

| Path | What |
| ---- | ---- |
| `scene_01_welcome.yaml` | The document: the rig, the phrases and the type. |
| `resource/scene/avatar_layer.svg` | The instructor's bubble — groups `presenter`, `eyes-open`, `eyes-closed`, `mouth-closed`, `mouth-mid`, `mouth-open`, stacked at the same place. |
| `resource/scene/pitch_text.svg` | Six lines of type, one actor each. |
| `resource/scene/backdrop_agentic.svg` | The default ground: a lit gradient, a prompt and its reply behind the type, and a diagram of agents wired to their tools on the right. |
| `resource/scene/backdrop.svg` | The plain alternative — flat ground and the wordmark. |
| `resource/style/theme_dark.css` · `theme_paper.css` | Two themes, values only; each drawing owns its class-to-variable mapping. |
| `resource/script/*.txt` · `resource/audio/*.mp3` | The six spoken lines, and their recordings. |
| `resource/template/main.html` | The HTML container. |

## Three looks, and the pairing that matters

All three stylesheets declare an **identical set of variable names** — the drawings
map their own classes onto those names, so re-skinning is an edit to the document's
`style` asset and nothing else:

| look | backdrop | theme | reads as |
| ---- | -------- | ----- | -------- |
| agentic *(default)* | `backdrop_agentic.svg` | `theme_agentic.css` | a lit gradient with a faint agent-and-tool diagram behind the type |
| paper | `backdrop.svg` | `theme_paper.css` | warm white, ink type |
| dark | `backdrop.svg` | `theme_dark.css` | the lecture-hall version |

⚠️ **A backdrop and a theme are a pair.** The gradient backdrop paints its own
light ground, so it wants ink type and an outlined bubble; put `theme_dark` behind
it and you get white text on white. Swapping a look means swapping both lines.

⚠️ **A theme that omits a name a drawing reads** re-skins part of the picture and
leaves the rest on the literal fallback baked into the SVG — so the check is that
the three files declare the same SET of names, not the same number of them.

**A light gradient does not need a panel under its type.** Ink reads on this one
end to end — 14.1:1 for the heading and 8.2:1 for the body at its darkest corner —
and a panel would have hidden the drawing it sits on. ⚠️ **What is behind the words
is drawn fainter than what is not**: 6% under the text column against 10% for the
diagram on the right, because anything that competes with a sentence has lost. Reach for one when the type
crosses something busy or dark; measure first, because a panel costs you the
background you chose.

The provider name in the backdrop is a placeholder — one `<text>` element to
change.

## Stacking the rig on another scene

The layer is transparent outside the bubble and shares the `0 0 1280 720`
viewBox, so it drops onto any scene of that size: declare `avatar_layer` as a
second scene asset and drive the same actors from that scene's beats. The bubble
occupies x 1036–1236, y 480–680; everything else in the layer is empty.
