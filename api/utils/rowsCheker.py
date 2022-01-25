import sys
import json
from api.utils.hasura_api import request_Maestro_productos

def dataCheck(data):
    json_data = json.loads(data)
    productos = request_Maestro_productos()
    err = []
    try:
        for row in json_data:
            index = json_data.index(row)
            if row.get('nart', 'N/A') == False:
                err.append({ 'columna': 'nart', 'error': 'Nart vacio' })
            nart = row.get('nart','')
            if nart not in productos:
                err.append({ 'columna': 'nart', 'error': f'nart {nart} no encontrado en Maestro de productos' })
    except:
        print(sys.exc_info())
    new_err = [ dict(t) for t in {tuple(d.items()) for d in err} ]
    return new_err