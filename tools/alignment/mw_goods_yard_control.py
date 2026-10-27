#!/usr/bin/env python3
"""Builds a ControlNet conditioning image (canny/lineart style) for the
Maldon West goods yard, from geometry read off the 1897 OS plan.

Source of the geometry: maldon3d/map_w.jpg, pixel coordinates read by eye
against a 10px grid overlay at 5x zoom, converted to BNG via the same
registration the 3D viewer uses (maldon3d/index.html's BASEW/toENW):
    E = 583925 + 0.53 * u
    N = 206590 - 0.53 * v
This is a manual digitisation, not a traced/surveyed footprint - expect
+/-5m from pixel-reading precision, on top of the plan's own stated
+/-25m registration tolerance (see maldon3d/index.html's caption). Good
enough to constrain an illustration; not good enough to cite as survey.

Cross-checked against data/alignments/wsw_centreline.csv: the shed
position converts to within ~15-30m of the chainage ~10035-10050
centreline points, which is itself flagged `not_railway_like` in that
stretch - consistent, not independently confirming.

Usage: mw_goods_yard_control.py [--out FILE] [--size N]
"""
import argparse
import math

from PIL import Image, ImageDraw

# Goods shed rectangle, read from the plan (maldon3d/map_w.jpg pixels
# ~538,560 to ~552,602), converted to BNG.
SHED = [
    (584210.1, 206293.2),  # NW
    (584217.6, 206293.2),  # NE
    (584217.6, 206270.9),  # SE
    (584210.1, 206270.9),  # SW
]

# Running lines through the yard throat (plan pixels ~578-605 u band),
# approximated as two parallel tracks - the loop/headshunt serving the
# shed siding, not a precise track-by-track trace.
TRACK_A = [(584212.0, 206412.0), (584218.0, 206320.0), (584222.0, 206260.0)]
TRACK_B = [(584219.0, 206412.0), (584225.0, 206320.0), (584229.0, 206260.0)]

# Shed siding spur, splitting off track A towards the shed
SIDING = [(584215.0, 206360.0), (584213.8, 206293.2)]

# Spital Road tunnel portals (see docs/ROADMAP.md discussion - plan
# reading gives ~29m, closer to 66ft/21m than 66yd/60m)
NORTH_PORTAL = (584211.2, 206416.2)
SOUTH_PORTAL = (584219.2, 206388.6)

ALL_POINTS = SHED + TRACK_A + TRACK_B + SIDING + [NORTH_PORTAL, SOUTH_PORTAL]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="mw_goods_yard_control.png")
    p.add_argument("--size", type=int, default=1024)
    p.add_argument("--margin", type=float, default=8.0, help="metres of padding")
    args = p.parse_args()

    es = [pt[0] for pt in ALL_POINTS]
    ns = [pt[1] for pt in ALL_POINTS]
    e0, e1 = min(es) - args.margin, max(es) + args.margin
    n0, n1 = min(ns) - args.margin, max(ns) + args.margin
    scale = args.size / max(e1 - e0, n1 - n0)

    def px(pt):
        e, n = pt
        x = (e - e0) * scale
        y = (n1 - n) * scale  # flip so north is up
        return (x, y)

    img = Image.new("RGB", (args.size, args.size), "white")
    d = ImageDraw.Draw(img)

    d.polygon([px(p) for p in SHED], outline="black", width=4)
    for track in (TRACK_A, TRACK_B):
        d.line([px(p) for p in track], fill="black", width=3)
    d.line([px(p) for p in SIDING], fill="black", width=3)

    # mark the portals as short crossbars over the line, for the prompt
    # to anchor "tunnel mouth" detail on
    for portal in (NORTH_PORTAL, SOUTH_PORTAL):
        x, y = px(portal)
        d.line([(x - 15, y), (x + 15, y)], fill="black", width=5)

    img.save(args.out)
    print(f"wrote {args.out} ({args.size}x{args.size}, "
          f"{e1-e0:.0f}m x {n1-n0:.0f}m world extent, {scale:.2f} px/m)")


if __name__ == "__main__":
    main()
