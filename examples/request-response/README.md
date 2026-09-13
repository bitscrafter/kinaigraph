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

| `scene_02_store.yaml` | Beat 2 — the shared store is added, and the packet rides the new leg. |

| `scene_03_theme.yaml` | Beat 3 — the same diagram and route in two themes, side by side. |
| `scene_04_stitch.yaml` | The three beats in order, each carrying its own narration. |

### Beat 3 is side by side because theming is compile-time

`css()` resolves during compilation and the runtime never re-reads a variable, so there
is no such thing as animating from one theme to another. Two compiled results shown
together is not a stylistic choice — it is the only honest picture of the property. A cut
would make the viewer compare against memory, which is what a compile-time claim should
least have to rely on.

Both halves run the same six-leg route for the same `TRAVEL_MS`. Measured on the render,
the two packets stay within **1.6 px of each other at worst, typically under 1** — a
viewer watching for a difference in timing will not find one.

Three things the beat gives up, each for its own reason:

- ⛔ **No `css()`, and therefore no pulses.** `css()` bakes one value per animation
  section from the default-scope scene and never looks at which scene an entry targets,
  so under a grid a `css()`-driven colour comes out identical in both cells while
  everything around it re-themes. Beat 1's badge pulses all read
  `css("pulse-stroke-color")`, so they are dropped rather than frozen.
- ⚠️ **No payload callouts.** A cell is 1920×540 and the 1280×720 diagram letterboxes
  into it at 0.75; beat 1's seventeen-line response box would take a third of the cell at
  text too small to read.
- ⚠️ **Six SVG copies.** Two scene assets may not share a root `<svg id>`, so each cell
  needs its own diagram and chevron layer. The `*_top` / `*_bottom` files differ from
  their originals by that id alone — re-derive them rather than editing.

**The source panels are authored at 1920×540 — the cell's own aspect** — so they fill
without letterboxing and one unit in them is one capture pixel. That is what lets their
text render at full size beside a diagram sitting at 0.75, and it gives per-word control
(`<tspan>`) that a `note` cannot: a note takes one `font_color` for its whole text, so
the amber on the stylesheet name would be unavailable.

⚠️ **Their key and value columns are set by explicit `x` on each `tspan`, not by spaces.**
XML collapses runs of whitespace and drops leading whitespace in a text node, so an
indent typed into the content renders flush and a padded `cell:  ` collapses to one
space. Spaces cannot hold a column here.

Each panel shows its own cell's `context.scenes[]` entry, so the two differ in the three
places those entries genuinely differ — the asset, the stylesheet and the cell. The
stylesheet is the one picked out in amber, because it is the line the beat is about.

Their slab and text are off-palette, because the panel is the document talking about
itself. Their full-bleed **ground** is themed and has to be — without it the page shows
through as white bars where the diagram letterboxes. ⚠️ And they are declared **first**
in `defs.assets`: declaration order is render order, and an opaque ground declared after
the diagram paints straight over it.

⛔ **Both stylesheets declare their variables twice** — once at `:root`, once under this
document's asset names. A grid puts both scenes in one document and `:root` is one
element per document, so without the second declaration the last stylesheet emitted
paints the whole frame. The stylesheets carry beat 3's asset names as a result, a
coupling the compiler could remove; filed upstream as
`grid-cells-cannot-carry-one-theme-each`.

### Beat 2's claim is checkable by eye

`get_user_profile_v2.svg` is `get_user_profile_v1.svg` — the file beat 1 rides — **plus
the `data-store` group and the `link-store-user` path, and nothing else**. Every other
node, link, badge and CSS rule is byte-identical, which is why the diagram does not move
at the cut between the beats. A viewer who suspects the two are different drawings can
watch for a jump and not find one.

⚠️ That property is load-bearing and easy to lose. **v2 is derived from v1** — re-derive
it rather than hand-editing it, or the beat starts asserting something the render no
longer shows. (Badge 4 sits *below* the user service in both files for the same reason:
the store needs the gap above it, and the two diagrams must differ by the store alone.)

The store is not decoration — the packet rides the new leg. `link-store-user` is only
35 px of visible line, because the two nodes really are that close, so the dip down and
back is quick. That is what a local lookup should look like, and it is a consequence of
the drawing rather than a duration anyone chose: `pace_by: distance` splits the beat's
travel by arc length, so the two long legs take most of it by themselves.

⛔ **Beat 2 does not change the theme.** Re-skinning is beat 3's subject, and a beat that
changed the structure *and* the palette at one cut would leave a viewer unable to
attribute either. The force of "one node, one link" is that everything else held still.

### The payloads are callouts, and their pointers move

Beat 1 shows the actual HTTP exchange — **five callouts over six legs**, each up while the
packet carries the bytes it quotes. The client request rides out on leg 1, the authz
exchange occupies legs 2 and 3, the gateway's own request to the user service leg 4, and
the profile body comes home across legs 5 and 6.

Four of the five are up for **exactly their own leg** and never share the screen. The
fifth is the exception, and it is the one worth watching: the body the user service
returns and the body the gateway hands the client are the same bytes, so **one box is held
across both legs** rather than drawn twice. The pointer swings from the user link to the
client link while the content never changes — which SHOWS the gateway not touching it,
where a second box could only have asserted it.

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

**The payload text is read from `resource/text/`, not inlined.** Each callout's
`type: text` asset names its payload with `file:`; the compiler reads the file at Pass 3
and inlines the contents, so the `.txt` is the single authority and there is no second
copy to keep in agreement with it. A file it cannot read — absent, unreadable, not
UTF-8 — is a compilation error rather than a silently empty box.

⚠️ **The payloads are indented with spaces, not tabs**, and that is a rendering
constraint rather than a style choice: a tab inside SVG text has no defined advance
width, so the browser would set the JSON's shape at its own discretion.

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
  re-resolves the apex every frame, so each payload callout keeps aiming at the packet
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
scene_02_store.yaml                                beat 2, the store arrives
scene_03_theme.yaml                                beat 3, two themes at once
scene_04_stitch.yaml                               the three beats, with narration
resource/
  scene/get_user_profile_v1.svg                       the system, as drawn
  scene/get_user_profile_v2.svg                       the same, plus the shared data store
  scene/chevron_layer.svg                          the packet marker
  script/                                          the three narration lines
  style/theme_*.css                                four skins (dark, light, pastel, blueprint)
  template/main.html                               the page the scene is composed into
  text/                                            the five HTTP payloads beat 1 quotes
```

## Rendering it

You need Kinaigraph installed — see the [install instructions](../../README.md#install).
Run from this directory:

```sh
kinaigraph scene_00_tts_generation.yaml    # once, to synthesize narration
kinaigraph scene_01_flow.yaml
kinaigraph scene_02_store.yaml
kinaigraph scene_03_theme.yaml
kinaigraph scene_04_stitch.yaml
```

⛔ **Do not pass `--outdir` here.** The beats declare their capture as
`./resource/video/scene_0N.mp4` and the stitch reads those same paths, but `--outdir`
rebases only the OUTPUT — the beats' clips land under it while the stitch still resolves
its inputs beside the document. The stitch then refuses with `no file at …`, naming three
paths that were just written somewhere else.

The beats capture **intermediates** into `resource/video/`; `scene_04_stitch.yaml` is the
only document that writes beside the document, and `request_response.mp4` is the file to
watch. The finished piece runs about **69 s**.

### The stitch carries no authored offset

Every beat sizes *itself* to its own line — each spends `narration.duration` minus its
margins on the walk — so a rendered clip comes out **exactly as long as the line that
narrates it**. Measured across the three: 34.67 / 34.64, 17.30 / 17.28, 16.60 / 16.58.

Mixing each line onto its own clip at offset zero therefore lands the voice against the
pictures it describes, with nothing to keep in step by hand. The timestamps chain by
**bookmark** (`flow_bk.end`, `store_bk.end`) rather than by number, so the offsets are
read from the clips' own probed durations: re-record a line, re-render that beat, and
everything after it moves by itself.

Render `scene_01_flow_with_orient_at_parent_action.yaml` too if you want to see the
difference the table above describes.

Paths inside a scene resolve against the scene file's own folder — which is this
directory — so `file:` values need no `../`. **Outputs resolve against the document's own
folder too, unless you pass `--outdir`** — and this example relies on that default, which
is what keeps a beat's capture and the stitch's reading of it the same path.

Synthesis calls a text-to-speech provider and needs `ELEVENLABS_API_KEY` in the
environment. Every run costs credits, which is why it is a separate file: re-rendering a
beat must never re-synthesize audio that did not change.
