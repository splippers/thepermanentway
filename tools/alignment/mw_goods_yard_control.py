#!/usr/bin/env python3
"""Builds a ControlNet conditioning image (line drawing) of the Maldon West
station, tunnel and goods yard, for the multitraktion illustration pipeline.

Geometry comes from one place: the georeferenced footprints traced from the
Ordnance Survey 25-inch map of Essex (1890s; NLS tiles, about 1-2 m) in
data/alignments/mw_1890s_footprints.geojson, plus the map-snapped line through
the station in maldon3d/mw_footprints.js. Nothing here is read from the
sketch (MWSketch.jpg is not to scale against itself) or from the 1897 plan
overlay (its registration was up to ~170 m out in the yard).

An earlier version of this script placed the goods shed about 170 m too far
north from a plan-pixel reading; see docs/research/maldon_west_corrections.md.

What is and is not drawn:
- Drawn from the trace: both platforms, canopies, station buildings, booking
  office, road-bridge strip, tunnel south-portal structure, goods shed (about
  46 x 14 m), shed office, signal box, weighing machine, end-and-side dock,
  roadside houses, the cutting top edges and the line.
- Not drawn, because not traced: individual tracks, sidings, the headshunt,
  the twin covered stairways (only the stair strips on the map), the tower.

Usage: mw_goods_yard_control.py [--part station|yard|all] [--out FILE] [--size N]
       [--margin M] [--no-cutting] [--no-houses]

The site is 700 m long and under 150 m wide, so "all" is a thin strip; use
--part station (platforms, booking office, tunnel mouth) or --part yard (goods
shed, dock, signal box, south portal) for something closer to square.
"""
import argparse
import json
import pathlib

from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parents[2]
GEOJSON = ROOT / "data" / "alignments" / "mw_1890s_footprints.geojson"
AXIS_JS = ROOT / "maldon3d" / "mw_footprints.js"

HOUSES = {"house_nw", "house_w2", "house_e", "cottage"}
PARTS = {"station": (206320, 206570), "yard": (205990, 206350), "all": (0, 1e9)}
HEAVY = {"goods_shed", "booking_office", "east_building", "west_building"}


def load_features():
    polys, lines = {}, {}
    for f in json.loads(GEOJSON.read_text())["features"]:
        name, bng = f["properties"]["name"], [tuple(p) for p in f["properties"]["bng"]]
        (polys if f["geometry"]["type"] == "Polygon" else lines)[name] = bng
    return polys, lines


def load_axis():
    txt = AXIS_JS.read_text()
    data = json.loads(txt[txt.index("=") + 1:].rstrip().rstrip(";"))
    return [tuple(p) for p in data["axis"]]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="mw_goods_yard_control.png")
    p.add_argument("--size", type=int, default=1024)
    p.add_argument("--margin", type=float, default=8.0, help="metres of padding")
    p.add_argument("--part", choices=sorted(PARTS), default="all")
    p.add_argument("--no-cutting", action="store_true", help="omit the cutting top edges")
    p.add_argument("--no-houses", action="store_true", help="omit the roadside houses")
    args = p.parse_args()

    polys, lines = load_features()
    if args.no_houses:
        polys = {k: v for k, v in polys.items() if k not in HOUSES}
    if args.no_cutting:
        lines = {}
    axis = load_axis()
    lo, hi = PARTS[args.part]
    inside = lambda q: lo <= q[1] <= hi
    polys = {k: v for k, v in polys.items() if inside(v[0]) or inside(v[len(v) // 2])}
    lines = {k: [q for q in v if inside(q)] for k, v in lines.items()}
    axis = [q for q in axis if inside(q)]

    pts = [q for v in polys.values() for q in v] + [q for v in lines.values() for q in v] + axis
    es, ns = [q[0] for q in pts], [q[1] for q in pts]
    e0, e1 = min(es) - args.margin, max(es) + args.margin
    n0, n1 = min(ns) - args.margin, max(ns) + args.margin
    scale = args.size / max(e1 - e0, n1 - n0)

    def px(q):
        return ((q[0] - e0) * scale, (n1 - q[1]) * scale)  # north up

    img = Image.new("RGB", (round((e1 - e0) * scale), round((n1 - n0) * scale)), "white")
    d = ImageDraw.Draw(img)
    for name, v in polys.items():
        d.polygon([px(q) for q in v], outline="black", width=4 if name in HEAVY else 3)
    for v in lines.values():
        d.line([px(q) for q in v], fill="black", width=2)
    d.line([px(q) for q in axis], fill="black", width=3)
    img.save(args.out)
    print(f"{args.out}: {img.size[0]}x{img.size[1]}, {len(polys)} polygons, "
          f"{len(lines)} edge lines, axis of {len(axis)} points; "
          f"E {e0:.0f}-{e1:.0f}, N {n0:.0f}-{n1:.0f}")


if __name__ == "__main__":
    main()
