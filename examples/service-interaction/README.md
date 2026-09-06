# Service Interaction — One Packet, Two Authorings

A "Get User Info" request walks a small system: the client calls the gateway, the gateway
checks the caller with auth, fetches the profile from the user service, and carries the
answer home. Six legs over three drawn connectors, each ridden twice.

What makes this example worth reading is that the **same beat is authored twice**, and
the two files disagree about something real. It is the closest thing in this repository
to a before-and-after.

## The scenes

| File | What it is |
| ---- | ---------- |
| `scene_01_flow.yaml` | Beat 1, authored with **six explicit `move` entries** and hand-measured leg lengths. |
| `scene_01_flow_with_bookmarks.yaml` | The same beat, authored with **action bookmarks** and `pace_by: distance`. Shorter — and more correct. |

`scene_00_tts_generation.yaml` is synthesis-only. It generates the narration for all
three beats from the scripts under `script/`. Run it once, before rendering, and again
whenever a script changes.

Beats 2 (*"the data store this diagram forgot"*) and 3 (*"re-themes from a single
line"*) exist here as **narration and resources** — `get_user_info_v2.svg` adds the store
node, and `resources/css/` carries four stylesheets — but are not yet authored as scenes.
The [`microservices-flow`](../microservices-flow/) example shows both of those ideas
built out.

## What it shows

- **The packet rides the links themselves.** `move … along` names the `<path>` the
  diagram draws, so the route travelled and the route drawn cannot drift apart. Redraw a
  connector and the animation follows it.
- **One packet, not one per direction.** `orient: auto` turns the marker onto each leg's
  heading, which is why the marker layer's pre-drawn left/up/down chevrons go unused.
- **`lateral` puts the return trip in its own lane.** Outbound and return share a
  connector and would otherwise retrace identical pixels. A side is relative to the
  **direction of travel**, so `side: left` on every leg automatically places the return
  on the opposite side of the line from the outbound pass. One keyword; no per-leg
  bookkeeping.
- **Why six entries rather than one `move` with six sub-actions:** a sub-action was not
  addressable from the timeline when `scene_01_flow.yaml` was written, so nothing could
  hang a badge pulse on a leg boundary. Six entries buy that addressability; the cost is
  six hand-measured lengths.

### The disagreement, and why the shorter file is the better one

Both files put the packet on the road at 350 ms and take it off at 13442.7 ms — the
envelope matches to a tenth of a millisecond. The **leg boundaries** do not:

| leg | hand-measured | compiler-measured |
| --- | --- | --- |
| 1 & 6 | 2552.2 ms | 2674.2 ms (372.0 px) |
| 2–5 | 1997.1 ms | 1936.1 ms (269.3 px) |

The compiler's numbers hold **one speed** across every leg: 372.0 / 2674.2 and
269.3 / 1936.1 are both 0.1391 px/ms. The hand-measured constants give leg 1 a length
ratio of 1.278 where the true arc ratio is 1.381 — so in `scene_01_flow.yaml` the packet
**speeds up and slows down at each leg boundary**. That is exactly what
`pace_by: distance` exists to prevent, and it was silently not happening.

`scene_01_flow_with_bookmarks.yaml` was also written *before* the `action-bookmarks`
feature was built, as a check of the design against a real document rather than a sketch.
The feature shipped and the file needed no change to become valid: the spelling it was
written against is the spelling that shipped.

## Layout

```text
scene_00_tts_generation.yaml      narration synthesis (run first)
scene_01_flow.yaml                beat 1, hand-timed
scene_01_flow_with_bookmarks.yaml beat 1, paced by distance
script/                           the three narration lines
resources/
  diagram/get_user_info_v1.svg    the system, as drawn
  diagram/get_user_info_v2.svg    the same, plus the shared data store
  diagram/chevron_layer.svg       the packet marker
  css/theme_*.css                 four skins (dark, light, pastel, blueprint)
  template/main.html              the page the scene is composed into
```

## Rendering it

You need Kinaigraph installed — see the [install instructions](../../README.md#install).
Run from this directory:

```sh
kinaigraph scene_00_tts_generation.yaml --outdir ./out    # once, to synthesize narration
kinaigraph scene_01_flow_with_bookmarks.yaml --outdir ./out
```

Render `scene_01_flow.yaml` too if you want to see the difference the table above
describes.

Paths inside a scene resolve against the scene file's own folder — which is this
directory — so `file:` values need no `../`. Outputs resolve against whatever you pass as
`--outdir`.

Synthesis calls a text-to-speech provider and needs `ELEVENLABS_API_KEY` in the
environment. Every run costs credits, which is why it is a separate file: re-rendering a
beat must never re-synthesize audio that did not change.
