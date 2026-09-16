# Annotated Infographic: The Atmosphere

A 38-second video built from **a picture that already existed**. The input is
`resource/image/atmosphere.png` — a 1100 × 2700 raster, the shape a poster is, not
the shape a video is. Nothing inside it is an actor, nothing inside it moves, and
the document never edits it. What the document adds is a **camera** and six
**callouts**.

This is the case where you have a PNG or a JPEG — exported from a design tool,
scanned, screenshotted, handed to you — and want an annotated video of it.

## The one scene

| Beat | Window | What happens |
| ---- | ------ | ------------ |
| `establish` | 0.0 – 2.5 s | The whole poster, fitted to the frame's height. 1100 × 2700 into 1920 × 1080 means 0.4 × — the establishing shot is the only one that shows the piece entire. |
| `push_in` | 2.5 – 5.0 s | Pan and zoom together onto the masthead. |
| `title` | 5.0 – 8.5 s | A callout with no pointer says what the source is. |
| `pan_upper` … `troposphere` | 8.5 – 34.0 s | Four stops down the picture — exosphere and thermosphere, mesosphere, stratosphere, troposphere — each a 2 s pan then a 3.5 s dwell with one callout. The first stop holds **two** dwells, `upper` and `upper_iss`, because the camera has one framing and the picture there has two things worth saying. |
| `pull_out` | 34.0 – 38.5 s | Back to the whole poster. |

## The camera is the picture moving

The language has no camera primitive, so nothing here is a camera — and there is
no rig either. The whole scene is a background and the picture:

```xml
<rect width="1920" height="1080" fill="var(--scene-background-color, #050a14)"/>
<image id="atmosphere_infographic" x="0" y="0" width="1100" height="2700" .../>
```

The `<image>` element **is the actor**: it takes the move and the scale itself, so
a picture point `p` lands on screen at **`PAN + ZOOM × p`**. That one expression is
every stop and every pointer in the document.

Wrapper groups — one to translate, one to scale — were measured against this and
add nothing: with the image drawn at `(0, 0)` the composed transform is the same
either way. The arithmetic depends on `pivot: top_left` instead. The default pivot
is `center`, which scales about the actor's own middle: fine for a push-in on a
shape, wrong for a camera, because the fixed point then moves as the picture does.

A push-in needs the pan and the zoom at once, and that is **two entries for one
actor at one bookmark** — `move` writes position, `show` writes scale, different
properties, so they run together. Two sub-actions inside a SINGLE entry would run
in sequence instead: a dolly, then a zoom.

Every stop is written as a **vertical centre in the image's own pixels** — the
coordinates you read off the PNG — and `const` converts it:

```yaml
MESOSPHERE_Y: 1290
MESOSPHERE_PAN_Y: "FRAME_H / 2 - DETAIL_ZOOM * MESOSPHERE_Y"
```

Re-frame a stop by moving the centre, never the pan.

## The callouts annotate the picture without touching it

Each note's **box is parked in the frame** and its **pointer aims into the
picture**:

```yaml
pointer:
    target:
        x: "DETAIL_PAN_X + DETAIL_ZOOM * MESOSPHERE_POINT_X"
        y: "MESOSPHERE_PAN_Y + DETAIL_ZOOM * MESOSPHERE_POINT_Y"
at:
    x: 430
    y: 600
```

The target is the same `PAN + ZOOM × p` mapping, so a pointer is aimed at a place
in the *image* — the meteor streaks, the ozone band, Everest — while the box stays
at a fixed size in the frame. A box that scaled with the camera would be unreadable
at the overview and enormous at a stop.

Two consequences worth keeping:

- **The type is sized against the picture, not the frame.** A detail stop magnifies
  the poster by `DETAIL_ZOOM`, so its own 20 px captions arrive at 32.5 px. The
  callouts are set at 30 px to match; at 20 px they read as fine print beside the
  thing they annotate.
- **A pointer and its stop are one fact.** The target is converted by that stop's
  pan, so moving a stop without moving its pointer aims the leader at empty sky.
  Check the pair.
- ⚠️ **A note's text WRAPS, and what will not fit is silently clipped.** A line 14 px
  too long for the box cost this example a callout that rendered with its second
  line missing and no warning anywhere. Measuring the ink *inside* the box does not
  catch it — the check that does is counting the rendered text lines and comparing
  against the authored ones.

Each callout's window is three actions in one entry — fade in, hold, fade out —
whose durations sum to the dwell, with the hold derived (`DWELL_MS - FADE_MS * 2`)
rather than written twice.

## The input image

`resource/image/atmosphere.png` is treated as **given**. The poster's own SVG
source sits in `resource/temp/` beside the script that rasterises it, because
that is where an input's provenance belongs — but no part of the pipeline reads
it. Swap in any PNG or JPEG, re-run the generator, and adjust the stops.

`resource/temp/make_frame_svg.py` wraps that file in the 16:9 scene and prints its
pixel size:

```sh
python3 resource/temp/make_frame_svg.py
```

Rebuilding the input from the poster source is three steps, and only the last one
is part of the example:

```sh
resource/temp/render.sh resource/temp/atmosphere.svg 1100 2700 1
cp resource/temp/atmosphere.png resource/image/atmosphere.png
python3 resource/temp/make_frame_svg.py
```

⚠️ **The image is embedded as base64, not linked.** A relative `href` resolves in
`animation.html` but **breaks at capture**, which renders a copy of the page from
`resource/temp/.capture/` — one directory deeper, where `../image/` no longer
exists. The failure is silent in the video: a broken-image icon, panned and zoomed
exactly as the picture would have been.

## Files

| Path | Role |
| ---- | ---- |
| `scene_01_layers_tour.yaml` | The document: camera, callouts, timeline. |
| `resource/image/atmosphere.png` | **The input.** A pre-existing raster. |
| `resource/scene/atmosphere_frame.svg` | Generated — the 16:9 frame and the two camera groups. |
| `resource/style/theme_dark.css` | One variable: the letterbox colour behind the picture. |
| `resource/temp/make_frame_svg.py` | Embeds the image in the frame. Re-run after swapping the input. |
| `resource/temp/atmosphere.svg` | Where the input PNG came from — provenance, not a build step. |
| `resource/temp/render.sh` | Rasterises that SVG at a device scale factor. |

## Rendering

```sh
kinaigraph run scene_01_layers_tour.yaml
```

The tour is silent — the picture and the callouts carry it. There is no
`scene_00_tts_generation.yaml` here.

## Sources

The poster states facts, so its figures were checked against primary sources
rather than carried over from wherever the draft got them. The poster carries the
citations itself, in the footer; they are repeated here with links, together with
what each one settled.

| Claim | Source |
| ----- | ------ |
| Layer altitudes; mesopause ≈ −85 °C; the ISS orbits in the thermosphere; the Kármán line holds 99.99997% of the atmosphere below it | [NASA, *Earth's Atmosphere: A Multi-layered Cake*](https://science.nasa.gov/earth/earth-atmosphere/earths-atmosphere-a-multi-layered-cake/) |
| Mesosphere to 85 km; thermosphere 500–2,000 °C, top anywhere from 500 to 1,000 km | [UCAR, *Layers of Earth's Atmosphere*](https://scied.ucar.edu/learning-zone/atmosphere/layers-earths-atmosphere) · [UCAR, *The Thermosphere*](https://scied.ucar.edu/learning-zone/atmosphere/thermosphere) |
| Thermosphere up to 2,000 °C or higher | [NASA, *What Is Earth's Atmosphere?*](https://www.nasa.gov/general/what-is-earths-atmosphere/) |
| Dry air is 78% nitrogen, 21% oxygen, 0.93% argon | [UCAR, *What's in the Air*](https://scied.ucar.edu/learning-zone/air-quality/whats-in-the-air) |
| The ozone layer is 15–35 km | [NOAA/WMO, *Twenty Questions About the Ozone Layer*](https://csl.noaa.gov/assessments/ozone/2022/twentyquestions/) · [NASA Ozone Watch](https://ozonewatch.gsfc.nasa.gov/facts/SH.html) |
| A radiosonde can exceed 35 km before the balloon bursts | [NWS, *Radiosonde Observation*](https://www.weather.gov/upperair/factsheet) |
| Airliners cruise at 9.1–12 km; the tropopause runs ~8 km polar to ~18 km tropical | [Britannica, *How High Does an Airplane Fly?*](https://www.britannica.com/topic/How-High-Does-An-Airplane-Fly) · [Britannica, *Tropopause*](https://www.britannica.com/science/tropopause) |
| The hydrogen geocorona reaches ~630,000 km — past the Moon's 384,400 km | [Baliukin et al., *JGR Space Physics* 2019](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2018JA026136) · [ESA/SOHO](https://www.esa.int/Science_Exploration/Space_Science/Earth_s_atmosphere_stretches_out_to_the_Moon_and_beyond) · [NASA Space Place](https://spaceplace.nasa.gov/moon-distance/en/) |
| Everest is 8,848.86 m (Nepal–China, December 2020) | [Kathmandu Post](https://kathmandupost.com/national/2020/12/08/it-s-official-mount-everest-is-8-848-86-metres-tall) |

Two things the checking changed, worth keeping in view:

- **Layer boundaries are conventions, and the sources disagree.** NASA puts the
  mesosphere at 50–80 km and the thermosphere at 80–700; UCAR has the mesosphere
  to 85 km and the thermosphere's top anywhere from 500 to 1,000. The poster uses
  the common 50–85 / 85–600 set and its footer now says boundaries vary by source
  as well as by latitude and season.
- **Nothing is "outside" the atmosphere.** There are two boundaries and neither is
  an edge: the Kármán line at 100 km is an administrative convention, and the
  exobase (~500–1,000 km) is where a particle's mean free path exceeds the scale
  height, so molecules stop colliding. The ISS callout is built on that — it sits
  four times above the Kármán line and is *still* dragged down by air.
