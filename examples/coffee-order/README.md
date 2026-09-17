# Coffee Order — a sequence diagram, drawn as it is told

A UML sequence diagram of a café order: the customer asks, the barista writes the
cup, the machine and the wand work at once, and a drink comes back. Four
participants, ten messages, two combined fragments. 52 seconds, in one cut, and 93% of it is speech.

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
back onto its own bar.

⚠️ **TWO MUGS IN ONE LANE MEANS TWO THINGS HAPPENING AT ONCE THERE**, so anywhere
that is not true, the first has to be GONE before the second arrives. A request
still fading out as its own reply sets off says the two overlapped, which is a
claim about the café, not a detail of the animation.

Two beats carry a there-and-back in a single line — the detour, and each lane of
the `par`. They only fit sequentially if the crossings run shorter, which is the
one rule: **a beat holding two journeys runs them at `RUN * 0.55`**, and the
second waits on `DRAW + FADE * 2 + RUN * 0.55` — precisely the time the first
takes to appear, cross and leave.

⚡ **The `par` is the exception that proves it.** Two mugs on screen at once is
exactly right there — but one per LANE. The lanes are simultaneous with each
other; nothing is simultaneous with itself.

⚡ **The two long bars advance ROW BY ROW, ending at the message just sent.** At
any moment each is exactly as long as that person has been busy. Two ways to get
this wrong: snap them to full length at the first message and the picture
describes a morning that has not happened yet — and gives away the last line,
that the customer's bar runs the full height and nobody else's does. Grow them at
a constant rate across the whole piece instead and they lag the conversation and
read as a creep. The row positions are the drawing's own, expressed as fractions
of the bar, so moving a row in the artwork moves the bar with it.

⚡ **A MARKER RIDES ITS ELEMENT'S `opacity` BUT NOT ITS `reveal`.** That one
measured fact decides how every arrowhead here is built:

| shaft | head | why |
| --- | --- | --- |
| returns — **faded** | a `<marker>`, the ordinary way | the marker fades in lockstep with its line |
| calls — **drawn** | its own element, shown when the shaft lands | a marker paints at full strength from the first frame |

Revealing a marker-headed arrow puts the point at the far end while the shaft is
still a fifth of the way across. So the head is drawn the way its shaft is
drawn, and the split is not a matter of taste.

⚠️ **A marker's local +x is the direction of travel**, so the tip belongs at the
larger x with the arms trailing. Drawn the other way round the chevron points
back down its own arrow — which is easy to miss on a left-pointing return.

## Groups say a thing once

⚡ **A GROUP BROADCASTS; IT IS NOT A CONTAINER.** Naming one in a timeline
expands into one instruction per member, so members stay individually
addressable afterwards. That is what lets `not_yet` hide forty actors in a
single line while every one of them is still shown on its own beat later.

⚠️ **The two starting states are different properties, not one state.** A faded
thing waits at `opacity: 0`, a drawn thing at `reveal: 0` — they cannot share a
group because they do not share a verb. Hence `not_yet` and `undrawn`.

⚡ **The `par` groups are the argument, not the saving.** Two entries at one
bookmark merely *happen* to coincide; `par_calls` **states** that the espresso
leg and the milk leg are one thing that happens once. The document now says what
the picture is claiming.

⛔ **The riders are deliberately not grouped.** A group `move` may only use
`dx`/`dy` — absolute and anchor positions are refused at compile time — and even
if they were allowed, the two legs cross different distances. A group is for
things doing the *same* thing, not merely things doing it at the same moment.

## Why the mugs do not ride their own arrows

The obvious way to move a rider is `move: { along: { asset: <the message> } }` —
`request-response` does exactly that, and it works here too: a mug will trace a
straight `<line>` or follow the three segments of a self-call `<path>` with no
waypoints authored at all.

⛔ **It is refused in this example, and the refusal is right.** The diagram pans,
so the riders sit inside the group the camera moves:

```text
'rider_order' sits inside the moving group 'sheet' — a move-along rider nested
inside a moving group is transformed twice (once by the group, once by the ride)
```

⚡ **You can have a camera that moves the drawing, or riders that ride the
drawing's own geometry — not both on the same elements.** This example chose the
camera, because a sequence diagram deeper than its frame is the entire point. So
the mugs cross by `dx`, and the distance is named as what it is: the gap between
two lifelines, `X_MACHINE - X_BARISTA`.

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
