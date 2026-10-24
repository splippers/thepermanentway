"""Snap the route to the LIDAR using OpenStreetMap's abandoned-railway line only as a guide."""
import json,numpy as np
from pyproj import Transformer
from scipy.ndimage import gaussian_filter,map_coordinates
t=Transformer.from_crs(4326,27700,always_xy=True)
ways={}
for e in json.load(open('osm.json'))['elements']:
    g=e['geometry']; xs,ys=t.transform([p['lon'] for p in g],[p['lat'] for p in g]); ways[e['id']]=np.c_[xs,ys]
def w(i,rev=False): return ways[i][::-1] if rev else ways[i]
chain=[w(160283203,True),w(104259930,True),w(104259933,True),w(103912715,True),w(103912716,True),w(103912717,True),w(103912718,True),w(170867842,True),
       w(1025555601,True),w(1025555600,True),w(1025555602,True),w(108177657)[8:],w(160284674),w(160284678),w(160284664),w(160284676),w(160284296)]
guide=[]
for c in chain:
    for p in c:
        if not guide or np.hypot(*(p-guide[-1]))>1: guide.append(p)
guide=np.array(guide)
from wcs import bng
ws=np.array(bng(51.8060,0.6391)); k0=int(np.argmin(np.hypot(*(guide-ws).T))); guide=guide[k0:]   # start at Witham station
print('guide points',len(guide),'length m',round(float(np.sum(np.hypot(*np.diff(guide,axis=0).T)))))
a=np.load('mosaic.npy'); m=json.load(open('mosaic.json')); e0,n1=m['e0'],m['n1']
S=2; b=a[::S,::S]; ok=~np.isnan(b); bn=np.nan_to_num(b,nan=np.nanmean(b))
strength=np.minimum(gaussian_filter(np.abs(bn-gaussian_filter(bn,6)),1.0),2.0)*ok
def sample(E,N):
    r=(n1-N)/S; c=(E-e0)/S; return map_coordinates(strength,[r,c],order=1,mode='constant',cval=0)
d=np.r_[0,np.cumsum(np.hypot(*np.diff(guide,axis=0).T))]; s=np.arange(0,d[-1],10.0)
pts=np.c_[np.interp(s,d,guide[:,0]),np.interp(s,d,guide[:,1])]
tg=np.gradient(pts,axis=0); tg/=np.hypot(*tg.T)[:,None]; nr=np.c_[-tg[:,1],tg[:,0]]
offs=np.arange(-25,25.1,2.0); K=len(offs)
U=np.zeros((len(pts),K))
for k,o in enumerate(offs):
    q=pts+nr*o; acc=0
    for tt in (-20,-10,0,10,20): qq=q+tg*tt; acc=acc+sample(qq[:,0],qq[:,1])
    U[:,k]=acc/5-0.004*abs(o)              # stay near the guide unless the terrain clearly says otherwise
maxj=2; lam=0.05
cost=-U.copy(); back=np.zeros((len(pts),K),int)
for i in range(1,len(pts)):
    prev=cost[i-1]; best=np.full(K,1e9); arg=np.zeros(K,int)
    for dj in range(-maxj,maxj+1):
        sh=np.full(K,1e9)
        if dj>0: sh[dj:]=prev[:K-dj]
        elif dj<0: sh[:dj]=prev[-dj:]
        else: sh=prev.copy()
        c=sh+lam*(dj*2.0)**2/2.0; mk=c<best; best[mk]=c[mk]; arg[mk]=(np.arange(K)-dj)[mk]
    cost[i]=best-U[i]; back[i]=arg
k=int(np.argmin(cost[-1])); idx=[k]
for i in range(len(pts)-1,0,-1): k=back[i][k]; idx.append(k)
idx=idx[::-1]
line=pts+nr*offs[idx][:,None]; st=np.array([max(0,U[i,idx[i]]+0.004*abs(offs[idx[i]])) for i in range(len(pts))])
print('mean lateral shift from OSM guide %.1f m; max %.0f m; mean strength %.2f'%(np.mean(np.abs(offs[idx])),np.max(np.abs(offs[idx])),st.mean()))
np.save('line_en.npy',line); np.save('line_strength.npy',st)
