#!/home/mzamith/Apps/anaconda3/bin/python
from pyproj import Proj, transform

outProj = Proj(init='epsg:4326')
inProj = Proj(init='epsg:3857') # It is equal to WSG

x1,y1 = 100.0, 100.0
x2,y2 = transform(inProj,outProj,x1,y1)
print ("Coordenate(", x2, ",", y2, ")")

