# Kinaigraph

**A declarative language for animation and motion graphics.** You author scenes in YAML that bring together your SVG artwork and narration scripts, declaring how they work together and what happens when. Kinaigraph does the tedious, exacting work: timing motion to narration, interpolating every frame, and keeping audio and video in sync — then renders the scene as a video file or live playback in the browser.

This repository is the public home for Kinaigraph. It will hold the **examples**, the
**binaries**, and the **documentation**.

## Status — pre-release (alpha)

Kinaigraph is early software, rolling out in stages:

- ✅ **Examples** — complete, compiler-validated example projects. Available now (below).
- 🔜 **Binaries** — the Kinaigraph command-line tool that renders the examples. Coming in the next few weeks.
- 🔜 **Documentation** — a guide to authoring with Kinaigraph. Coming later.

Until the binary ships, the examples are here to read: they show what authoring in
Kinaigraph looks like, even though you can't render them yourself just yet.

**What ends the alpha.** The `-alpha` is dropped when the authoring language goes one full
release without a change that stops an existing example in this repository from rendering.
The condition is about the **language**, not the tool: what an alpha warns you about is
that a scene you write may need editing to keep working across a release. The examples
below are the measure — every release renders all of them end to end — so this is
something you can check rather than something we judge.

## Examples

Each example is a set of YAML **scene** files plus its resources — SVG artwork, CSS
themes, and narration scripts. Kinaigraph compiles a scene and renders it to an MP4
(and can also play it live in the browser).

| Example                                                                                                | What it shows                                                                                                                                                                                               |
| ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`microservices-flow`](examples/microservices-flow/)                                                   | A narrated walkthrough of a request moving through a microservices architecture — animation paced to narration, animated diagrams, and compile-time theming (the same scene re-rendered in light and dark). |
| [`life-lessons-en`](examples/life-lessons-en/) &middot; [`life-lessons-es`](examples/life-lessons-es/) | Kinetic typography — quotes that fade in over paper texture, paced to spoken narration. English and Spanish.                                                                                                |

Narration audio is generated from the scripts via text-to-speech, so a scene reads
its timing from the spoken lines. See each example's folder for its specific layout.

## License

Kinaigraph is pre-release software provided **as is**, for **non-commercial use**,
with no warranty and no support — use it at your own risk. The example projects may be
copied and modified for non-commercial purposes, with attribution.

See [LICENSE](LICENSE) for the full terms.

Copyright © 2026 José Luis Ríos Treviño. All rights reserved.
