# Coffee Order — a sequence diagram, drawn as it is told

A UML sequence diagram of a café order: the customer asks, the barista writes the
cup, the machine and the wand work at once, and a drink comes back. Four
participants, ten messages, two combined fragments. 54 seconds, in one cut, and 89% of it is speech.

The narration is about the **morning**, not about the notation. It never says
"lifeline" or "activation": the picture is there to be read while somebody tells
you what happened at the counter.

```sh
kinaigraph narrate_brief.yaml   # once — costs credits; the recordings are committed
kinaigraph coffee_order_brief.yaml
```

The narration is in the repository, so a clone renders it with no key.

## Why a sequence diagram is worth animating

**Every other diagram in this repository is spatial. This one is not.** A map, a
plot, a topology, a poster — you can read those in any order. A sequence diagram
has a vertical axis and that axis is **time**. Which means a video of one has two
clocks pointing the same way, and they can be made the same clock: the drawing runs
1600 deep, the frame is 1080, and the camera walks down it as the story advances.

That is the whole structure. Nothing here is a slide.

## The `par` fragment is the argument

`par` means its operands run **at the same time**. The operands are the
compartments either side of the dashed divider — and without that divider the
frame says nothing at all, because one compartment is just two messages in order.

Now look at where the operands sit: **one above the other**, in a drawing where
down has meant *later* since the first message. The notation expresses "at the
same time" using the one direction that already means "not at the same time." It
works only because the reader has been taught the convention.

⚡ **That is the thing animation fixes, and it is the reason this example
exists.** The espresso bar and the milk bar grow together on screen. The frame you
are left holding at the end is a correct static diagram; the video is what told
you which parts of it happened at once.

## What is drawn, and what is faded

⚠️ **`reveal` and a dashed stroke want the same property.** `reveal` draws a
stroke on by arc-length dash offset, which is exactly what the dash pattern of a
UML return arrow already uses. So the split here is not a taste:

| | how it arrives | why |
| --- | --- | --- |
| calls — solid | **drawn**, `reveal: {from: 0, to: 1}` | no dash to lose |
| returns, lifelines — dashed | **faded**, `opacity` | drawing one costs its dashes |
| activation bars | **drawn downward** | they are stroked lines, not rects |

⚡ **An activation bar is a line, not a rectangle.** That is what lets it grow: a
rect's stroke would draw *around its perimeter*, while a thick line with a
`reveal` extends from its start point down. The bar's width is the stroke width.

⚡ **A mug rides every message, and during the `par` there are two.** The riders
are separate elements rather than one token reused, because two are in flight at
the same moment — a single mug would have to be in two places, which is exactly
what the fragment exists to say. Their runs are the distance between two
lifelines (`X_MACHINE - X_BARISTA`), not numbers measured off the drawing.

A message to self is still a message, so it carries a mug too: out, down, and
back onto its own bar — three legs, each its own entry, because separate entries
at one bookmark are what run in sequence when each states its own start.

⚡ **The two long bars advance ROW BY ROW, ending at the message just sent.** At
any moment each is exactly as long as that person has been busy. Two ways to get
this wrong: snap them to full length at the first message and the picture
describes a morning that has not happened yet — and gives away the last line,
that the customer's bar runs the full height and nobody else's does. Grow them at
a constant rate across the whole piece instead and they lag the conversation and
read as a creep. The row positions are the drawing's own, expressed as fractions
of the bar, so moving a row in the artwork moves the bar with it.

⚠️ **Every arrowhead is its own actor, not a `marker`.** A marker is untouched by
the dash machinery, so a marker-headed arrow shows its point at full strength
before the shaft has travelled. Each head is shown when its shaft lands.

## Pinned, and scrolling

The title, the four participant heads and the four lifelines **do not move**. Only
the conversation does. A head that scrolled away would leave you unable to say
which lifeline you were looking at by the time the drink is made.

⛔ **The clip belongs on a static wrapper, not on the moving group.** A
`clip-path` resolves in its own element's user space, so putting it on the group
that travels makes the window travel too — and clip nothing. `sheet_viewport`
holds the clip and never moves; `sheet` moves inside it.

⛔ **And the thing that scrolls must not be the scene's root `<svg>`.** Targeting
the root as an actor resets the scene, and every child state written in the same
frame is discarded. The symptom is precise and misleading: the drawing renders
complete, correct, and completely static. The camera moves an inner `<g>`.

## Timing: there is not one millisecond in the document

⚡ **EVERY DURATION IS A SHARE OF THE LINE BEING SPOKEN OVER IT.** Five fractions
govern the whole piece — how long an arrow takes to draw, how long a fade takes,
how long a mug takes to cross, how long the camera takes, and how much quiet
follows. A longer line does not merely wait longer; it draws, travels and rests
longer, in proportion. Re-record anything and the beat re-fits itself.

⚡ **ACTIONS INSIDE ONE ENTRY RUN IN SEQUENCE.** That is why there is almost no
`hold` arithmetic: a beat is written as the list of things that happen, in order,
each stating only its own length. A rider is one entry — wait, arrive, run,
leave — rather than three entries chained by hand-summed offsets.

⚠️ **A BOOKMARK ENDS WHEN ITS LONGEST ACTION DOES**, which is the trap here. An
entry that overruns its own line does not get truncated: it stretches the beat,
and the overrun is heard as dead air after the narrator has stopped. One beat ran
to 1.44× its line this way. The check is arithmetic, not taste — add up the
fractions in the longest chain and keep the total under `1 + PAUSE`.

⚠️ **A WAIT MUST HOLD THE VALUE IT IS WAITING AT.** Delaying a half-grown bar
with `reveal: 0` does not pause it, it resets it — the bar collapses and regrows
every beat. Each wait states the level the previous beat left behind.

## Files

| Path | What |
| ---- | ---- |
| `coffee_order_brief.yaml` | The document: the choreography and the camera. |
| `narrate_brief.yaml` | Synthesis. The six lines. **The only thing here that bills.** |
| `resource/scene/sequence_coffee_order.svg` | The diagram. Frame-sized root, scrolling `sheet` inside it. |
| `resource/scene/brand_layer.svg` | The publisher's mark — its own scene, so the camera never carries it off. |
| `resource/style/theme_paper.css` | Values only; the drawing owns which class reads which name. |
| `resource/script/brief/*.txt` · `resource/audio/brief/*.mp3` | The six lines, and their recordings. |
| `resource/image/bitscrafter_logo.png` | The mark as a raster, before embedding. |
| `resource/template/main.html` | The HTML container. |

## Rendering it

You need Kinaigraph installed — see the [install instructions](../../README.md#install).
Run from this directory. Paths inside the document resolve against this folder, so
`file:` values need no `../`. The deliverable lands beside the document; the silent
intermediate goes to `resource/video/`.

Re-recording needs `ELEVENLABS_API_KEY`, and synthesis is a separate document on
purpose: re-rendering the scene must never re-synthesise audio that did not change.
