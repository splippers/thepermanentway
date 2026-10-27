import numpy as np, json
from PIL import Image
def refine(g,pts,win=14,thr=110,side='min'):
    pts=np.array(pts,float); ys=np.arange(int(pts[0,1]),int(pts[-1,1])+1)
    xe=np.interp(ys,pts[:,1],pts[:,0]); out=[]
    for y,x in zip(ys,xe):
        row=g[y]; lo=int(max(0,x-win)); hi=int(min(len(row),x+win+1)); cand=[xx for xx in range(lo,hi) if row[xx]<thr]
        out.append(((min(cand) if side=='min' else max(cand)) if cand else x))
    out=np.array(out,float)
    from scipy.ndimage import median_filter,gaussian_filter
    out=median_filter(out,31,mode='nearest'); c=np.polyfit(ys,out,3); out=np.polyval(c,ys)
    return [(float(a),float(b)) for a,b in zip(out[::5],ys[::5])]
gA=np.array(Image.open('mwA_raw.png').convert('L')).astype(float)
west=[(137,0),(150,60),(165,125),(180,190),(195,260),(210,350),(227,430),(235,487)]
east=[(371,5),(375,120),(383,230),(390,300),(398,360),(402,415)]
E1=refine(gA,west,side='min')
E2=refine(gA,[(383,170),(383,230),(390,300),(398,360),(402,415)],side='max')
import numpy as np
a=np.array(E2); c=np.polyfit(a[:40,1],a[:40,0],1); yy=np.arange(0,170,5); E2=[(float(np.polyval(c,y)),float(y)) for y in yy]+E2
json.dump({'cut_west_top':E1,'cut_east_top':E2},open('edgesA.json','w'))
from PIL import ImageDraw
im=Image.open('mwA_raw.png').convert('RGB').resize((820*2,783*2)); d=ImageDraw.Draw(im)
for E in (E1,E2): d.line([(a*2,b*2) for a,b in E],fill=(0,0,255),width=3)
im.crop((100,0,900,1000)).save('edgeqa.png')
