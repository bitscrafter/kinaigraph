# Migrating `differentiators` from the precursor DSL

Source: `/Users/luis/_Dev/project/animation-dsl/examples/differentiators`
(4 scenes + TTS + composition, 1390 lines, 1920x1080, 192.33 s rendered)

## The translation table — derived by compiling, not by reading

| precursor | current | notes |
| --- | --- | --- |
| `type: "diagram"` | `type: "scene"` | |
| `roles: [primary]` | *(retired)* | the primary scene is now `animation.defaults.assets.scene` |
| `type: "engine"` asset | *(retired)* | the runtime is no longer declared per document |
| `defs.groups:` | `defs.assets.<n>: { type: "group", members: [...] }` | both block-list and inline-list forms appear in the source |
| `opacity-range: {from, to}` | `opacity: {from, to}` | the range moved onto the property it ranges |
| `play: {}` on a video | `roll:` | |
| `play: {}` on an audio | `mix: { asset: { name: … } }` | ⚠️ a mix RIDES a roll — it is a sibling action on the video entry, not an entry of its own |
| `animation.<bk>.<prop>` | `animation::<bk>.<prop>` | cross-section bookmarks take the `::` qualifier |
| `a-hyphenated-name` | `a_hyphenated_name` | hyphens are not legal in identifiers: asset names, group names, bookmark labels, timeline keys |

## Two more classes the first pass did not reach

| | |
| --- | --- |
| **The template predates the current tokens** | the precursor's `animation-template.html` lacks `KINAI_STYLE::PLACEHOLDER`, `KINAI_BYTECODE::PLACEHOLDER` and the rest. Use the suite's `main.html` — already copied in. |
| **SVG element ids vs identifiers** | ids MAY carry hyphens; asset names, group names, bookmark labels and timeline keys MAY NOT. The precursor referenced ids bare from the timeline, so the two collide. ✅ **RESOLVED HERE**: 145 ids across the four SVGs are converted to underscores, so bare references stay legal and ~100 bridging actor declarations are avoided. |

## ⚠️ The YAML in this directory is the UNMODIFIED SOURCE

Translate it fresh. My own regex pass was restored away after it did three kinds of
damage, each silent until the compiler or a line count caught it:

- a `play:` → `roll:` substitution collapsed the newline, producing
  `- video_x:          - roll:` on one line;
- a timeline rebuild anchored on `timeline:` matched the ANIMATION section in
  `scene_04` and replaced 300 lines of it;
- the hyphen sweep was applied to SVG id references as well as identifiers.

`scene_03` lost 43 lines and `scene_04` its whole animation section before the line
counts exposed it. **Translate with a parser, or by hand per file with the table above —
not with regexes over whole documents.**

## What was open at 22 errors in 5 classes

1. **14 × `show`/`pulse` with no visual property.** The precursor allowed
   `show: { hold: N }` as a pure delay; the current language requires one of
   `opacity` / `scale` / `rotation` / `reveal` / `fill` / `stroke` / `stroke_width`.
   Each site needs a decision: carry the previous value explicitly, or fold the hold
   into the neighbouring action's `hold.after`.
2. **2 × groups landed in `const:`.** My inline-list rewrite matched `const` entries in
   `scene_04`. Scope the rewrite to the `assets:` block.
3. **1 × YAML shape** in `scene_03_benefits` around line 139.
4. **5 × `animation.timeline.<bk>.start` keys** in `scene_04` — a three-segment form the
   `::` rewrite did not match.
5. **1 × unrecognised action** — the last `play:` not covered by the video/audio patterns.

## Decisions still owed

- ~~The name~~ **DECIDED: `why-a-language`.**
- ~~Length~~ **DECIDED: migrate as-is. This is the FULL version**; a shorter cut may
  follow once it renders, and would be a second deliverable rather than a replacement.
- **The narration offset.** The precursor started each line at an `animation::audio_in`
  bookmark *inside* the clip. The current stitch idiom mixes at offset zero because each
  beat sizes itself to its own line. Reconciling these is a design choice, not a
  translation: either give the mix a `span.from`, or re-shape each scene to its line the
  way request-response and wave-anatomy do.
- **Standards.** The precursor's theme has not been audited yet — expect the same
  findings as elsewhere (prefix, dead variables, class rules in the stylesheet, fonts).
