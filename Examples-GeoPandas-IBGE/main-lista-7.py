import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from pyproj import Transformer
import math
import sys
#-------------------------------------------------------------------------------
'''
p1 and p2 are polygon Coordinate
p4x is maximum value used to cal if point in or out
b2 is b value of second line
'''
def point_in_poly_faster(p1x, p1y, p2x, p2y, p4x, p3x, p3y):
    is_in = True
    #print('\t\t point_in_poly_faster:')
    # first line
    if abs(p2x - p1x) <= 1E-20 or abs(p2y - p1y) <= 1E-20:
        msg = '[ERROR] at line 75 in python script \n'
        stderr_fileno.write(msg)
        sys.exit(-1)
    else:

        a1 = (p2y - p1y) / (p2x - p1x)


    b1 = (p1y +(-p1x * a1)) * -1
    b2 = p3y

    x = (b1 + b2) / (a1)
    y = b2

    scale_x = (p2x - x) / (p2x - p1x)
    scale_y =  (p2y - y) /  (p2y - p1y)
    scale_xx = (p4x - x) / (p4x - p3x)

    if scale_x < 0 or scale_x > 1:
        is_in = False

    if scale_y < 0 or scale_y > 1:
        is_in = False

    if scale_xx < 0 or scale_xx > 1:
        is_in = False


    #print('\t point: ', x, ' ', y)
    #print('\t scale: ', scale_x, ' ', scale_y)

    return is_in


'''
Check if the mesh centroid is in or out from another geometry
In this case, geometry is always polygon or multipolygon
'''
def checkIntersect(geom, mesh, x_min,):
    g_x, g_y = geom.exterior.coords.xy
    mesh['contido'] = False
    #coords = np.dstack((x,y)).tolist() #Getting coordiantes from polygons

    for j in range(0, len(mesh)):
        x, y = mesh.iloc[j].geometry.centroid.xy
        x_mesh = x[0]
        y_mesh = y[0]

        count = 0
        for i in range(0, len(g_x)-1):
            x_p1 = g_x[i]
            y_p1 = g_y[i]
            x_p2 = g_x[i+1]
            y_p2 = g_y[i+1]

            if abs(x_p1 - x_p2) > 1E-20 and abs(y_p1 - y_p2) > 1E-20:
                x_p3 = x_mesh
                y_p3 = y_mesh

                ret = point_in_poly_faster(x_p1, y_p1, x_p2, y_p2, x_min, x_p3, y_p3)
                if ret == True:
                    count = count + 1

        if (count > 0) and ((count % 2) != 0):
            mesh.loc[mesh.id == j, 'contido'] = True

    return mesh


def print_GPD(geodf):
    for i in range(0, len(geodf)):
        r = geodf.loc[i]
        txt = '{};{}'.format(r['CD_MUN'], r['NM_MUN'])
        print(txt)

#-------------------------------------------------------------------------------
def build_quad_mesh(minx, miny, maxx, maxy, discretization, gdf):
    crtin = gdf.crs
    msg = '{} {} {} {} {}'.format(minx, miny, maxx, maxy, discretization)
    print(msg)
    # transformer = Transformer.from_crs(5880, crtin, always_xy=True)
    print(crtin)
    transformer = Transformer.from_crs(3857, crtin, always_xy=True)
    dx, dy = transformer.transform(discretization/ 2, discretization /2 )
    distx = maxx - minx
    disty = maxy - miny
    w = int(math.ceil(distx / dx))
    h = int(math.ceil(disty / dy))
    print('Malha {},{}'.format(w, h))
#---------------------------------------------------------------------------------
    x = minx
    y = miny
    ID = 0
    ID_v     = []
    COORD_v  = []
    INDEX_v  = []
    X_MAX    = []
    X_MIN    = []
    Y_MAX    = []
    Y_MIN    = []

    #we must to close polygon, it means, the last point must be equal to the first one
    while y <= maxy:
        x = minx#
        while x <= maxx:
            s_poly = 'POLYGON (({0:.20f} {1:.20f}, {2:.20f} {1:.20f}, {2:.20f} {3:.20f}, {0:.20f} {3:.20f}, {0:.20f} {1:.20f}))'.format(x, y, x + dx, y + dy)
            ID_v.append(ID)
            COORD_v.append(s_poly)
            INDEX_v.append('unknow!')
            X_MAX.append( x + dx)
            X_MIN.append( x - dx)
            Y_MAX.append( y + dy)
            Y_MIN.append( y - dy)
            x = x + dx
            ID = ID + 1
            if (ID % 100) == 0:
                print('.', end = '')
        y = y + dy

    print('Creating dataframe')
    df=pd.DataFrame({'id':ID_v, 'geometry':COORD_v, 'district':INDEX_v, 'x_max':X_MAX, 'x_min': X_MIN, 'y_max':Y_MAX, 'y_min': Y_MIN })

    print('Creating geoseries')
    df['geometry'] = gpd.GeoSeries.from_wkt(df['geometry'])

    geo_mesh = gpd.GeoDataFrame(df, geometry='geometry')
    g = [i for i in geoni.geometry]
    geo_mesh = checkIntersect(g[0], geo_mesh, minx-(2*dx))

    return geo_mesh

'''
Add a new attribute layer in mesh geopandas dataframa - it is another column
This procedure is based on distance in global coordiante domain
'''
def addPointAttribute(mesh, attib_field, attribute_gdf):
    aux_attib_field = attib_field
    size = len(mesh)
    #s_domain = math.floor(len(school_jg) / threads)
    #https://github.com/classner/pymp/blob/master/README.md
    #with pymp.Parallel(threads) as p:
    #    for i in p.range(0, len(school_jg)):
    #        if p.thread_num == 0:
    #            print(i, '/', s_domain)
    for i in range(0, len(attribute_gdf)):
        print(i, '/', len(attribute_gdf))
        a_x, a_y = attribute_gdf.iloc[i].geometry.centroid.xy
        x_p1 = a_x[0]
        y_p1 = a_y[0]

        for k in range(0, size): #for each cell, I will check if there is or not a bus stop

            lMesh =  mesh.iloc[k]

            x_g_max = lMesh.x_max
            x_g_min = lMesh.x_min
            y_g_max = lMesh.y_max
            y_g_min = lMesh.y_min

            in_side = True
            if x_p1 < x_g_min:
                in_side = False

            if x_p1 > x_g_max:
                in_side = False

            if y_p1 < y_g_min:
                in_side = False

            if y_p1 > y_g_max:
                in_side = False

            if in_side == True:
                value = lMesh[aux_attib_field]
                value = value + 1
                mesh.loc[mesh.id == lMesh.id, aux_attib_field] = value
                #mesh.__setitem__((mesh.id == lMesh.id, aux_attib_field), value)
    return mesh


if __name__ == '__main__':
    print('Exemplo de uso do Geopandas - mapa do Baixada Fluminense')
    shp_file_name_city = 'dados-IBGE/RJ_Municipios_2020.shp'
    shp_file_name_schools = 'inloco/educ_escolasPoint.shp'
    shp_file_streets = 'dados-IBGE/3303500_faces_de_logradouros_2019.shp'
    geodf = gpd.read_file(shp_file_name_city, encodig='UTF-8')
    geo_schools = gpd.read_file(shp_file_name_schools, encodig='ISO-8859-1')
    #https://gis.stackexchange.com/questions/324621/geopandas-linestrings-must-have-at-least-2-coordinate-tuples-when-reading-gpx
    #geost = gpd.read_file(shp_file_streets, encodig='utf-8')

    #print_GPD(geodf)
    #sys.exit()
    #print(geo_schools.columns)
    geo_schools_ni = geo_schools.loc[geo_schools['Município'] == 'NOVA IGUAÇU']
    geoni = geodf.loc[geodf['CD_MUN'] == '3303500']
    poly_geom = geoni.bounds


    #pegando minímos e máximos
    minx = float(poly_geom.minx)
    miny = float(poly_geom.miny)
    maxx = float(poly_geom.maxx)
    maxy = float(poly_geom.maxy)

    print('Construindo malha')
    geo_mesh = build_quad_mesh(minx, miny, maxx, maxy, 1000, geoni)
    geo_in = geo_mesh.loc[geo_mesh['contido'] == True]

    print('Add escolas')
    geo_in['escolas'] = 0
    geo_in = addPointAttribute(geo_in, 'escolas', geo_schools_ni)
    print('Salvando arquivo')
    geo_in.to_file('saida/dataframe.shp')

    fig, ax = plt.subplots(figsize=(10, 10))
    #geost.plot(ax=ax, color='blue', edgecolor='k')

    geoni.geometry.boundary.plot(ax=ax, color='black', edgecolor='k')
    geo_in.geometry.boundary.plot(ax=ax, color='#ccccff', edgecolor='k')
    geo_schools.plot(ax=ax, color='#ff0000', edgecolor='k')
    #geodf.geometry.boundary.plot(color=None, edgecolor='k', linewidth=2, ax=ax)

    crs = geoni.crs
    title = 'Mapa do Município do Estado do Rio de Janeiro'
    plt.title(title)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()
    #etapa 1 - escolha do Município: Nova Iguaçu
