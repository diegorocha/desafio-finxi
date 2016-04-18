from requests import get
from simplejson import loads

def get_coordenates(endereco):
    if endereco:
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}'.format(endereco)
        response = get(url)
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

