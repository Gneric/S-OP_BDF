import sys
import json

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
    clasificaciones = request_clasificaciones_Maestro_productos()

    maestro_bpu = [ x['name'] for x in clasificaciones if x['category'] == 'BPU' ]
    maestro_randCategory = [ x['name'] for x in clasificaciones if x['category'] == 'BRANDCATEGORY' ]
    maestro_applicationForm = [ x['name'] for x in clasificaciones if x['category'] == 'APPLICATIONFORM' ]
    maestro_tipo = [ x['name'] for x in clasificaciones if x['category'] == 'TIPO' ]

    maestro_bpu_upper = [ x['name'].upper() for x in clasificaciones if x['category'] == 'BPU' ]
    maestro_randCategory_upper = [ x['name'].upper() for x in clasificaciones if x['category'] == 'BRANDCATEGORY' ]
    maestro_applicationForm_upper = [ x['name'].upper() for x in clasificaciones if x['category'] == 'APPLICATIONFORM' ]
    maestro_tipo_upper = [ x['name'].upper() for x in clasificaciones if x['category'] == 'TIPO' ]

    material_err = []
    err_message = []
    err_check = False
    for row in data:
        row['Material'] = row['Material'].strip()
        row['SPGR'] = row['SPGR'].strip()
        row['TIPO'] = row['TIPO'].strip()
        row['Descripcion'] = row['Descripcion'].strip()
        row['BPU'] = row['BPU'].strip()
        row['BrandCategory'] = row['BrandCategory'].strip()
        row['ApplicationForm'] = row['ApplicationForm'].strip()

        material = row.get('Material','')
        bpu = row.get('BPU', '')
        brandCategory = row.get('BrandCategory','')
        applicationForm = row.get('ApplicationForm','')
        tipo = row.get('TIPO','')

        # Revision de datos
        if bpu.upper() not in maestro_bpu_upper:
            material_err.append(row.get('Material'))
            err_message.append(f'BPU - {bpu} de Material {material} erroneo')
        else:
            row['BPU'] = maestro_bpu[maestro_bpu_upper.index(row['BPU'].upper())]
        if brandCategory.upper() not in maestro_randCategory_upper:
            material_err.append(row.get('Material'))
            err_message.append(f'brandCategory - {brandCategory} de Material {material} erroneo')
        else:
            row['BrandCategory'] = maestro_randCategory[maestro_randCategory_upper.index(row['BrandCategory'].upper())]
        if applicationForm.upper() not in maestro_applicationForm_upper:
            material_err.append(row.get('Material'))
            err_message.append(f'applicationForm - {applicationForm} de Material {material} erroneo')
        else:
            row['ApplicationForm'] = maestro_applicationForm[maestro_applicationForm_upper.index(row['ApplicationForm'].upper())]
        if tipo.upper() not in maestro_tipo_upper:
            material_err.append(row.get('Material'))
            err_message.append(f'TIPO - {tipo} de Material {material} erroneo')
        else:
            row['TIPO'] = maestro_tipo[maestro_tipo_upper.index(row['TIPO'].upper())]
            
    new_err = list(dict.fromkeys(material_err))
    new_data = [ x for x in data if x['Material'] not in new_err ]
    if err_message:
        err_check = True
    return err_check, err_message, new_data

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
