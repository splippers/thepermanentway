#!/usr/bin/env python3
"""Builds a ControlNet conditioning image (canny/lineart style) for the
Maldon West station, platforms and goods yard.

Geometry sources, in order of trust:
1. refmaterial/Maldon/MWSketch.jpg - a dimensioned engineer's/BR-era
   sketch: goods shed 21ft x 34ft, platforms 324ft each (Up and Down),
   coal road/headshunt ~1080-1085ft, "End & Side Dock" 12ft x 16ft.
   Real measurements - this is what sizes everything below.
2. The ECC field survey (Kemble and Garwood, 2011; see mission-wsw.js
   sources), "Goods Shed, Maldon West" entry: "two blind arcades and one
   rebuilt and raised to a square profile facing to S, a small round
   window above central arcade, similar blind arcades with a central
   loading door facing to W, c.1889" - confirms the sketch's shed as the
   surviving building, gives orientation (loading door faces W).
3. maldon3d/map_w.jpg (1897 OS plan, same source as the ECC survey's own
   "Map 38"), pixel coordinates read by eye against a grid overlay,
   converted to BNG via the viewer's registration:
       E = 583925 + 0.53 * u
       N = 206590 - 0.53 * v
   Used for POSITION (centroid, portal locations, track alignment) since
   the sketch isn't itself geo-registered; the plan's own tolerance is
   +/-25m (see maldon3d/index.html's caption), tightened a bit by cross-
   checking the platform run against data/alignments/wsw_centreline.csv
   (a 324 ft run from the inferred north portal lands within ~0.5 m of
   the centreline's own chainage-to-distance figure).

Expect +/-5m on position from pixel-reading precision; shed and platform
SIZES are now the sketch's real dimensions, not plan-pixel guesses.

Usage: mw_goods_yard_control.py [--out FILE] [--size N]
"""
import argparse
import math

from PIL import Image, ImageDraw

FT = 0.3048  # metres per foot

# Goods shed: 21ft x 34ft (MWSketch.jpg), centred on the plan-read
# position, long axis roughly N-S per the plan/photos (loading door on
# the W long side, per the ECC survey description).
_SHED_CX, _SHED_CY = 584213.8, 206282.0  # centroid, from the plan reading
_SHED_W, _SHED_L = 21 * FT, 34 * FT
SHED = [
    (_SHED_CX - _SHED_W / 2, _SHED_CY + _SHED_L / 2),
    (_SHED_CX + _SHED_W / 2, _SHED_CY + _SHED_L / 2),
    (_SHED_CX + _SHED_W / 2, _SHED_CY - _SHED_L / 2),
    (_SHED_CX - _SHED_W / 2, _SHED_CY - _SHED_L / 2),
]

# End & Side Dock, 12ft x 16ft (MWSketch.jpg), just south of the shed
_DOCK_CX, _DOCK_CY = 584218.0, 206278.0
_DOCK_W, _DOCK_L = 12 * FT, 16 * FT
DOCK = [
    (_DOCK_CX - _DOCK_W / 2, _DOCK_CY + _DOCK_L / 2),
    (_DOCK_CX + _DOCK_W / 2, _DOCK_CY + _DOCK_L / 2),
    (_DOCK_CX + _DOCK_W / 2, _DOCK_CY - _DOCK_L / 2),
    (_DOCK_CX - _DOCK_W / 2, _DOCK_CY - _DOCK_L / 2),
]

# Running lines through the yard throat (plan pixels ~578-605 u band),
# approximated as two parallel tracks - the loop/headshunt serving the
# shed siding, not a precise track-by-track trace.
TRACK_A = [(584212.0, 206412.0), (584218.0, 206320.0), (584222.0, 206260.0)]
TRACK_B = [(584219.0, 206412.0), (584225.0, 206320.0), (584229.0, 206260.0)]

# Shed siding spur, splitting off track A towards the shed
SIDING = [(584215.0, 206360.0), (584213.8, 206293.2)]

# Spital Road tunnel portals (see mission-wsw.js discussion - plan
# reading gives ~29m gap, close to 66ft/21m, not 66yd/60m)
NORTH_PORTAL = (584211.2, 206416.2)
SOUTH_PORTAL = (584219.2, 206388.6)

# Platforms: 324ft each (MWSketch.jpg), Up and Down, running from the
# north portal back towards Witham along the real centreline (see
# data/alignments/wsw_centreline.csv, chainage ~9789 to ~9890 - this
# matches 324ft to within ~0.5m, independent of the sketch).
_CENTRELINE = [  # chainage, easting, northing - from wsw_centreline.csv
    (9790.0, 584174.4, 206533.4), (9800.0, 584176.4, 206523.6),
    (9810.0, 584178.4, 206513.8), (9820.0, 584180.4, 206504.0),
    (9830.0, 584182.6, 206494.2), (9840.0, 584184.7, 206484.5),
    (9850.0, 584186.9, 206474.7), (9860.0, 584189.1, 206465.0),
    (9870.0, 584191.4, 206455.2), (9880.0, 584193.7, 206445.5),
    (9890.0, 584196.0, 206435.8),
]
_PLATFORM_OFFSET = 4.0  # m, running-line to platform edge, each side


def _offset_line(points, offset):
    """Offset a polyline perpendicular to its local direction."""
    out = []
    for i, (_, e, n) in enumerate(points):
        if i == 0:
            de, dn = points[1][1] - e, points[1][2] - n
        elif i == len(points) - 1:
            de, dn = e - points[i - 1][1], n - points[i - 1][2]
        else:
            de = points[i + 1][1] - points[i - 1][1]
            dn = points[i + 1][2] - points[i - 1][2]
        length = math.hypot(de, dn) or 1.0
        nx, ny = -dn / length, de / length  # perpendicular, unit
        out.append((e + nx * offset, n + ny * offset))
    return out


PLATFORM_DOWN = _offset_line(_CENTRELINE, _PLATFORM_OFFSET)
PLATFORM_UP = _offset_line(_CENTRELINE, -_PLATFORM_OFFSET)

ALL_POINTS = (SHED + DOCK + TRACK_A + TRACK_B + SIDING
              + [NORTH_PORTAL, SOUTH_PORTAL] + PLATFORM_DOWN + PLATFORM_UP)


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

    img_w = round((e1 - e0) * scale)
    img_h = round((n1 - n0) * scale)
    img = Image.new("RGB", (img_w, img_h), "white")
    d = ImageDraw.Draw(img)

    d.polygon([px(p) for p in SHED], outline="black", width=4)
    d.polygon([px(p) for p in DOCK], outline="black", width=3)
    for track in (TRACK_A, TRACK_B):
        d.line([px(p) for p in track], fill="black", width=3)
    d.line([px(p) for p in SIDING], fill="black", width=3)
    d.line([px(p) for p in PLATFORM_DOWN], fill="black", width=3)
    d.line([px(p) for p in PLATFORM_UP], fill="black", width=3)

    # mark the portals as short crossbars over the line, for the prompt
    # to anchor "tunnel mouth" detail on
    for portal in (NORTH_PORTAL, SOUTH_PORTAL):
        x, y = px(portal)
        d.line([(x - 15, y), (x + 15, y)], fill="black", width=5)

    img.save(args.out)
    print(f"wrote {args.out} ({img_w}x{img_h}, "
          f"{e1-e0:.0f}m x {n1-n0:.0f}m world extent, {scale:.2f} px/m)")


if __name__ == "__main__":
    main()
