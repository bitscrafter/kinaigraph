# Presenter Avatar — Kinaigraph input package

Exported from the Claude Design session (`Presenter Avatar.dc.html`). A rigged
picture-in-picture presenter that delivers the Kinaigraph pitch, bottom-right
of a 1280×720 scene.

## Contents

| Path | What |
| ---- | ---- |
| `resources/avatar_layer.svg` | The rigged avatar layer — shared `0 0 1280 720` viewBox, actor groups: `presenter`, `eyes-open`, `eyes-closed`, `mouth-closed`, `mouth-mid`, `mouth-open`. Bubble themes via `kg-node-*`; character colors stay literal. |
| `resources/template/main.html` | Common HTML container (copied from microservices-flow). |
| `resources/css/theme_dark.css` | Dark theme (copied from microservices-flow). |
| `script/avatar_intro.txt` | Narration script — the Kinaigraph pitch. |
| `scene_00_tts_generation.yaml` | Generates `audio/avatar_intro.mp3` from the script. |
| `scene_avatar_intro.yaml` | The scene: fade in → talk (mouth pulses, breathing, two blinks) → fade out. All timing derived from `audio_intro.duration`. |

## Rendering

```bash
kinaigraph scene_00_tts_generation.yaml --outdir .
kinaigraph scene_avatar_intro.yaml      --outdir .
```

## How the talking works

`mouth-closed` (the smile) rests visible. `mouth-open` opacity-pulses 0→1 for
`TALK_CYCLES` cycles across the narration; `mouth-mid` pulses to 0.6 slightly
out of phase. Blinks are two 1-cycle pulses on `eyes-closed` placed with
`hold.before`. Tune `TALK_CYCLES` / `BREATHE_CYCLES` / `BLINK_MS` in `const`.

## Overlaying on another scene

Stack it like `chevron_layer.svg`: add `avatar_layer` as a second scene asset
in any 1280×720 scene (e.g. the microservices flow) and drive the same actors
from that scene's beats. The bubble sits at x 1036–1236, y 480–680.

## Caveat

The YAML is drafted against the schema + examples but has not been compiled.
Paste any compiler diagnostics back into the design session to get corrected
source.
