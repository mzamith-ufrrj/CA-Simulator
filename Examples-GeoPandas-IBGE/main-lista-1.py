import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from pyproj import Transformer
import math
import sys

def print_GPD(geodf):
    for i in range(0, len(geodf)):
        r = geodf.loc[i]
        txt = '{};{}'.format(r['CD_MUN'], r['NM_MUN'])
        print(txt)

#-------------------------------------------------------------------------------

def build_quad_mesh(minx, miny, maxx, maxy, discretization, crtin):
    msg = '{} {} {} {} {}'.format(minx, miny, maxx, maxy, discretization)
    print(msg)
    # transformer = Transformer.from_crs(5880, crtin, always_xy=True)
    print(crtin)
    transformer = Transformer.from_crs(3857, crtin, always_xy=True)
    dx, dy = transformer.transform(discretization, discretization)
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
    return gpd.GeoDataFrame(df, geometry='geometry')


if __name__ == '__main__':
    print('Exemplo de uso do Geopandas - mapa do Baixada Fluminense')
    shp_file_name_city = 'dados-IBGE/RJ_Municipios_2020.shp'
    shp_file_streets = 'dados-IBGE/3303500_faces_de_logradouros_2019.shp'
    geodf = gpd.read_file(shp_file_name_city, encodig='utf-8')
    #https://gis.stackexchange.com/questions/324621/geopandas-linestrings-must-have-at-least-2-coordinate-tuples-when-reading-gpx
    #geost = gpd.read_file(shp_file_streets, encodig='utf-8')

    #print_GPD(geodf)
    #sys.exit()

    geoni = geodf.loc[geodf['CD_MUN'] == '3303500']
    poly_geom = geoni.bounds

    #pegando minímos e máximos
    minx = float(poly_geom.minx)
    miny = float(poly_geom.miny)
    maxx = float(poly_geom.maxx)
    maxy = float(poly_geom.maxy)

    geo_mesh = build_quad_mesh(minx, miny, maxx, maxy, 200, geoni.crs)

    #sys.exit()
    #exibindo o mapa em camadas
    fig, ax = plt.subplots(figsize=(10, 10))
    #geost.plot(ax=ax, color='blue', edgecolor='k')
    geo_mesh.geometry.boundary.plot(ax=ax, color='gray', edgecolor='k')
    geoni.plot(ax=ax, color='yellow', edgecolor='k')
    geodf.geometry.boundary.plot(color=None, edgecolor='k', linewidth=2, ax=ax)

    crs = geoni.crs
    title = 'Mapa do Município do Estado do Rio de Janeiro'
    plt.title(title)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()
    #etapa 1 - escolha do Município: Nova Iguaçu

