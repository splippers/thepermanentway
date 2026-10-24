import numpy as np,json,csv,math,scipy.sparse as sp
from scipy.sparse.linalg import spsolve
from scipy.ndimage import map_coordinates
from pyproj import Transformer
from wcs import bng
import os; OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','data','alignments')+os.sep
a=np.load('mosaic.npy'); m=json.load(open('mosaic.json')); e0,n1=m['e0'],m['n1']
line=np.load('line_smooth.npy'); conf_l=np.load('line_conf.npy')
d=np.r_[0,np.cumsum(np.hypot(*np.diff(line,axis=0).T))]
h=5.0; s=np.arange(0,d[-1],h)
E=np.interp(s,d,line[:,0]); N=np.interp(s,d,line[:,1]); conf=np.interp(s,d,conf_l)
tang=np.gradient(np.c_[E,N],axis=0); tang/=np.hypot(*tang.T)[:,None]; nrm=np.c_[-tang[:,1],tang[:,0]]
an=np.nan_to_num(a,nan=-9999)
zs=[map_coordinates(an,[n1-(N+nrm[:,1]*o),(E+nrm[:,0]*o)-e0],order=1) for o in (-1.5,0,1.5)]
z=np.median(zs,axis=0); z[z<-1000]=np.nan
n=len(s); D2=sp.diags([1.,-2.,1.],[0,1,2],shape=(n-2,n))/h**2
def fit(z,lam=60.0,iters=40,tuk=0.35):
    w=np.ones(n); v=np.ones(n-2)
    for _ in range(iters):
        f=spsolve((sp.diags(w)+lam*D2.T@sp.diags(v)@D2).tocsc(),w*z)
        r=z-f; w=np.clip(1-(r/tuk)**2,0,1)**2+1e-4; v=1.0/(np.abs(D2@f)+1e-4)
    return f,w
f,w=fit(z)
rejected=w<0.05
g=np.gradient(f,h)*100
# railway-like check: a branch line cannot sustain steep grades; those stretches are not trusted
steep=np.abs(g)>3.0
flag=np.zeros(n,int)      # 0 measured, 1 interpolated (outlier rejected), 2 not railway-like (replaced by straight grade)
flag[rejected]=1
i=0
while i<n:
    if steep[i]:
        j=i
        while j<n and steep[j]: j+=1
        if (j-i)*h>=60:
            lo=max(i-5,0); hi=min(j+5,n-1)
            f[lo:hi+1]=np.interp(s[lo:hi+1],[s[lo],s[hi]],[f[lo],f[hi]]); flag[lo:hi+1]=2
        i=j
    else: i+=1
g=np.gradient(f,h)*100
t=Transformer.from_crs(27700,4326,always_xy=True); lon,lat=t.transform(E,N)
with open(OUT+'wsw_centreline.csv','w',newline='') as fh:
    w_=csv.writer(fh); w_.writerow(['chainage_m','easting','northing','lat','lon','z_raw_m','z_fit_m','gradient_pct','trace_confidence','flag'])
    for k in range(n): w_.writerow([round(s[k],1),round(E[k],1),round(N[k],1),round(lat[k],6),round(lon[k],6),round(float(z[k]),2),round(float(f[k]),2),round(float(g[k]),2),round(float(conf[k]),2),['measured','interpolated','not_railway_like'][flag[k]]])
json.dump({'type':'Feature','properties':{'name':'Witham - Maldon - South Woodham Ferrers (traced from LIDAR)'},'geometry':{'type':'LineString','coordinates':[[round(float(x),6),round(float(y),6),round(float(zz),2)] for x,y,zz in zip(lon,lat,f)]}},open(OUT+'wsw_centreline.geojson','w'))
ST=[('Witham',51.8060,0.6391),('Wickham Bishops',51.7732,0.6431),('Langford & Ulting',51.7480,0.6666),('Maldon East & Heybridge',51.7353,0.6825),('Maldon West',51.7262,0.6659),('Barons Lane Halt',51.6906,0.6701),('Cold Norton',51.6718,0.6738),('Stow Maries Halt',51.6612,0.6514),('South Woodham Ferrers',51.6500,0.6070)]
rows=[]
for nm,la,lo in ST:
    pe,pn=bng(la,lo); dist=np.hypot(E-pe,N-pn); k=int(np.argmin(dist))
    rows.append((nm,round(s[k]),round(float(dist[k])),round(float(lat[k]),6),round(float(lon[k]),6),round(float(f[k]),1),round(float(conf[k]),2),['measured','interpolated','not_railway_like'][flag[k]]))
with open(OUT+'wsw_stations.csv','w',newline='') as fh:
    w_=csv.writer(fh); w_.writerow(['station','chainage_m','offset_from_wikipedia_coord_m','lat_on_centreline','lon_on_centreline','z_fit_m','trace_confidence','profile_flag']); w_.writerows(rows)
for r in rows: print(r)
print('length',round(s[-1]),'flags: measured %d%% interpolated %d%% not_railway_like %d%%'%tuple(100*np.mean(flag==q) for q in (0,1,2)))
print('max |grade| %.2f%%  median %.2f%%'%(np.abs(g).max(),np.median(np.abs(g))))
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig,ax=plt.subplots(2,1,figsize=(14,7.5),sharex=True)
ax[0].plot(s/1000,z,'.',ms=2,color='0.65',label='raw LIDAR height along the traced line')
ax[0].plot(s[flag==0]/1000,f[flag==0],'r.',ms=2,label='fitted profile (measured)')
ax[0].plot(s[flag==1]/1000,f[flag==1],'.',ms=3,color='orange',label='interpolated from neighbours (trees, roads, bridges rejected)')
ax[0].plot(s[flag==2]/1000,f[flag==2],'.',ms=3,color='purple',label='not railway-like: straight grade between trusted ends')
for nm,ch,*_ in rows: ax[0].axvline(ch/1000,color='k',lw=.4); ax[0].text(ch/1000,ax[0].get_ylim()[1]*0.97,nm,rotation=90,fontsize=7,va='top')
ax[0].set_ylabel('height (m)'); ax[0].legend(loc='upper right',fontsize=7)
ax[1].plot(s/1000,g,'b-',lw=.8); ax[1].axhline(0,color='k',lw=.5); ax[1].set_ylabel('gradient (%)'); ax[1].set_xlabel('chainage from Witham end (km)')
plt.suptitle('Witham - Maldon - South Woodham Ferrers: profile from LIDAR (contains Environment Agency information, OGL)',fontsize=9)
plt.tight_layout(); plt.savefig(OUT+'wsw_profile.png',dpi=80)
