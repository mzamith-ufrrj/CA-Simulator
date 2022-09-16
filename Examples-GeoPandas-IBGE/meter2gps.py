from pyproj import Transformer
if __name__ == '__main__':
    discretization = 50.0
    transformer = Transformer.from_crs(3857, 4674, always_xy=True)
    dx, dy = transformer.transform(discretization, discretization)
    print('Coordenadas do globo: ({} , {})'.format(dx, dy))