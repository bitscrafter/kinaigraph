# Course Welcome — an instructor, puppeteered from the timeline

The first half-minute of an online course. An instructor greets the class from a
bubble in the corner while the practicalities arrive beside her: how many
modules, in what order, what each one ends with, where questions go.

It is the format every course, onboarding pack and internal announcement uses —
a talking head and a few lines of type — and it is normally cut by hand, keyframe
by keyframe. Here the whole thing is 28 seconds of declarations.

```sh
kinaigraph scene_01_welcome.yaml
```

Silent, and it renders from a clone with nothing installed beyond Kinaigraph.

## A state change is two pulses written against each other

**No part of the language knows what a face is.** The drawing carries three mouth
shapes and two eye states stacked in the same place, all but one hidden. `pulse`
oscillates one property and returns it — so point two of them at two shapes in
opposite directions, over the same window with the same `cycles`, and they stay
phase-locked: as one arrives the other leaves, and exactly one is visible.

```yaml
- mouth_closed:
      - pulse:
            duration: PHRASE_1_MS
            cycles: PHRASE_1_CYCLES
            opacity: { from: 1, to: 0 }
- mouth_open:
      - pulse:
            duration: PHRASE_1_MS
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
  phrases here, 2.6 s to 4.8 s, separated by pauses you can see, and the mouth
  SHAPE alternates between them: wide on the emphatic phrases, half-open on the
  quiet ones.
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

## Putting a voice under it

Every window is a share of `TALK_MS`. Declare an `audio` asset, replace that
constant with `<that asset>.duration`, and the rig re-times itself to the
recording — phrases, pauses, blinks and all. It stays silent here so it runs
anywhere, and because a mouth driven by `cycles` is a convincing puppet rather
than lip-sync: it matches the rhythm of speech, never the syllables.

## Files

| Path | What |
| ---- | ---- |
| `scene_01_welcome.yaml` | The document: the rig, the phrases and the type. |
| `resource/scene/avatar_layer.svg` | The instructor's bubble — groups `presenter`, `eyes-open`, `eyes-closed`, `mouth-closed`, `mouth-mid`, `mouth-open`, stacked at the same place. |
| `resource/scene/pitch_text.svg` | Six lines of type, one actor each. |
| `resource/scene/backdrop.svg` | The ground and the course provider's wordmark. |
| `resource/style/theme_dark.css` | Values only; each drawing owns its class-to-variable mapping. |
| `resource/template/main.html` | The HTML container. |

The provider name in the backdrop is a placeholder — one `<text>` element to
change.

## Stacking the rig on another scene

The layer is transparent outside the bubble and shares the `0 0 1280 720`
viewBox, so it drops onto any scene of that size: declare `avatar_layer` as a
second scene asset and drive the same actors from that scene's beats. The bubble
occupies x 1036–1236, y 480–680; everything else in the layer is empty.
