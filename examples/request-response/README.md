# Request/Response — One Packet, Two Authorings

A "Get User Profile" request walks a small system: the client calls the gateway, the gateway
checks the caller with auth, fetches the profile from the user service, and carries the
answer home. Six legs over three drawn connectors, each ridden twice.

What makes this example worth reading is that the **same beat is authored twice**, and
the two files disagree about something real. It is the closest thing in this repository
to a before-and-after.

## The scenes

| File | What it is |
| ---- | ---------- |
| `scene_01_flow.yaml` | Beat 1, authored with **action bookmarks** and `pace_by: distance`. The canonical one. |
| `scene_01_flow_with_orient_at_parent_action.yaml` | The same beat, authored with **six explicit `move` entries** and hand-measured leg lengths. |

The names say where `orient: auto` sits, because that is what the two structures force.
The canonical file rides one parent `move` carrying six bookmarked **sub-actions**, and
`orient` goes on each sub-action. The other has no parent at all — six independent
top-level **actions**, one per timeline entry, each carrying its own `orient`.

⚠️ Neither is the *third* spelling, `orient` on a parent that carries only `actions:` and
no `along` of its own. That parent has no tangent to read, writes a constant `0` rotation,
and the chevron never turns around on the return legs. It is an open bug in the engine,
not an authoring choice, and nothing in this example does it.

`scene_00_tts_generation.yaml` is synthesis-only. It generates the narration for all
three beats from the scripts under `resource/script/`. Run it once, before rendering, and again
whenever a script changes.

Beats 2 (*"the data store this diagram forgot"*) and 3 (*"re-themes from a single
line"*) exist here as **narration and resources** — `get_user_profile_v2.svg` adds the store
node, and `resource/style/` carries four stylesheets — but are not yet authored as scenes.
The [`microservices-flow`](../microservices-flow/) example shows both of those ideas
built out.

### The payloads are callouts, and their pointers move

Beat 1 shows the actual HTTP exchange. The request appears while the packet carries it
out — leg 1, client → gateway — and the response appears while the packet carries the
answer home on leg 6. Each is up for **exactly its own leg** and never shares the screen
with the other.

What makes them worth reading is that the box and the pointer are bound at **different
times**:

```yaml
pointer:
    target:
        anchor:
            asset: packet
            pos: center
            binding: live # re-resolves EVERY FRAME
at: # a literal coordinate — the box does not move
    x: CALLOUT_X
    y: REQUEST_CALLOUT_Y
```

`binding: live` on `pointer.target` re-aims the apex each frame, so the leader tracks the
packet down the connector while the box holds still. That split is the reason these are
annotations rather than artwork: a box drawn into the SVG could name the payload but
could not follow the thing carrying it, and a box that *travelled* with the packet would
be unreadable for the same reason a moving subtitle is.

`binding` normally cascades from `at` to `pointer.target`. Here `at` is a literal, which
carries no binding to inherit, so `live` is stated where it is meant. Naming
`pointer.target` explicitly is also **required** off a literal `at` — there is no anchor
for it to default from, and omitting it is a `MissingRequiredField`.

The two boxes sit on the sides their own packets travel. `lateral` has already put the
outbound pass above the connector and the return below it, so the request box is placed
above the line and the response box below, and neither leader ever crosses it.

Each callout's window is spelled as **actions in sequence inside one timeline entry** — a
fade in, a hold, a fade out — whose three durations sum to `leg1.duration` exactly:

```yaml
leg1.start:
    - callout_request:
          - show:
                duration: "leg1.duration * CALLOUT_FADE_SHARE"
                opacity: { from: 0, to: 1 }
                hold:
                    after: "leg1.duration * (1 - CALLOUT_FADE_SHARE * 2)"
          - show:
                duration: "leg1.duration * CALLOUT_FADE_SHARE"
                opacity: { from: 1, to: 0 }
```

The fade is a **share of the leg**, not a span in milliseconds. Two fades are spent inside
one leg's window and the hold is what is left, so a fixed fade would go negative on any
leg shorter than twice it — and a leg's length comes from `narration.duration`. The three
windows are `SHARE + (1 - 2·SHARE) + SHARE`, which is 1 at every narration length.

Keying the fade-out at `leg1.end` instead would *start* it there and let the box linger a
fade into leg 2. Only `scene_01_flow.yaml` carries the callouts: naming the window
`leg1.duration` costs nothing there, where the leg is already addressable, while
`scene_01_flow_with_orient_at_parent_action.yaml` would have to spend another
hand-measured constant on it.

⚠️ **The payload text is inlined as `content:`, not read from `resource/text/`.** The same
two payloads are committed at `resource/text/get_user_profile_request.txt` and
`…_response.txt`, and a `type: text` asset does accept a `file:` — but no layer reads it,
so a note sourced from a file renders an **empty box**. Until that is fixed the `.txt`
files are the authority and the inlined copies must be kept in agreement with them.

### The store callout is a `note` annotation, not artwork

`get_user_profile_v2.svg` draws the diagram and nothing else. The callout that names the new
store is declared by the **document**, as a `note` annotation — a box, an auto-aimed
pointer and its own fade, authored in YAML. Keeping it out of the artwork is what lets the
same scene be reused by a beat that does not want the callout at all.

Paste this into the beat-2 document when it is authored; it is verified against
`get_user_profile_v2.svg` and reproduces the callout the SVG used to carry:

```yaml
defs:
    assets:
        data_store:
            type: "actor"
            part_of: diagram          # the scene asset holding get_user_profile_v2.svg
            id: data-store
        store_caption:
            type: "text"
            content: |
                now with a
                data store
            font_family: 'Arial, "Liberation Sans", Helvetica, sans-serif'
            font_size: 13
            # A literal, necessarily: css() reads a style selected on a scene or
            # template, and no style is in scope inside defs. This is blueprint's
            # --title-text-color; re-theming the note's TEXT means editing it here.
            font_color: "#eafaff"

animation:
    annotations:
        store_note:
            note:
                text: store_caption
                shape:
                    rect:
                        width: 100
                        height: 40
                padding: 6
                align: center
                pointer:
                    target:                    # the fork aims itself; `side` is auto-only
                        anchor:
                            asset: data_store
                            pos: right
            at:
                anchor:
                    asset: data_store
                    pos: center
                    dx: 80
                    dy: -20
            origin: top_left
            fill: 'css("callout-fill-color")'  # inside `animation`, so css() resolves
    timeline:
        0:
            - store_note:
                  - show:
                        opacity:
                            from: 0
                            to: 1
                        duration: 800
```

Two limits worth knowing before you extend it. The old artwork set the caption in
**italic**; a `type: text` asset takes only `content` / `file` / `font_family` /
`font_size` / `font_color`, so italic is not available. And a note's box tracks the
attached stylesheet through `css()` while its text colour cannot — which is why
`--callout-fill-color` and `--callout-stroke-color` are theme variables and a
`--callout-text-color` is not. Every note in the example inherits that split: each one's
text colour is a literal on its `type: text` asset, tracking `theme_blueprint.css`.

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
- **A fixed box with a moving pointer.** `binding: live` on a callout's `pointer.target`
  re-resolves the apex every frame, so the two payload callouts keep aiming at the packet
  as it travels while their boxes stay put and stay readable.
- **Why six entries rather than one `move` with six sub-actions:** a sub-action was not
  addressable from the timeline when `scene_01_flow_with_orient_at_parent_action.yaml`
  was written, so nothing could hang a badge pulse on a leg boundary. Six entries buy that addressability; the cost is
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
ratio of 1.278 where the true arc ratio is 1.381 — so in
`scene_01_flow_with_orient_at_parent_action.yaml` the packet **speeds up and slows down at
each leg boundary**. That is exactly what
`pace_by: distance` exists to prevent, and it was silently not happening.

`scene_01_flow.yaml` was also written *before* the `action-bookmarks`
feature was built, as a check of the design against a real document rather than a sketch.
The feature shipped and the file needed no change to become valid: the spelling it was
written against is the spelling that shipped.

## Layout

```text
scene_00_tts_generation.yaml                       narration synthesis (run first)
scene_01_flow.yaml                                 beat 1, paced by distance
scene_01_flow_with_orient_at_parent_action.yaml    beat 1, hand-timed
resource/
  scene/get_user_profile_v1.svg                       the system, as drawn
  scene/get_user_profile_v2.svg                       the same, plus the shared data store
  scene/chevron_layer.svg                          the packet marker
  script/                                          the three narration lines
  style/theme_*.css                                four skins (dark, light, pastel, blueprint)
  template/main.html                               the page the scene is composed into
  text/                                            the two HTTP payloads beat 1 quotes
```

## Rendering it

You need Kinaigraph installed — see the [install instructions](../../README.md#install).
Run from this directory:

```sh
kinaigraph scene_00_tts_generation.yaml --outdir ./out    # once, to synthesize narration
kinaigraph scene_01_flow.yaml --outdir ./out
```

Render `scene_01_flow_with_orient_at_parent_action.yaml` too if you want to see the
difference the table above describes.

Paths inside a scene resolve against the scene file's own folder — which is this
directory — so `file:` values need no `../`. Outputs resolve against whatever you pass as
`--outdir`.

Synthesis calls a text-to-speech provider and needs `ELEVENLABS_API_KEY` in the
environment. Every run costs credits, which is why it is a separate file: re-rendering a
beat must never re-synthesize audio that did not change.
