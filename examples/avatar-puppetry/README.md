# Avatar Puppetry — a rig driven from the timeline

A presenter talks, blinks and breathes in the corner of a 1280 × 720 slide while
four lines of type arrive beside him. **No part of the language knows what a face
is.** The drawing carries three mouth shapes and two eye states stacked on top of
each other, all but one hidden, and the document swaps between them.

22 seconds, silent, and it renders from a clone with nothing installed beyond
Kinaigraph itself.

```sh
kinaigraph scene_01_presenter.yaml
```

## A state change is two pulses written against each other

`pulse` oscillates one property and returns it. Point two of them at two shapes
in opposite directions, over the same window with the same `cycles`, and they
stay phase-locked — as one arrives the other leaves, so exactly one is visible:

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

That is the whole technique, and it generalises past faces: any drawing that has
two or more states in the same place — a switch, a signal, a valve, a character —
can be driven this way without the language having a concept for it.

⚠️ **The pair is held together by its numbers, not by a relationship.** Nothing
declares that these two actors belong to each other; equal `duration` and equal
`cycles` are what keep them in step. Change one and the other does not follow —
both shapes will be visible at once for part of the cycle, or neither will.

## What makes it read as alive

- **Speech is phrases, not a flap.** One pulse across the whole talk gives a
  single rate with no silences — the thing that reads as a machine. There are
  four phrases here with different lengths and different rates, separated by
  pauses you can see, and the mouth SHAPE changes with them: wide on the emphatic
  phrases, half-open on the quiet ones. A shape that sits a phrase out waits for
  it with `hold.before`, since same-type sub-actions run in sequence.
- **Blinks are irregular.** Four of them, at gaps of 2.6 s, 4.1 s, 3.2 s and
  5.4 s. Evenly spaced blinks read as a metronome. Each lasts 150 ms — long
  enough to see, short enough not to look like a wince.
- **Two idle cycles that do not divide into each other.** The bubble breathes
  (scale, 7 cycles) and sways (rotation, 3 cycles) across the same window, so it
  never returns to the same pose on a beat. ⚠️ A rotation target must sit in
  `[0, 360)`, so the sway rocks from upright to 1.6° rather than either side of
  centre.

## Driving it from a voice instead

Every window is a share of `TALK_MS`. Declare an `audio` asset, replace that
constant with `<that asset>.duration`, and the rig re-times itself to the
recording — phrases, pauses, blinks and all. This example stays silent so that it
runs anywhere, and because a mouth driven by `cycles` is a convincing puppet, not
lip-sync: it matches the rhythm of speech, never the syllables.

## Files

| Path | What |
| ---- | ---- |
| `scene_01_presenter.yaml` | The document: the rig, the phrases and the type. |
| `resource/scene/avatar_layer.svg` | The presenter bubble — groups `presenter`, `eyes-open`, `eyes-closed`, `mouth-closed`, `mouth-mid`, `mouth-open`, stacked at the same place. |
| `resource/scene/pitch_text.svg` | The four lines of type, one actor each. |
| `resource/scene/backdrop.svg` | The background and the wordmark. |
| `resource/style/theme_dark.css` | Values only; each drawing owns its class-to-variable mapping. |
| `resource/template/main.html` | The HTML container. |

## Stacking the rig on another scene

The layer is transparent outside the bubble and shares the `0 0 1280 720`
viewBox, so it drops onto any scene of that size: declare `avatar_layer` as a
second scene asset and drive the same actors from that scene's beats. The bubble
occupies x 1036–1236, y 480–680 — everything else in the layer is empty.
