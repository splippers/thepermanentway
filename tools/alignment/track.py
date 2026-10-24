import numpy as np,json,math
from scipy.ndimage import gaussian_filter,map_coordinates,maximum_filter
from scipy.interpolate import splprep,splev
from wcs import bng
a=np.load('mosaic.npy'); m=json.load(open('mosaic.json')); e0,n1=m['e0'],m['n1']
S=2
b=a[::S,::S]; bn=np.nan_to_num(b,nan=np.nanmean(b)); lrm=bn-gaussian_filter(bn,6)
strength=gaussian_filter(np.abs(lrm),1.0)
strength=np.minimum(strength,2.0)
ST=[('Witham',51.8060,0.6391),('Wickham Bishops',51.7732,0.6431),('Langford & Ulting',51.7480,0.6666),('Maldon East & Heybridge',51.7353,0.6825),('Maldon West',51.7262,0.6659),('Barons Lane Halt',51.6906,0.6701),('Cold Norton',51.6718,0.6738),('Stow Maries Halt',51.6612,0.6514),('South Woodham Ferrers',51.6500,0.6070)]
P=np.array([bng(la,lo) for _,la,lo in ST])      # E,N
def to_rc(E,N): return (n1-N)/S,(E-e0)/S
def sample(E,N): 
    r,c=to_rc(E,N); return map_coordinates(strength,[r,c],order=1,mode='nearest')
def resample(poly,step):
    d=np.r_[0,np.cumsum(np.hypot(*np.diff(poly,axis=0).T))]; s=np.arange(0,d[-1],step)
    return np.c_[np.interp(s,d,poly[:,0]),np.interp(s,d,poly[:,1])],s
def viterbi(poly,half,dstep=3,step=40,maxjump=20,lam=0.02,wind=None):
    pts,s=resample(poly,step)
    tang=np.gradient(pts,axis=0); tang/=np.hypot(*tang.T)[:,None]; nrm=np.c_[-tang[:,1],tang[:,0]]
    offs=np.arange(-half,half+1e-6,dstep); K=len(offs)
    U=np.zeros((len(pts),K))
    for k,o in enumerate(offs):
        q=pts+nrm*o
        # integrate strength along +-20 m of track direction to favour long continuous features
        acc=0
        for t in (-20,-10,0,10,20):
            qq=q+tang*t; acc=acc+sample(qq[:,0],qq[:,1])
        U[:,k]=acc/5
    maxj=int(maxjump/dstep)
    cost=-U.copy(); back=np.zeros((len(pts),K),int); 
    for i in range(1,len(pts)):
        prev=cost[i-1]; best=np.full(K,1e9); arg=np.zeros(K,int)
        for dj in range(-maxj,maxj+1):
            sh=np.full(K,1e9); 
            if dj>=0: sh[dj:]=prev[:K-dj] if dj>0 else prev
            else: sh[:dj]=prev[-dj:]
            c=sh+lam*(dj*dstep)**2/ max(dstep,1)
            m_=c<best; best[m_]=c[m_]; arg[m_]=(np.arange(K)-dj)[m_]
        cost[i]=best+(-U[i]); back[i]=arg
    k=int(np.argmin(cost[-1])); idx=[k]
    for i in range(len(pts)-1,0,-1): k=back[i][k]; idx.append(k)
    idx=idx[::-1]
    return pts+nrm*offs[idx][:,None],U[np.arange(len(pts)),idx]
poly=P.copy()
line,u=viterbi(poly,half=300)
for it,(half,lam) in enumerate([(120,0.05),(50,0.12),(25,0.2)]):
    sm=np.c_[gaussian_filter(line[:,0],4,mode='nearest'),gaussian_filter(line[:,1],4,mode='nearest')]
    line,u=viterbi(sm,half=half,dstep=2,step=20,maxjump=8,lam=lam)
np.save('line_en.npy',line); np.save('line_strength.npy',u)
r,c=to_rc(line[:,0],line[:,1]); np.save('path_pix2.npy',np.c_[r,c])
L=np.sum(np.hypot(*np.diff(line,axis=0).T)); print('points',len(line),'length m',round(L),'mean strength',round(float(u.mean()),2))
