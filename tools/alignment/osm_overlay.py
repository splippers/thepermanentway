import json,csv,numpy as np
from pyproj import Transformer
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
from scipy.ndimage import gaussian_filter
t=Transformer.from_crs(4326,27700,always_xy=True)
d=json.load(open('osm.json'))['elements']
a=np.load('mosaic.npy'); m=json.load(open('mosaic.json')); e0,n1=m['e0'],m['n1']
E0,E1,N0,N1=584000,585800,206200,208000
sub=a[int(n1-N1):int(n1-N0),int(E0-e0):int(E1-e0)]; sn=np.nan_to_num(sub,nan=np.nanmean(sub))
hs=LightSource(315,40).hillshade(sn,vert_exag=4,dx=1,dy=1)
cl=list(csv.DictReader(open('/home/jon/tpw/data/alignments/wsw_centreline.csv')))
CE=np.array([float(r['easting']) for r in cl]); CN=np.array([float(r['northing']) for r in cl])
fig=plt.figure(figsize=(12,12.4),dpi=100); ax=fig.add_axes([0.07,0.05,0.92,0.92])
ax.imshow(hs,cmap='gray',extent=[E0,E1,N0,N1],vmin=0.2,vmax=1.0)
n=0
for e in d:
    xs,ys=t.transform([p['lon'] for p in e['geometry']],[p['lat'] for p in e['geometry']])
    if max(xs)<E0-100 or min(xs)>E1+100 or max(ys)<N0-100 or min(ys)>N1+100: continue
    n+=1; ax.plot(xs,ys,'-',color='orange',lw=2.2)
    tg=e['tags']; ax.text(xs[len(xs)//2]+10,ys[len(ys)//2],tg.get('railway','')+(' '+tg['name'] if 'name' in tg else ''),fontsize=7,color='orange',backgroundcolor=(0,0,0,.5))
ax.plot(CE,CN,'-',color='lime',lw=1.4)
ax.set_xlim(E0,E1); ax.set_ylim(N0,N1); ax.set_xticks(range(E0,E1+1,100)); ax.set_yticks(range(N0,N1+1,100)); ax.grid(color='yellow',lw=.35,alpha=.5)
ax.set_xticklabels([str(x) if (x//100)%2==0 else '' for x in range(E0,E1+1,100)],fontsize=7,rotation=90); ax.set_yticklabels([str(y) if (y//100)%2==0 else '' for y in range(N0,N1+1,100)],fontsize=7)
ax.set_title('orange = OpenStreetMap abandoned/razed railway (c) OpenStreetMap contributors, ODbL | green = my LIDAR trace',fontsize=8)
fig.savefig('maldon_osm.png'); print('ways in window',n)
