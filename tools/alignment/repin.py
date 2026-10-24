import numpy as np
from wcs import bng
from scipy.interpolate import splprep,splev
line=np.load('line_en_orig.npy'); u=np.load('line_strength_orig.npy')
# survey positions (centre of the 100 m grid square) and station coordinates
EAST=bng(51.7353,0.6825)                 # Maldon East station (Wikipedia)
WEST=bng(51.7262,0.6659)                 # Maldon West station (Wikipedia)
NAV=(584650,207750); VIA=(584450,207650)  # Navigation west bridge, Chelmer viaduct (ESAH survey, TL846077 / TL844076)
i_e=int(np.argmin(np.hypot(*(line-np.array(NAV)).T)));   # trunk leaves the Witham line near the Navigation bridge; Maldon East is a spur
i_w=int(np.argmin(np.hypot(*(line-np.array(WEST)).T)))
print('indices',i_e,i_w,len(line))
pins=np.array([line[i_e],NAV,VIA,WEST],float)
t=np.r_[0,np.cumsum(np.hypot(*np.diff(pins,axis=0).T))]
tck,_=splprep([pins[:,0],pins[:,1]],k=3,s=0,u=t/t[-1])
n=int(t[-1]//20)+2; x,y=splev(np.linspace(0,1,n),tck)
new=np.c_[x,y]
out=np.vstack([line[:i_e],new,line[i_w+1:]])
st=np.r_[u[:i_e],np.full(n,0.55),u[i_w+1:]]       # moderate confidence on the pinned link
np.save('line_en.npy',out); np.save('line_strength.npy',st)
print('replaced',i_w-i_e+1,'points by',n,'; new length',round(float(np.sum(np.hypot(*np.diff(out,axis=0).T)))))
