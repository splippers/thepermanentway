#!/usr/bin/env python3
"""Build the 'Maldon LIDAR: help needed' annotation page (static, phone friendly).

Renders three 1.8 km LIDAR hillshade windows at 1 px = 1 m, embeds the traced centreline,
stations and surveyed structures, and writes index.html + images to --out.
Run from this directory with the scratch mosaic present (or it fetches windows from the EA WCS).
"""
import argparse, csv, json, os, sys
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
from matplotlib.colors import LightSource
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wcs import bng, fetch
import rasterio

ap = argparse.ArgumentParser()
ap.add_argument('--out', default='/mnt/SANDIEGO/Projects/maldon-reborn/web/lidar')
ap.add_argument('--data', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'alignments'))
ap.add_argument('--cache', default='annot_cache')
args = ap.parse_args()
os.makedirs(args.out, exist_ok=True); os.makedirs(args.cache, exist_ok=True)

AREAS = [
  dict(id='maldon', name='Maldon: the link between East and West', E0=584000, N0=206200,
       blurb='The embankment from the junction north of the town, over the Chelmer viaduct, down the west side of Maldon to Maldon West.'),
  dict(id='witham', name='Witham: the run out of the station', E0=581600, N0=214500,
       blurb='Where the branch left the main line and how far it survives under the town.'),
  dict(id='swf', name='South Woodham Ferrers: the scar', E0=579800, N0=196900,
       blurb='The last 2 km into the new town, where the track was obliterated.'),
]
SZ = 1800

def window(a):
    f = os.path.join(args.cache, '%s_%d_%d.tif' % (a['id'], a['E0'], a['N0']))
    if not os.path.exists(f):
        fetch(a['E0'], a['N0'], a['E0'] + SZ, a['N0'] + SZ, f)
    z = rasterio.open(f).read(1).astype('float64'); z[z < -1e30] = np.nan
    return z

def render(z, path):
    fill = np.nanmean(z); zn = np.nan_to_num(z, nan=fill)
    lrm = zn - gaussian_filter(zn, 12)
    hs = LightSource(azdeg=315, altdeg=40).hillshade(zn, vert_exag=4, dx=1, dy=1)
    hs = np.clip((hs - 0.5) * 1.5 + 0.5, 0, 1)   # stretch contrast so cuttings and embankments stand out
    base = np.stack([hs * 0.85 + 0.12] * 3, -1)
    t = np.clip(lrm / 2.0, -1, 1)
    tint = np.stack([0.5 + 0.5 * np.clip(t, 0, 1), 0.5 - 0.15 * abs(t), 0.5 + 0.5 * np.clip(-t, 0, 1)], -1)
    rgb = base * 0.62 + tint * 0.38
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype('uint8')).save(path, quality=84)
    return float(np.isnan(z).mean())

cl = list(csv.DictReader(open(os.path.join(args.data, 'wsw_centreline.csv'))))
CE = np.array([float(r['easting']) for r in cl]); CN = np.array([float(r['northing']) for r in cl])
CH = [r['chainage_m'] for r in cl]
stations = list(csv.DictReader(open(os.path.join(args.data, 'wsw_stations.csv'))))
structs = list(csv.DictReader(open(os.path.join(args.data, 'wsw_structures.csv'))))
ST = [('Witham', 51.8060, 0.6391), ('Wickham Bishops', 51.7732, 0.6431), ('Langford & Ulting', 51.7480, 0.6666),
      ('Maldon East & Heybridge', 51.7353, 0.6825), ('Maldon West (yard, S tunnel portal)', 51.7254, 0.6658), ('Barons Lane Halt', 51.6906, 0.6701),
      ('Cold Norton', 51.6718, 0.6738), ('Stow Maries Halt', 51.6612, 0.6514), ('South Woodham Ferrers', 51.6500, 0.6070)]
def me_shapes(E0, N1):
    """Maldon East drawn to scale: OSM building outline, 37 m frontage, 100 m platform (dimensions from the Maldon Reborn spec)."""
    fp = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'me_osm_footprint.json')))
    P = np.array(fp['bng'][:-1]); C = P.mean(0)
    u = np.array([-0.7107, 0.7035]); n = np.array([0.7035, 0.7107])            # long axis (NW) and its normal (NE)
    px = lambda q: [round(float(q[0] - E0), 1), round(float(N1 - q[1]), 1)]
    s_ = (P - C) @ n; ne, sw = s_.max(), s_.min()                                # NE wall = platform side, SW wall = street front
    uu = (P - C) @ u; se_end, nw_end = uu.min(), uu.max()                         # SE end (engine shed side) and NW end (Ulting side)
    front_mid = C + n * sw
    # Orientation from local knowledge: facing the building from the trackbed, Ulting/Witham are to the right (NW),
    # engine shed and Long Pond to the left (SE). Canopy starts at the SE gabled block and juts ~15 m past the NW end.
    canopy = [(se_end + 12.9, 0.7), (nw_end + 15, 0.7), (nw_end + 15, 3.8), (se_end + 12.9, 3.8), (se_end + 12.9, 0)]
    platform = [(se_end, 0), (se_end + 100, 0), (se_end + 100, 4.5), (se_end, 4.5), (se_end, 0)]
    shapes = [dict(kind='poly', label='Maldon East building (OSM outline, includes later additions)', pts=[px(q) for q in P] + [px(P[0])]),
              dict(kind='bar', label='frontage \u2248 37 m (street, SW wall)', pts=[px(front_mid - u * 18.5 - n * 2), px(front_mid + u * 18.5 - n * 2)]),
              dict(kind='poly', label='platform \u2248 100 m (inferred position)', pts=[px(C + u * sx + n * (ne + sy)) for sx, sy in platform]),
              dict(kind='poly', label='canopy (inferred): juts NW towards Ulting', pts=[px(C + u * sx + n * (ne + sy)) for sx, sy in canopy])]
    return shapes

out = []
for a in AREAS:
    z = window(a); nan = render(z, os.path.join(args.out, a['id'] + '.jpg'))
    E0, E1, N0, N1 = a['E0'], a['E0'] + SZ, a['N0'], a['N0'] + SZ
    m = (CE > E0 - 100) & (CE < E1 + 100) & (CN > N0 - 100) & (CN < N1 + 100)
    trace = [[round(float(x - E0), 1), round(float(N1 - y), 1)] for x, y in zip(CE[m][::2], CN[m][::2])]  # pixel coords
    pts = []
    for n, la, lo in ST:
        e, nn = bng(la, lo)
        if E0 <= e <= E1 and N0 <= nn <= N1: pts.append(dict(label=n, kind='station', x=round(e - E0), y=round(N1 - nn)))
    for s in structs:
        e, nn = float(s['easting']), float(s['northing'])
        if E0 <= e <= E1 and N0 <= nn <= N1: pts.append(dict(label=s['structure'] + ' (survey, ~70 m)', kind='survey', x=round(e - E0), y=round(N1 - nn)))
    shapes = me_shapes(E0, N1) if a['id'] == 'maldon' else []
    out.append(dict(shapes=shapes, id=a['id'], name=a['name'], blurb=a['blurb'], E0=E0, N1=N1, size=SZ, img=a['id'] + '.jpg', trace=trace, marks=pts, nodata=round(nan, 4)))
    print(a['id'], 'nodata fraction', round(nan, 4), 'trace pts', len(trace), 'marks', len(pts))
json.dump(out, open(os.path.join(args.out, 'areas.json'), 'w'))
print('wrote', args.out)

# page, assets and data downloads
import shutil
here = os.path.dirname(os.path.abspath(__file__))
shutil.copy(os.path.join(here, 'annotation_page.html'), os.path.join(args.out, 'index.html'))
dd = os.path.join(args.out, 'data'); os.makedirs(dd, exist_ok=True)
for f in ['wsw_centreline.csv', 'wsw_centreline.geojson', 'wsw_stations.csv', 'wsw_structures.csv', 'wsw_profile.png', 'README.md']:
    shutil.copy(os.path.join(args.data, f), dd)
print('page written')
