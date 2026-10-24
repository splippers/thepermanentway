import os,math,numpy as np
from wcs import bng,fetch
ST=[(51.8060,0.6391),(51.7732,0.6431),(51.7480,0.6666),(51.7353,0.6825),(51.7262,0.6659),(51.6906,0.6701),(51.6718,0.6738),(51.6612,0.6514),(51.6500,0.6070)]
P=[bng(a,b) for a,b in ST]
# densify polyline every 100 m, collect 1 km tiles within 700 m of it
pts=[]
for (x0,y0),(x1,y1) in zip(P,P[1:]):
    n=int(math.hypot(x1-x0,y1-y0)//100)+1
    for i in range(n): pts.append((x0+(x1-x0)*i/n,y0+(y1-y0)*i/n))
pts.append(P[-1])
tiles=set()
for x,y in pts:
    for dx in (-700,0,700):
        for dy in (-700,0,700):
            tiles.add((int((x+dx)//1000)*1000,int((y+dy)//1000)*1000))
tiles=sorted(tiles); print(len(tiles),'tiles')
os.makedirs('tiles',exist_ok=True)
for e,n in tiles:
    f='tiles/%d_%d.tif'%(e,n)
    if not os.path.exists(f):
        try: fetch(e,n,e+1000,n+1000,f)
        except Exception as ex: print('fail',e,n,ex)
print('done')
