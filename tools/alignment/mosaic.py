import glob,numpy as np,rasterio
from rasterio.merge import merge
fs=sorted(glob.glob('tiles/*.tif'))
srcs=[rasterio.open(f) for f in fs]
arr,tr=merge(srcs,nodata=-9999)
a=arr[0].astype('float32'); a[a<-1e30]=np.nan; a[a==-9999]=np.nan
print('mosaic',a.shape,'cells',a.size)
np.save('mosaic.npy',a); import json; json.dump({'e0':tr.c,'n1':tr.f},open('mosaic.json','w'))
tile_nan=[]
for f,s in zip(fs,srcs):
    t=s.read(1).astype('float32'); t[t<-1e30]=np.nan
    tile_nan.append((f,float(np.isnan(t).mean()),float(np.nanstd(t))))
print('tiles with any nodata:',[(f.split('/')[1],round(p,3)) for f,p,_ in tile_nan if p>0])
print('overall nodata fraction in tiles:',round(float(np.mean([p for _,p,_ in tile_nan])),4))
print('elev range',float(np.nanmin(a)),float(np.nanmax(a)))
