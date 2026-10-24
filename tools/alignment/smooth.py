import numpy as np,json
from scipy.interpolate import splprep,splev
from scipy.ndimage import uniform_filter1d
line=np.load('line_en.npy'); u=np.load('line_strength.npy')
d=np.r_[0,np.cumsum(np.hypot(*np.diff(line,axis=0).T))]
# confidence: local mean of ridge strength over ~200 m, so isolated strong spots do not count
c=uniform_filter1d(u,9,mode='nearest'); c=np.clip(c/0.8,0,1)
sigma=2.5+120*(1-c)**3          # metres of lateral slack: tight where the ridge is clear, loose where it is not
sigma=np.maximum(sigma,2.5)
tck,uu=splprep([line[:,0],line[:,1]],w=1/sigma,s=len(line)*1.0,k=3)
t=np.linspace(0,1,6000); x,y=splev(t,tck); dx,dy=splev(t,tck,der=1); ddx,ddy=splev(t,tck,der=2)
curv=(dx*ddy-dy*ddx)/(dx*dx+dy*dy)**1.5
L=np.r_[0,np.cumsum(np.hypot(np.diff(x),np.diff(y)))]
R=1/np.maximum(np.abs(curv),1e-9)
print('length m',round(L[-1]),' min radius m %.0f  p5 radius %.0f'%(R.min(),np.percentile(R,5)))
for lo,hi in [(0,3000),(3000,6000),(6000,9000),(9000,12000),(12000,15000),(15000,18000),(18000,21500)]:
    m=(L>=lo)&(L<hi)
    if m.any(): print(lo,hi,'min R %.0f'%R[m].min())
np.save('line_smooth.npy',np.c_[x,y]); np.save('line_conf.npy',np.interp(L,d*L[-1]/d[-1],c))
