# Tracing the alignment from LIDAR

Pipeline that traces the Witham - Maldon - South Woodham Ferrers trackbed from
the Environment Agency 1 m LIDAR composite DTM (2022) and writes
`data/alignments/`. Run from this directory, in order:

1. `corridor.py`  download 1 km DTM tiles along the route (WCS) into `tiles/` (~280 MB)
2. `mosaic.py`    merge them (`mosaic.npy`)
3. `track.py`     find the trackbed: dynamic programming over lateral offset, favouring
                  long continuous ridges/cuttings, tightened in three passes
3a. `snap_osm.py` (preferred) snap the route to the LIDAR using OpenStreetMap's abandoned-railway ways as a guide (`overpass_query.txt` fetches them)
3b. `repin.py`   pin the Maldon link to the Chelmer viaduct and Navigation bridge from the county survey (the ground-following trace cannot see a viaduct)
4. `smooth.py`    fit a smooth curve (rails curve gracefully): tight where the ridge is
                  clear, free to bridge gaps where it is not
5. `profile.py`   (also run `structs.py` to compare survey structures with the traced line)
   `profile.py`   sample heights, fit a robust piecewise-linear profile that rejects
                  trees/roads/bridges, flag untrustworthy stretches, write outputs

`trace.py`-style helpers expect the scratch files above to sit in the working
directory. This is research code: it works, but it is not packaged.

OpenStreetMap data is not stored in the repo: re-run `overpass_query.txt` against an Overpass server and save the result as `osm.json`.
