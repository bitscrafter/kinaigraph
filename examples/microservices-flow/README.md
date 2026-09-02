# Microservices Flow — Capabilities Showcase

A five-scene narrated walkthrough that documents a request through a small
microservices architecture — and, in doing so, demonstrates several kinaigraph
capabilities one at a time. Each scene adds one idea; together they tell a single
story (set up the flow → narrate it → evolve it → re-skin it → recap).

## The five scenes

| Scene | File | Beat | Capability shown |
| ----- | ---- | ---- | ---------------- |
| 1 | `scene_01_intro.yaml` | High-level overview; one narration sets the whole pace; the chevron makes a single sweep | SVG layer stacking; **animation paced by narration** |
| 2 | `scene_02_step_flow.yaml` | The detailed flow — each step narrated, each service pulses on arrival | **Audio-fitted motion**: each chevron movement is timed from that shot's audio duration |
| 3 | `scene_03_add_datastore.yaml` | "We forgot a shared data store" — swap in `overview_v2.svg` (one node + two legs), re-run; a subtitle and callout fade in | **Structural evolution is a tiny edit** + animated **text overlay**; the new leg's timing auto-fits its narration |
| 4 | `scene_04_retheme.yaml` | The same flow re-rendered in light mode | **Compile-time theming** — the only authored diff is `style.file:` (`theme_light.css` vs `theme_dark.css`) |
| 5 | `scene_05_conclusion.yaml` | A recap card whose bullets fade in across the narration | Sequenced **text animation** (`show.opacity-range` + `hold.at-start`) |

`scene_00_tts_generation.yaml` is synthesis-only — it generates the ten narration
MP3s under `audio/` from the matching scripts under `script/`. Run it once (or
whenever a script changes) before rendering.

## How the capabilities show up

- **Narration-driven timing (Scenes 1, 2, 3).** Every motion duration is an
  expression over a narration's `.duration`, and phases are chained bookmarks
  (`audio_intro.end @ audio_client_to_gateway`), so the *total* video length and
  every step both follow the narration. Change a script, regenerate TTS, re-render —
  the motion re-fits with no manual timing edits. Scene 2 makes this explicit
  per-step; Scene 3 shows it applying to *freshly added* structure (the store leg).
- **Structural evolution (Scene 3).** `overview_v2.svg` is `overview_v1.svg` plus one
  `data-store` node and two legs (`link-auth-store`, `link-store-user`) — the Auth and
  User services share the store. Adding the step to the flow is a couple of timeline
  lines, and re-running the binary is the whole "deploy."
- **Theming (Scene 4).** Both dark and light variants attach a standalone `style:`
  asset to the template via `template.style: style`; the one-line difference is that
  asset's `file:` value.
- **Text overlay / animation (Scenes 3, 5).** Titles, callouts and recap bullets are
  plain SVG `<text>` elements faded in with `show.opacity-range`, sequenced with
  `hold.at-start`. Text only — no logo.

## Files

| Path | What |
| ---- | ---- |
| `resources/diagram/overview_v1.svg` | Base architecture (Client + Gateway + Auth + User). Scenes 1–2. |
| `resources/diagram/overview_v2.svg` | `overview_v1` + `data-store` + `link-auth-store` + `link-store-user` + `subtitle`/`store-callout` annotations. Scenes 3–4. |
| `resources/diagram/chevron_layer.svg` | Top-stacked layer carrying the animating `chevron-packet`. |
| `resources/diagram/conclusion.svg` | Recap card (four `bullet-*` rows + `wordmark`). Scene 5. |
| `resources/template/main.html` | Common HTML container (carries the `KINAI_*` placeholders). |
| `resources/css/theme_dark.css` / `theme_light.css` | The two CSS-custom-property sets. |
| `script/` | Source narration text per shot. |
| `audio/` | TTS-generated narration MP3s (output of `scene_00`). |
| `video/` | Rendered MP4s. |

(`resources/diagram/diff_panel.svg` is a standalone One-Dark code-panel asset kept
for reuse; it is not part of the current five-scene arc.)

## Rendering

```bash
# 1) Generate audio once (only when scripts change).
kinaigraph scene_00_tts_generation.yaml --outdir .

# 2) Render each scene end-to-end (produces the per-scene *_composition.mp4).
kinaigraph scene_01_intro.yaml       --outdir .
kinaigraph scene_02_step_flow.yaml   --outdir .
kinaigraph scene_03_add_datastore.yaml   --outdir .
kinaigraph scene_04_retheme.yaml     --outdir .
kinaigraph scene_05_conclusion.yaml  --outdir .

# 3) Stitch the five composition outputs into the final video.
kinaigraph scene_06_stitch.yaml      --outdir .
```

Per scene the binary produces `<scene>_animation.mp4` (frames only) and
`<scene>_composition.mp4` (audio mixed). The headline deliverable is a single
stitched video, `microservices_flow_full.mp4`, authored as `scene_06_stitch.yaml`
— a `roll` of the five composition outputs (Scene 1 → … → Scene 5). It requires
each scene's `_composition.mp4` to exist first.
