# Migrating `differentiators` from the precursor DSL — DONE

Source: `/Users/luis/_Dev/project/animation-dsl/examples/differentiators`
(4 scenes + TTS + composition, 1920x1080).

✅ **Complete.** Every document compiles, every scene renders, and the two stitch
documents write `./why_a_language_brief.mp4` and `./why_a_language_full.mp4`.
What the example *is* lives in [`README.md`](README.md); this file is the record
of how it got here and what the translation cost.

## The translation table — derived by compiling, not by reading

| precursor | current | notes |
| --- | --- | --- |
| `type: "diagram"` | `type: "scene"` | |
| `roles: [primary]` | *(retired)* | the primary scene is now `animation.defaults.assets.scene` |
| `type: "engine"` asset | *(retired)* | the runtime is no longer declared per document |
| `defs.groups:` | `defs.assets.<n>: { type: "group", members: [...] }` | both block-list and inline-list forms appear in the source |
| `opacity-range: {from, to}` | `opacity: {from, to}` | the range moved onto the property it ranges |
| `play: {}` on a video | `roll:` | |
| `play: {}` on an audio | `mix: { span: { from: … }, asset: … }` | ⚠️ a mix RIDES a roll — a sibling action on the video entry, not an entry of its own |
| `animation.timeline.<bk>.start:` *as a timestamp key* | `span.from: "animation::<bk>.start"` *on the mix* | the three-segment form the first pass's `::` rewrite never matched |
| `a-hyphenated-name` | `a_hyphenated_name` | asset names, group names, bookmark labels, timeline keys |
| `generation:` | `synthesis:` | |
| `output:` *on a tts entry* | `export:` | |
| `hold: N` | `hold: { after: N }` | |
| `x: "<id>:left"` | `restore:` *(no checkpoint)* | the precursor's way of saying "back where you were drawn"; baseline restore says it directly |
| `show: { hold: N }` | `show: { opacity: 1, hold: { after: N } }` | a `show` must now say what it shows; each of these was a pure pad, so it restates the value it is already at |
| `pulse: { duration, cycles }` | `pulse: { …, scale: { amplitude: N } }` | same rule on `pulse`. `amplitude` is an `add` contribution, so it composes with the `restore` running beside it instead of racing it |

## Two classes the first pass did not reach

|     |     |
| --- | --- |
| **The template predates the current tokens** | the precursor's `animation-template.html` lacks `KINAI_STYLE::PLACEHOLDER`, `KINAI_BYTECODE::PLACEHOLDER` and the rest. The suite's `main.html` is used instead. |
| **SVG element ids vs identifiers** | ids MAY carry hyphens; asset names, group names, bookmark labels and timeline keys MAY NOT. The precursor referenced ids bare from the timeline, so the two collide. ✅ **RESOLVED**: every hyphenated id in the four drawings — 86 occurrences, 76 distinct — is an underscore, so bare references stay legal and a bridging actor declaration per element is avoided. |

⚠️ **Scene 2's `trad-N` became `traditional_N`, not `trad_N`** — the one id in the
four drawings that is not a mechanical hyphen-to-underscore of the precursor's.
In the precursor, drawing and timeline agreed on `trad-1`; here the drawing spells
it out, so the timeline had to follow. Diffing the two id sets is what surfaced
it, and nothing else would have: the abbreviation is legal, so a translation that
carried `trad_1` across would have compiled and simply animated nothing.

## What the migration had to decide, not translate

- **The narration offset.** ✅ Each scene keeps its own `composition` and mixes its
  own lines at the bookmarks inside its own clip, each with an explicit
  `span.from`. See README — the short version is that `request-response`'s
  offset-free idiom needs one line per clip and three of these four scenes carry
  several.
- **The property-less `show` and `pulse`.** ✅ Counted in the source: 5 `show`s and
  10 `pulse`s. The five were pure pads and are now `opacity: 1` carrying a
  `hold.after` — the value the element is already at, restated so the hold has
  something to ride. The ten are scene 2's box pulses, which had a duration and a
  cycle count and nothing to oscillate; they now swell `scale` by an amplitude.
- **`biz_dim` versus the final fade.** ✅ Deleted. The precursor wrote circle_biz
  `1.0 -> 0.5` and the ring group `0.5 -> 0` from the same instant, which the
  current language rejects as a `set`/`set` race (§6.7.2) and which nothing could
  have rendered coherently. The fade now uses `opacity: 0` with no `from`.
- **The teaser.** ✅ Removed. The precursor had already commented its sequence
  out; the artwork, the script and the recording are gone too, since it promised
  a next episode that does not exist. Its removal also collapsed scene 4's
  colour/metrics class split, which existed only to give the teaser's two lines
  one size in two colours.
- **Standards.** ✅ Theme rework done: values moved out of the four SVGs into
  `theme_dark.css` / `theme_light.css`, mapping left behind with fallbacks, no
  prefixes, no dead variables, no `@media`-only definitions, Arial stack.

## Dead weight removed on the way through

- `--utilities-opacity` — declared in scene 2, read nowhere.
- `--global-opacity` and the four group-opacity rules that read it — the timeline
  owns opacity, and in three of the four scenes the variable was `1.0` anyway.
- `--teaser-accent` and the `.teaser-accent` / `.teaser-title` / `.benefit-group`
  rules — no element carried any of them.
- `pulseDuration` (scene 2), `fadeOutDuration` (scene 3), `teaserFadeOut` and six
  commented-out consts (scene 4) — declared, never referenced.
- `all-circle-text` (scene 4) — a group declared and never used.
- The `body` and `.container` rules in the stylesheet — page layout is the
  compiler's, and no other example's theme sets it.

## After the migration — the content refresh

✅ The migration landed the precursor's argument unchanged. A separate pass then
revised it, because the ideas were written against the previous language and had
stopped describing this one:

- **Absolutes softened.** Claims about other people's technology are what ages;
  claims about Kinaigraph are not. "Automated variations are impossible" became
  "hard to come by", "fundamentally unpredictable" became "today its output is
  hard to predict", and `Trial-Error Due to Unpredictable` became
  `Trial & Error / Uncertain Output`. The determinism claim was deliberately left
  sharp — it is a guarantee the language makes by design.
- **Five challenges and three benefits added**, chosen by one rule: every
  challenge on screen must have an answer on screen. Two of the precursor's
  challenges had none (syncing, usage costs) and one benefit answered nothing
  anyone had named (consistent styling).
- **AI reframed from rival to input.** `Binary Output / No Source` against
  `AI-Authorable / LLM Writes the Source` — a generated video is a terminal
  artefact; a Kinaigraph document is source a model can write and a human can
  review.
- **Scene 1 renamed** from `intro` to `premise`, and its heading from
  *Why Explainer Videos?* to *Why Kinaigraph?*
- Seven of the thirteen lines were re-recorded for the above. The run was scoped
  to those seven by a temporary synthesis document, since
  `synthesis.context.status` is section-wide and a plain re-run bills all
  thirteen.

## Then it was cut twice

✅ The revised argument turned out to run 3:57, and the enumerating scenes were
1:37 and 1:35 of it. Measured, **the animation was not the problem**: 237.7 s of
video held 221.8 s of speech, so every margin, pad, fade and hold in four scenes
came to 15.9 s — under 7%. Only the script could give the time back.

So the example now ships **two cuts**: the **full** one, which names every box
aloud, and a **brief** one at 2:28, whose voice names a CATEGORY and lets the
boxes enumerate it. Same drawings, same theme, same timeline shapes. Scenes 1
and 4 are identical in both and rendered once.

Two defects surfaced while building the category waves, both of which had been
shipping in the full cut:

- ⛔ **The shared band parked all seven boxes at one offstage y**, where the two
  rows overlap by 120 px each — so row B sat on top of row A's labels for the
  whole slide. The rows now park 160 apart, the same gap they keep on screen.
- ⛔ **`Variations Resist` and `Re-Author` overlapped by 120 px and travelled
  together.** The fix was not to swap two boxes — computed, that makes it worse —
  but to order the band so no category spans both rows.

## The warning that earned this file

⛔ **The YAML was translated by hand, file by file, against the table above.** An
earlier pass used regexes over whole documents and did three kinds of damage, each
silent until the compiler or a line count caught it: a `play:` → `roll:`
substitution collapsed a newline; a timeline rebuild anchored on `timeline:`
matched the ANIMATION section in scene 4 and replaced 300 lines of it; and the
hyphen sweep hit SVG id references as well as identifiers. Scene 3 lost 43 lines
and scene 4 its whole animation section before line counts exposed it.

That pass was restored away, and this migration started again from the untouched
source.
