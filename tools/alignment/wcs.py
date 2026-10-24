import sys,urllib.request,urllib.parse
from pyproj import Transformer
t=Transformer.from_crs(4326,27700,always_xy=True)
def bng(lat,lon): return t.transform(lon,lat)
COV='13787b9a-26a4-4775-8523-806d13af58fc__Lidar_Composite_Elevation_DTM_1m'
def fetch(e0,n0,e1,n1,out,scale=None):
    q=[('service','WCS'),('version','2.0.1'),('request','GetCoverage'),('coverageId',COV),
       ('format','image/tiff'),('subset','E(%d,%d)'%(e0,e1)),('subset','N(%d,%d)'%(n0,n1))]
    url='https://environment.data.gov.uk/spatialdata/lidar-composite-digital-terrain-model-dtm-1m-2022/wcs?'+urllib.parse.urlencode(q)
    r=urllib.request.Request(url,headers={'User-Agent':'tpw-research/1.0 (jon@splippers.com)'})
    d=urllib.request.urlopen(r,timeout=120).read()
    open(out,'wb').write(d); return len(d)
if __name__=='__main__':
    lat,lon,half,out=float(sys.argv[1]),float(sys.argv[2]),int(sys.argv[3]),sys.argv[4]
    e,n=bng(lat,lon); print('BNG',round(e),round(n))
    print(fetch(round(e)-half,round(n)-half,round(e)+half,round(n)+half,out),'bytes')
