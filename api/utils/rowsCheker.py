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
                err.append({ 'fila': index, 'columna': 'nart', 'error': 'Nart vacio' })
            if row.get('cantidad', 0) == False:
                err.append({ 'fila': index, 'columna': 'cantidad', 'error': 'Cantidad vacia o 0' })
            nart = row.get('nart','') 
            if nart not in productos:
                err.append({ 'fila': index, 'columna': 'nart', 'error': 'nart no encontrado en Maestro de productos' })
    except:
        print(sys.exc_info())
    return err
