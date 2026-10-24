# Witham - Maldon - South Woodham Ferrers: traced alignment

Files
- `wsw_centreline.csv` / `.geojson`: centreline every 5 m with raw and fitted height,
  gradient, trace confidence and a `flag` per sample
- `wsw_stations.csv`: each station projected onto the centreline
- `wsw_profile.png`: height and gradient along the line

Flags
- `measured`: fitted height agrees with the LIDAR
- `interpolated`: LIDAR rejected (trees, roads, bridges, ditches); height comes from the neighbouring good measurements
- `not_railway_like`: the traced line climbs or falls too steeply to be a railway;
  heights are a straight grade between trusted ends. Do not use as survey data.

How it was made
1. Environment Agency 1 m LIDAR terrain (2022 composite) for the whole corridor.
2. OpenStreetMap's abandoned and razed railway ways (Witham to Maldon Line, Woodham Ferrers to
   Maldon Line) as a guide to where the line ran.
3. Each point of that guide is moved up to 25 m sideways to the clearest embankment or cutting
   in the LIDAR, then the result is smoothed into a graceful curve. Where the LIDAR shows nothing
   (built over, or planted), the line stays close to the OpenStreetMap guide.
4. Heights come from the LIDAR, with trees, roads and bridges rejected and bridged from the
   neighbouring good measurements.
5. Structure positions and facts come from the Essex County Council 2011 field survey.

How far to trust it (see the profile plot)
- Strong: Wickham Bishops to Langford; Maldon West to Cold Norton and Stow Maries. Stations
  fall within 1 - 16 m of the line (Wickham Bishops 1, Langford 1, Maldon West 16, Barons Lane 5,
  Cold Norton 12, Stow Maries 8), using Wikipedia coordinates that played no part in the tracing.
- The Maldon link now follows the embankment ridge visible in the LIDAR, from the junction north
  of Maldon to the viaduct site and on to Maldon West (see `wsw_structures.csv`; surveyed bridge
  positions are only as precise as their 100 m grid squares).
- Witham: the branch left the main line at the north end of the station and curved east of the
  town. The trace starts 379 m from the Wikipedia station coordinate because the first stretch is
  buried under development; it agrees to within 5 - 56 m with a phone screenshot of RailMapOnline's
  historic layer, used only as a visual check.
- The last 2 km into South Woodham Ferrers: the new town (from the 1970s) obliterated the track.
  This stretch follows OpenStreetMap's mapped line and only property boundaries and a footpath north
  of Bancrofts Road mark it on the ground.
  A phone screenshot of RailMapOnline's historic layer shows the branch curving in from the north-east
  and meeting the Crouch Valley line at the west edge of the town; the traced line follows the same
  curve to within about 4 - 76 m (the screenshot's scale bar was cut off, so its scale was fitted).
- Heights are bare-earth model heights (+-15 cm published specification). The viaduct and the
  bypass embankments distort heights between Maldon East and Maldon West; the plot marks the
  untrusted stretch.

Licence and credits
- Combined data are published under the Open Database Licence (ODbL) because they use OpenStreetMap data:
  (c) OpenStreetMap contributors, https://www.openstreetmap.org/copyright
- Contains Environment Agency information (c) Environment Agency and/or database right, supplied under
  the Open Government Licence v3.0.
- Structure data and history: Kemble and Garwood, *The Lost Railways of the Blackwater and Crouch
  Estuaries* (Essex County Council, 2011). The survey's six-figure grid references name 100 m
  squares, so positions are +-70 m; each square's centre is used.
- Natural Earth coastlines (public domain). Station coordinates from Wikipedia.
- RailMapOnline (www.railmaponline.com) screenshots were used as a visual check only; no RailMapOnline
  data is included.
