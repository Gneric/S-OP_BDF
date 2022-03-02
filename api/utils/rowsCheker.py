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
    maestro_bpu = [ x['name'] for x in clasificaciones if x['category'] == 'BPU' ]
    maestro_randCategory = [ x['name'] for x in clasificaciones if x['category'] == 'BRANDCATEGORY' ]
    maestro_applicationForm = [ x['name'] for x in clasificaciones if x['category'] == 'APPLICATIONFORM' ]
    maestro_spgr = [ x['name'] for x in clasificaciones if x['category'] == 'TIPO' ]
    material_err = []
    err_message = []
    try:
        for row in json_data:
            material = row.get('Material','')
            bpu = row.get('BPU', '')
            brandCategory = row.get('BrandCategory','')
            applicationForm = row.get('ApplicationForm','')
            spgr = row.get('SPGR','')
            # Revision de datos
            if bpu not in maestro_bpu:
                material_err.append(row.get('Material'))
                err_message.append(f'BPU {bpu} de {material} no existente')
            if brandCategory not in maestro_randCategory:
                material_err.append(row.get('Material'))
                err_message.append(f'brandCategory {brandCategory} de {material} no existente')
            if applicationForm not in maestro_applicationForm:
                material_err.append(row.get('Material'))
                err_message.append(f'applicationForm {applicationForm} de {material} no existente')
            if spgr not in maestro_spgr:
                material_err.append(row.get('Material'))
                err_message.append(f'SPGR {spgr} de {material} no existente')
            new_err = [ dict(t) for t in {tuple(d.items()) for d in material_err} ]
            new_data = [ x for x in data if x['Material'] not in new_err ]
            print('Pre Check :', len(data))
            print('Post Check :', len(new_data))
            return data
    except:
        print(sys.exc_info())
        return []

def rowMaestroCheck(row):
    clasificaciones = request_clasificaciones_Maestro_productos()
    maestro_bpu = [ x['name'] for x in clasificaciones if x['category'] == 'BPU' ]
    maestro_randCategory = [ x['name'] for x in clasificaciones if x['category'] == 'BRANDCATEGORY' ]
    maestro_applicationForm = [ x['name'] for x in clasificaciones if x['category'] == 'APPLICATIONFORM' ]
    maestro_spgr = [ x['name'] for x in clasificaciones if x['category'] == 'TIPO' ]
    err_message = []
    try:
        material = row.get('Material','')
        bpu = row.get('BPU', '')
        brandCategory = row.get('BrandCategory','')
        applicationForm = row.get('ApplicationForm','')
        spgr = row.get('SPGR','')
        # Revision de datos
        if bpu not in maestro_bpu:
            err_message.append(f'BPU {bpu} de {material} no existente')
            return False, err_message
        if brandCategory not in maestro_randCategory:
            err_message.append(f'brandCategory {brandCategory} de {material} no existente')
            return False, err_message
        if applicationForm not in maestro_applicationForm:
            err_message.append(f'applicationForm {applicationForm} de {material} no existente')
            return False, err_message
        if spgr not in maestro_spgr:
            err_message.append(f'SPGR {spgr} de {material} no existente')
            return False, err_message
        else:
            return True, []
    except:
        print(sys.exc_info())
        return False, err_message