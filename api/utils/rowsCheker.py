from logging import warning
import sys
import json

from pandas import concat
from api.utils.hasura_api import request_Maestro_productos, request_clasificaciones_Maestro_productos

def dataCheck(data):
    json_data = json.loads(data)
    productos = request_Maestro_productos()
    err_check = False
    warn_check = False
    warnings = []
    err = []
    rows_checked = []
    try:
        for row in json_data:
            if row.get('nart', '') == False:
                err_check = True
                err.append({ 'columna': 'nart', 'error': 'Nart vacio' })
            nart = row.get('nart','')
            if nart not in productos:
                warn_check = True
                warnings.append({ 'columna': 'nart', 'error': f'nart {nart} no encontrado en Maestro de productos' })
    except:
        print(sys.exc_info())
    new_err = [ dict(t) for t in {tuple(d.items()) for d in err} ]
    return { 'error_check': err_check, 'errors': new_err, 'warning_check': warn_check, 'warnings': warnings }

def dataMaestroCheck(data):
    json_data = json.loads(data)
    clasificaciones = request_clasificaciones_Maestro_productos()
    maestro_bpu = clasificaciones[0]
    maestro_randCategory = clasificaciones[1]
    maestro_applicationForm = clasificaciones[2]
    maestro_spgr = clasificaciones[3]
    material_err = []
    err_message = []
    try:
        for row in json_data:
            material = row.get('Material','')
            bpu = row.get('BPU', '')
            brandCategory = row.get('BrandCategory','')
            applicationForm = row.get('ApplicationForm','')
            spgr = row.get('SPGR','')
            if row.get('BPU', '') == False:
                material_err.append(row.get('Material'))
                err_message.append(f'BPU de {material} vacio')
            if row.get('BrandCategory', '') == False:
                material_err.append(row.get('Material'))
                err_message.append(f'BrandCategory de {material} vacio')
            if row.get('ApplicationForm', '') == False:
                material_err.append(row.get('Material'))
                err_message.append(f'ApplicationForm de {material} vacio')
            if row.get('SPGR', '') == False:
                material_err.append(row.get('Material'))
                err_message.append(f'SPGR de {material} vacio')
            if bpu not in maestro_bpu:
                material_err.append(row.get('Material'))
                err_message.append(f'BPU de {material} no existente')
    except:
        print(sys.exc_info())
        return []