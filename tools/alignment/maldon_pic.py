import numpy as np,json,csv
from scipy.ndimage import gaussian_filter
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
from wcs import bng
a=np.load('mosaic.npy'); m=json.load(open('mosaic.json')); e0,n1=m['e0'],m['n1']
E0,E1,N0,N1=584000,585800,206200,208000       # 1.8 km square
c0,c1=int(E0-e0),int(E1-e0); r0,r1=int(n1-N1),int(n1-N0)
sub=a[r0:r1,c0:c1].copy()
print('window',sub.shape,'nan',int(np.isnan(sub).sum()))
fill=np.nanmean(sub); sn=np.nan_to_num(sub,nan=fill)
lrm=sn-gaussian_filter(sn,12)
ls=LightSource(azdeg=315,altdeg=40); hs=ls.hillshade(sn,vert_exag=4,dx=1,dy=1)
cl=list(csv.DictReader(open('/home/jon/tpw/data/alignments/wsw_centreline.csv')))
CE=np.array([float(r['easting']) for r in cl]); CN=np.array([float(r['northing']) for r in cl])
inside=(CE>E0-50)&(CE<E1+50)&(CN>N0-50)&(CN<N1+50)
ST={'Maldon East & Heybridge station':bng(51.7353,0.6825),'Maldon West station':bng(51.7262,0.6659)}
STR={'Chelmer viaduct (survey)':(584450,207650),'Navigation west bridge (survey)':(584650,207750),'Maldon West tunnel (survey)':(584350,206450)}
def base(ax,show_trace,labels):
    ax.imshow(hs,cmap='gray',extent=[E0,E1,N0,N1],vmin=0.2,vmax=1.0,alpha=1.0)
    ax.imshow(lrm,cmap='RdBu_r',vmin=-2,vmax=2,extent=[E0,E1,N0,N1],alpha=0.35)
    ax.set_xticks(range(E0,E1+1,100)); ax.set_yticks(range(N0,N1+1,100))
    ax.set_xticklabels([str(x) if (x//100)%2==0 else '' for x in range(E0,E1+1,100)],fontsize=7,rotation=90)
    ax.set_yticklabels([str(y) if (y//100)%2==0 else '' for y in range(N0,N1+1,100)],fontsize=7)
    ax.grid(color='yellow',lw=0.35,alpha=0.55)
    ax.set_xlim(E0,E1); ax.set_ylim(N0,N1)
    if show_trace:
        ax.plot(CE[inside],CN[inside],'-',color='lime',lw=1.4,label='my trace (wsw_centreline.csv)')
        ax.plot(CE[inside],CN[inside],'-',color='k',lw=0.4)
    if labels:
        for n,(x,y) in ST.items(): ax.plot(x,y,'o',color='magenta',ms=6); ax.text(x+15,y+10,n,color='magenta',fontsize=8,backgroundcolor=(0,0,0,0.45))
        for n,(x,y) in STR.items(): ax.plot(x,y,'s',color='cyan',ms=5); ax.text(x+15,y-30,n,color='cyan',fontsize=7,backgroundcolor=(0,0,0,0.45))
    ax.set_xlabel('Easting (British National Grid, m); grid every 100 m',fontsize=8); ax.set_ylabel('Northing (m)',fontsize=8)
for name,trace,labels in [('maldon_with_trace',True,True),('maldon_clean',False,False)]:
    fig=plt.figure(figsize=(12,12.4),dpi=100); ax=fig.add_axes([0.07,0.05,0.92,0.92])
    base(ax,trace,labels)
    ax.set_title('Maldon East (right) to Maldon West (bottom): LIDAR 1 m terrain. Contains Environment Agency information, OGL'+(' | green = my trace' if trace else ' | clean copy for drawing'),fontsize=8)
    fig.savefig(name+'.png'); plt.close(fig)
# world file for a pixel-exact version of the clean data (hillshade only, 1 px = 1 m)
img=(hs*255).astype('uint8')
from PIL import Image
Image.fromarray(img).save('maldon_hillshade_1m.png')
open('maldon_hillshade_1m.pgw','w').write('1.0\n0.0\n0.0\n-1.0\n%.1f\n%.1f\n'%(E0+0.5,N1-0.5))
print('ok')
