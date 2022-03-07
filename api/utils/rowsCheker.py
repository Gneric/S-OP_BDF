from logging import warning
import sys
import json

from pandas import concat
from api.utils.hasura_api import request_Maestro_productos, request_clasificaciones_Maestro_productos, request_used_categories

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
    maestro_bpu = [ x['name'].upper() for x in clasificaciones if x['category'] == 'BPU' ]
    maestro_randCategory = [ x['name'].upper() for x in clasificaciones if x['category'] == 'BRANDCATEGORY' ]
    maestro_applicationForm = [ x['name'].upper() for x in clasificaciones if x['category'] == 'APPLICATIONFORM' ]
    maestro_tipo = [ x['name'].upper() for x in clasificaciones if x['category'] == 'TIPO' ]
    material_err = []
    err_message = []
    try:
        for row in json_data:
            material = row.get('Material','')
            bpu = row.get('BPU', '')
            brandCategory = row.get('BrandCategory','')
            applicationForm = row.get('ApplicationForm','')
            tipo = row.get('TIPO','')
            # Revision de datos
            if bpu.upper() not in maestro_bpu:
                material_err.append(row.get('Material'))
                err_message.append(f'BPU - {bpu} de Material {material} erroneo')
            if brandCategory.upper() not in maestro_randCategory:
                material_err.append(row.get('Material'))
                err_message.append(f'brandCategory - {brandCategory} de Material {material} erroneo')
            if applicationForm.upper() not in maestro_applicationForm:
                material_err.append(row.get('Material'))
                err_message.append(f'applicationForm - {applicationForm} de Material {material} erroneo')
            if tipo.upper() not in maestro_tipo:
                material_err.append(row.get('Material'))
                err_message.append(f'TIPO - {tipo} de Material {material} erroneo')
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
    maestro_bpu = [ x['name'].upper() for x in clasificaciones if x['category'] == 'BPU' ]
    maestro_randCategory = [ x['name'].upper() for x in clasificaciones if x['category'] == 'BRANDCATEGORY' ]
    maestro_applicationForm = [ x['name'].upper() for x in clasificaciones if x['category'] == 'APPLICATIONFORM' ]
    maestro_tipo = [ x['name'].upper() for x in clasificaciones if x['category'] == 'TIPO' ]
    err_message = []
    try:
        material = row.get('Material','')
        bpu = row.get('BPU', '')
        brandCategory = row.get('BrandCategory','')
        applicationForm = row.get('ApplicationForm','')
        tipo = row.get('TIPO','')
        # Revision de datos
        if bpu.upper() not in maestro_bpu:
            err_message.append(f'BPU - {bpu} de Material {material} erroneo')
            return False, err_message
        if brandCategory.upper() not in maestro_randCategory:
            err_message.append(f'brandCategory - {brandCategory} de Material {material} erroneo')
            return False, err_message
        if applicationForm.upper() not in maestro_applicationForm:
            err_message.append(f'applicationForm - {applicationForm} de Material {material} erroneo')
            return False, err_message
        if tipo.upper() not in maestro_tipo:
            err_message.append(f'TIPO - {tipo} de Material {material} erroneo')
            return False, err_message
        else:
            return True, []
    except:
        print(sys.exc_info())
        return False, err_message

def checkExistingCategories(data):
    categories = request_used_categories()
    err_message = []
    for row in data:
        try:
            id = row.get('id','')
            name = row.get('name','')
            category = row.get('category','')
            key = name.upper()+category.upper()
            if id:
                continue
            if name == False or key in categories:
                err_message.append(f'el nombre {name} se encuentra en uso o se encuentra vacio')
        except:
            err_message.append(f'error en la fila {name}')
    return err_message
