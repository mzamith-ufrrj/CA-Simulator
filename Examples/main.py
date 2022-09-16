#   Requires:  pip install pyproj

from pyproj import Proj, transform
'''
inProj = Proj(init='epsg:3857')
outProj = Proj(init='epsg:4326') # It is equal to WSG
x1,y1 = -11705274.6374,4826473.6922
x2,y2 = transform(inProj,outProj,x1,y1)
print (x2)
print(y2)
'''
#long == x
#lat == y
'''
outProj = Proj(init='epsg:3857')
inProj = Proj(init='epsg:4326') # It is equal to WSG
x1,y1 = -43.205259, -22.814786
x2,y2 = transform(inProj,outProj,x1,y1)
print ("Coordenate(", x2, ",", y2, ")")
'''
outProj = Proj(init='epsg:3857')
inProj = Proj(init='epsg:4326') # It is equal to WSG

x1,y1 = -43.459335, -22.742368
x2,y2 = transform(inProj,outProj,x1,y1)
print ("Coordenate(", x2, ",", y2, ")")

inProj = Proj(init='epsg:3857')
outProj = Proj(init='epsg:4326') # It is equal to WSG
x3,y3 = transform(inProj,outProj,x2,y2)

x4,y4 = transform(inProj,outProj,x2+50,y2)
x5,y5 = transform(inProj,outProj,x2-50,y2)
x6,y6 = transform(inProj,outProj,x2,y2+50)
x7,y7 = transform(inProj,outProj,x2,y2-50)

print ("06,QUAD,RECTANGLE(", x4, " ", y4, ",", x7, " ", y7, ",", x5, " ", y5, ",", x6, " ", y6, ")")
