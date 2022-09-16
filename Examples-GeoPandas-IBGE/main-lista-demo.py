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
    #transformer = Transformer.from_crs(3857, crtin, always_xy=True)
    #dx, dy = transformer.transform(discretization, discretization)
    
    
#---------------------------------------------------------------------------------
    ID = 0
    ID_v     = []
    COORD_v  = []
    INDEX_v  = []

    #we must to close polygon, it means, the last point must be equal to the first one
    s_poly = 'POLYGON (({0:.20f} {1:.20f}, {2:.20f} {1:.20f}, {2:.20f} {3:.20f}, {0:.20f} {3:.20f}, {0:.20f} {1:.20f}))'.format(minx, miny, maxx, maxy)
    ID_v.append(ID)
    COORD_v.append(s_poly)
    INDEX_v.append('unknow!')
    ID = ID + 1
    if (ID % 100) == 0:
        print('.', end = '')

    print('Creating dataframe')
    df=pd.DataFrame({'id':ID_v, 'geometry':COORD_v, 'district':INDEX_v})

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
    
    geoni.geometry.boundary.plot(ax=ax, color='yellow', edgecolor='k')
    geo_mesh.geometry.boundary.plot(ax=ax, color='blue', edgecolor='k')
    #geodf.geometry.boundary.plot(color=None, edgecolor='k', linewidth=2, ax=ax)

    crs = geoni.crs
    title = 'Mapa do Município do Estado do Rio de Janeiro'
    plt.title(title)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()
    #etapa 1 - escolha do Município: Nova Iguaçu

