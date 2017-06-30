# coding: utf-8
from requests import get
from simplejson import loads


def get_coordenates(endereco):
    if endereco:
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}'.format(endereco)
        headers = {'accept-language': 'pt-BR,pt;q=0.8,en-US;q=0.6,en;q=0.4'}
        response = get(url, headers=headers)
        if response.status_code == 200:
            try:
                data = loads(response.text)
                results = data['results'][0]
                endereco_formatado = results['formatted_address']
                lat = results['geometry']['location']['lat']
                lng = results['geometry']['location']['lng']
                return (lat, lng, endereco_formatado)
            except:
                return None


def get_min_max_coordenates(lat=0, lng=0, circle=1):
    """
    A abordagem aqui é achar um quadrado, onde seja possivel
    inscrever um circulo de n km de distancia do ponto central.
    Com base nas distâncias calculadas em http://www.longitudestore.com/how-big-is-one-gps-degree.html
    Eu calculo as latitudes e longitudes minimas e máximas para esse quadrado.
    """
    _delta_lat = 0.0089831 * circle
    _delta_lng = 0.009044 * circle
    return (lat - _delta_lat, lat + _delta_lat, lng - _delta_lng, lng + _delta_lng)
