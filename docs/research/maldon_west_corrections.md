# Maldon West: proposed corrections

Status: **proposed, not applied.** Nothing in `game/mission-wsw.js`,
`data/alignments/wsw_structures.csv` or `tools/alignment/mw_goods_yard_control.py`
has been changed by this note. Each item says what the evidence is and what
would change if it is accepted.

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

## 5. West platform may be traced too thin

For about 85 of its 119 m the west platform polygon is 2-3 m wide, against
5-10 m for the east platform. The photograph MWPlat.jpg shows a normal
platform. Needs another look at the map; the polygon is probably too
narrow.

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
