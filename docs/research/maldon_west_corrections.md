# Maldon West: corrections

Status: **accepted and applied** (office Claude, commit d214947), after
review against `weststationgoodsshed1.jpg` and the reasoning in
`docs/notes/NOTE_FOR_OFFICE_CLAUDE.md`. Items 1-4 below (shed position,
shed size, tunnel length, platform length) are reflected in
`game/mission-wsw.js` and `data/alignments/wsw_structures.csv`.
`tools/alignment/mw_goods_yard_control.py` is flagged superseded rather
than rewritten - it should eventually read positions from
`data/alignments/mw_1890s_footprints.geojson` directly instead of its
own uncalibrated plan-pixel registration, but that rewrite hasn't
happened yet. Item 5 (west platform possibly traced too thin) and the
licence question are open and belong to this file's own trace, not to
anything office Claude touched.

Each item below still says what the evidence was and what changed -
kept as the record, not rewritten into past tense throughout.

## Evidence base

- **Map trace (new).** Footprints traced by eye from the Ordnance Survey
  25-inch map of Essex (1890s; sheet edition unconfirmed), georeferenced web
  tiles at about 0.37 m per pixel, courtesy of the National Library of
  Scotland (https://maps.nls.uk). Accuracy about 1-2 m. Output:
  `data/alignments/mw_1890s_footprints.geojson`; scripts in
  `tools/alignment/mw_trace/`. The NLS licence for this layer is not
  confirmed (see "Licence" below).
- **OpenStreetMap buildings** (ODbL) in West Station Yard, fetched via Overpass.
- **ECC field survey** (Kemble and Garwood, 2011): the goods shed entry
  (TL842061) and the tunnel entry.
- **Photographs** in `refmaterial/Maldon/` (MWPlat.jpg, MW1973.jpg,
  MW1957.jpg, maldon-west-25_o.jpg, weststationgoodsshed1.jpg).
- **Dimensioned sketch** `refmaterial/Maldon/MWSketch.jpg` (not to scale).

## 1. Goods shed position: about 170 m too far north

`mw_goods_yard_control.py` places the shed centroid at E 584213.8, N 206282.
That comes from reading the 1897 plan overlay (`maldon3d/map_w.jpg`) through
the viewer's registration (E = 583925 + 0.53u, N = 206590 - 0.53v).

Three independent sources agree on a position near **E 584200, N 206110**:

| Source | Position | Size |
|---|---|---|
| Map trace (1890s footprint) | 584193, 206116 | 46 x 14 m |
| OSM "Maldon Metals", West Station Yard | 584200, 206111 | 16 x 47 m bbox |
| ECC survey grid reference TL842061 | 584200, 206100 (to 100 m) | n/a |

`weststationgoodsshed1.jpg` shows a long red-brick building with a round
window in the gable and an arcaded long side, signed "Maldon Metals Ltd".
That is the survey's description of the surviving shed. Position 584214,
206282 sits among the modern units of West Station Yard (Pizza Supreme and
neighbours), not at the shed.

The plan overlay registration is therefore not within the stated +/-25 m at
the yard end: the same registration puts the south tunnel portal about 85 m
and the shed about 170 m from the map-based positions. It may still be fine
near the road. Suggested change: rerun `mw_goods_yard_control.py` with
positions taken from the GeoJSON, and drop the +/-25 m claim for the yard.

## 2. Goods shed size: sketch figure is not the building's size

`MWSketch.jpg` gives the shed as 21 ft by 34 ft (6.4 x 10.4 m). The sketch
is plainly not to scale (the 34 ft dimension is drawn longer than 324 ft of
platform would allow at the same scale). The map footprint and the OSM
building both say about 46 x 14 m. Suggested change: use 46 x 14 m for the
building; keep the sketch's figures only as the sketch's own labels (they may
describe the shed's original bay or the loading area).

## 3. Tunnel length: 66 yards is supported; 21 m is the road width

The recent change reads 66 yards as a probable units error for 66 feet
(21 m), on the grounds that the track-hatching gap at the Spital Road
crossing is about 21 m on the plan.

On the 25-inch map the tunnel is drawn with long dashed hidden lines between
two hatched strips, not just under the road:

- south portal strip: N 206326 to 206336 (about 10 m deep);
- north strip, under the booking office and bridge deck: N 206383 to 206389;
- between the strips: about 47-49 m of dashed tunnel outline;
- outer edge to outer edge: about 62 m, against the survey's 66 yards (60.4 m).

The crossing of Spital Road (a diagonal on the map) accounts for only about
21 m of that. Suggested change: restore "66 yards (about 60 m, including the
portal structures)" in `wsw_structures.csv` and `mission-wsw.js`, and remove
the "probably a units error" wording. The survey's 21 m, if it truly appears
in the survey, could be the width of the road above.

The south portal position is also anchored by Jon's coordinates for
"1 W Station Yard" (51.725403, 0.665799), which convert to N 206328, the
south strip.

## 4. Platform length: sketch 324 ft (99 m) against map 119-125 m

The sketch labels each platform 324 ft (99 m). The earlier guess of "424 ft"
is withdrawn: it was a misreading. The traced platforms are 119 m (west) and
125 m (east) overall, with long tapered ends; the full-width part of the
east platform is about 114 m. Not resolved: either the sketch is approximate,
or 324 ft is the straight, full-height part. Suggested change: say "about
100-125 m" in text until a better source turns up.

## 5. West platform is narrow on the map, and my first statistic misled

Rechecked against the raw map at 4x. The polygon follows the drawn outline
everywhere: the left outline and the inner line next to the track bundle.
The earlier "2-3 m wide for 85 m" figure came from slicing a polygon with a
step in it; the real picture is:

- west platform: 7-9.5 m wide over the first 30 m from the road end (where
  the canopy and building sit), then a tapering strip of about 2 m for the
  remaining 75-85 m; mean width 3.7 m over 119 m;
- east platform: 9 m at the road end, then 4-5 m for the rest; mean 6.4 m
  over 125 m.

So the west platform really is drawn thin and the east one about twice as
wide. A 2 m platform is implausibly narrow, so the inner line may be the
coping line with the platform surface partly hidden among the track bundle
lines; I cannot settle that from the map. Use the traced outlines as "what
the map draws", and take 3-4.5 m as the working width for the thin sections
until a photograph or plan says otherwise. `MWPlat.jpg` shows the platform
edge but cannot give a width.

**The 1957 group photo (`MW1957.jpg`).** About 30 people stand in three or
four ranks across the platform in front of a coach, with the tunnel arch
behind them, so the view is within roughly 30-40 m of the road end. The
front rank is about 4.5-5 m wide, which puts the photographer about 5 m
away; adding the ranks (about 2 m) and the gap to the edge, the platform is
at least 7.5-8 m deep there. That is a rough estimate with no known scale in
the frame (a metre or two either way), but it fits the map's 9 m at the road
end for the east platform. It says nothing about the thin outer stretch.

Above the arch the photo also shows two upper windows (one round-headed)
and brick buttresses, with what looks like a bricked-up door between the
windows (Jon's reading). Jon's account is that these opened onto the
enclosed corridor joining the two diagonal staircases, which was long gone
by 1957. This is useful detail for modelling the booking-office block and
the stairs, and it is from Jon's reading of the photo, not from a
documentary source.

## 6. Things the new work adds that the repo did not have

- Georeferenced footprints for both platforms, canopies, station buildings,
  booking office, goods shed, signal box, dock, houses and the cutting top
  edges.
- The station is wholly in a cutting, with the platforms north of the
  tunnel (under today's bypass, just north of the roundabout) and the yard
  south of it.
- A rebuilt cutting in `maldon3d/index.html`, because the LIDAR lost it
  under the bypass.

## Licence

The footprints derive from an NLS-hosted OS 25-inch map. The NLS page lists
its own layers as CC BY 3.0, but the Essex 25-inch layer is not listed, and
the underlying OS data may carry its own terms. Map tiles are not in this
repo. The GeoJSON is original tracing by eye and carries an attribution to
the OS and NLS. Before any wider release, ask maps@nls.uk.

## Open questions

See `docs/notes/NOTE_FOR_OFFICE_CLAUDE.md`.
