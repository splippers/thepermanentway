import json, math
exec(open('mwfeat.py').read())
from pyproj import Transformer
Z=18;N=2**Z
tr=Transformer.from_crs(4326,27700,always_xy=True)
def unmer(x,y):
    lon=x/(N*256)*360-180; lat=math.degrees(math.atan(math.sinh(math.pi*(1-2*y/(N*256))))); return lat,lon
OA=(33678173,22249329); OY=(33678173,22249841)
def conv(pts,o):
    out=[]
    for a,b in pts:
        lat,lon=unmer(a+o[0],b+o[1]); e,n=tr.transform(lon,lat); out.append((lon,lat,e,n))
    return out
kinds={'platform':'platform','canopy':'platform canopy / covered area (hatched on OS)','building':'building (hatched on OS)','annex':'building (hatched on OS)','booking':'booking office (probable; road-level building)','bridge':'road overbridge / tunnel mouth structure (hatched on OS)','stairs':'stairs / passage between road and platform (probable)','goods_shed':'goods shed','shed_office':'small building by goods shed','signal_box':'signal box (S.B.)','weighing_machine':'weighing machine (W.M.)','end_side_dock':'end and side dock (unhatched outline)','house':'house/cottage by Spital Road','cottage':'house/cottage by Spital Road'}
def kind(k):
    for kk,v in kinds.items():
        if kk in k: return v
    return k
feats=[]
def add(name,pts,o,geom='Polygon',extra=None):
    c=conv(pts,o)
    ring=[(x,y) for x,y,_,_ in c]
    g={'type':'Polygon','coordinates':[ring+[ring[0]]]} if geom=='Polygon' else {'type':'LineString','coordinates':ring}
    props={'name':name,'kind':kind(name),'bng':[(round(e,2),round(n,2)) for _,_,e,n in c]}
    if extra: props.update(extra)
    feats.append({'type':'Feature','geometry':g,'properties':props})
for k,p in F.items(): add(k,p,OA)
for k,p in Y.items(): add(k,p,OY)
E=json.load(open('edgesA.json'))
for k,p in E.items(): add(k,p,OA,'LineString')
add('tunnel_south_portal_structure',[(325,102),(415,100),(417,112),(326,122)],OY)
meta={'type':'FeatureCollection','name':'Maldon West station, 1890s layout traced from OS 25-inch (Essex), via NLS',
 'attribution':'Ordnance Survey 25-inch map of Essex (1890s), reproduced courtesy of the National Library of Scotland, https://maps.nls.uk. Tracing by The Permanent Way; accuracy about 1-2 m, drawn by eye from georeferenced tiles.',
 'features':feats}
json.dump(meta,open('mw_1890s_footprints.geojson','w'))
# dimensions report (BNG metres)
import numpy as np
def dims(name):
    f=[x for x in feats if x['properties']['name']==name][0]; P=np.array(f['properties']['bng'])
    c=P.mean(0); u,s,vt=np.linalg.svd(P-c); pr=(P-c)@vt.T; return (pr.max(0)-pr.min(0))
for n in ('west_platform','east_platform','west_canopy','east_canopy','east_building','booking_office','goods_shed','signal_box','shed_office','end_side_dock'):
    d=dims(n); print(n,'%.1f x %.1f m'%(max(d),min(d)))
