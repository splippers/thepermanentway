import csv,numpy as np
from pyproj import Transformer
t=Transformer.from_crs(27700,4326,always_xy=True)
# (name, parish, printed NGR, E, N, what the 2011 survey says)
S=[
("Woodham Ferrers junction (east of level crossing)","Woodham Ferrers","TQ805977",580500,197700,"Maldon branch diverged from the Southminster line immediately east of the level crossing; alignment now houses and property boundaries, plus a footpath north of Bancrofts Road"),
("Woodham Road bridge, Stow Maries","Stow Maries","TQ820987",582000,198700,"3-arched blue engineering brick bridge (bridge 833); cutting about 3 m below the field to the west; line preserved beneath the main arch"),
("Stow Maries culvert","Stow Maries","TQ824988",582400,198800,"Line marked by a strip of woodland; footbridge at TQ824989 shown c.1897 not extant"),
("Church Lane bridge / Stow St Mary Halt","Stow Maries","TQ835992",583500,199200,"Bridge of 3 segmental arches, blue engineering brick (bridge 836); halt platform was wooden sleepers; now a nature reserve; line in a woodland strip"),
("Pantile Wood embankment","Stow Maries","TQ837993",583700,199300,"Cutting gives way to an embankment; line preserved in a woodland strip"),
("Honey Pot Lane bridge","Stow Maries","TQ83994 (printed; read as TQ839994)",583900,199400,"Track crossed over the lane on a blue engineering brick bridge; only the two abutments remain (approximate position: survey NGR has five digits)"),
("St Stephens Road bridge, Cold Norton","Cold Norton","TQ846999",584600,199900,"Iron girder bridge with blue brick parapet (bridge 839); ground to the north raised about 3.5 m to form a front lawn"),
("Latchingdon Road bridge, Cold Norton","Cold Norton","TL849004",584900,200400,"Three 25.5 ft segmental arches, blue engineering brick with dentilled decoration (bridge 840); cutting partly filled in to the north by about 3 m"),
("The Street bridge, Purleigh","Purleigh","TL846021",584600,202100,"Embankment bridge; only the blue engineering brick abutments remain"),
("Barons Lane bridge and Halt","Purleigh","TL846024",584600,202400,"Girder and blue engineering brick bridge with blue brick copings; halt platform to the west of the track, north of the bridge, in a shallow cutting; access incline still extant in 2011"),
("Maldon West tunnel","Maldon","TL843064",584300,206400,"66 yard (21 m) tunnel under Spital Road, blocked at both ends in 2011; south portal balustrade intact; north end possibly beneath the bypass"),
("River Chelmer viaduct","Maldon","TL844076",584400,207600,"Brick arch and bowstring girder viaduct, 75 ft span, built 1889 (bridge 852), on an embankment; central span demolished 1965, piers 1989; replaced by a 1990 bypass bridge 1.8 m lower"),
("Chelmer & Blackwater Navigation west bridge","Maldon","TL846077",584600,207700,"Brick bridge on the double-track embankment; replaced by the bypass bridge"),
]
rows=[]
cl=list(csv.DictReader(open('/home/jon/tpw/data/alignments/wsw_centreline.csv')))
E=np.array([float(r['easting']) for r in cl]); N=np.array([float(r['northing']) for r in cl]); ch=np.array([float(r['chainage_m']) for r in cl])
for n,p,ngr,e,nn,desc in S:
    e+=50; nn+=50   # 6-figure grid refs name a 100 m square: use its centre
    lon,lat=t.transform(e,nn); d=np.hypot(E-e,N-nn); k=int(np.argmin(d))
    rows.append([n,p,ngr,e,nn,round(lat,6),round(lon,6),round(ch[k]),round(float(d[k])),desc])
    print('%-48s offset to traced line %4d m  (chainage %5d)'%(n,d[k],ch[k]))
with open('/home/jon/tpw/data/alignments/wsw_structures.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['structure','parish','survey_ngr','easting','northing','lat','lon','nearest_chainage_m','offset_from_traced_centreline_m','survey_description']); w.writerows(rows)
