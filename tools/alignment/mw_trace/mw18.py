import math,os,sys,numpy as np
from PIL import Image, ImageDraw, ImageFont
Z=18;N=2**Z
def mer(lat,lon): return ((lon+180)/360*N*256,(1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*N*256)
def unmer(x,y): return (math.degrees(math.atan(math.sinh(math.pi*(1-2*y/(N*256))))),x/(N*256)*360-180)
def canvas(lat0,lon0,lat1,lon1):
    xa,ya=mer(lat0,lon0); xb,yb=mer(lat1,lon1)
    x0,x1=int(min(xa,xb)),int(max(xa,xb)); y0,y1=int(min(ya,yb)),int(max(ya,yb))
    W=Image.new('RGB',(x1-x0,y1-y0),'white')
    for tx in range(x0//256,x1//256+1):
        for ty in range(y0//256,y1//256+1):
            f=f'os25/t/{Z}_{tx}_{ty}.png'
            if not os.path.exists(f):
                import subprocess
                subprocess.run(['curl','-s','-m','30','-A','thepermanentway-research/0.1','-o',f,f'https://mapseries-tilesets.s3.amazonaws.com/25_inch/essex/{Z}/{tx}/{ty}.png'])
            try:
                im=Image.open(f).convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im)
                W.paste(bg.convert('RGB'),(tx*256-x0,ty*256-y0))
            except Exception: pass
    return W,x0,y0
def grid(W,step,scale,name):
    im=W.resize((W.width*scale,W.height*scale),Image.LANCZOS); d=ImageDraw.Draw(im,'RGBA'); f=ImageFont.load_default(size=15)
    for g in range(0,W.width,step):
        d.line([(g*scale,0),(g*scale,im.height)],fill=(0,160,0,80)); d.text((g*scale+2,2),str(g),fill=(0,110,0,255),font=f)
    for g in range(0,W.height,step):
        d.line([(0,g*scale),(im.width,g*scale)],fill=(0,160,0,80)); d.text((2,g*scale+2),str(g),fill=(0,110,0,255),font=f)
    im.save(name)
if __name__=='__main__':
    W,x0,y0=canvas(51.7275,0.6638,51.7249,0.6682)   # station + tunnel
    print(W.size,x0,y0); W.save('mwA_raw.png'); grid(W,50,2,'mwA_grid.png')
