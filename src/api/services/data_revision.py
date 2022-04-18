from src.api.hasura_queries.data_revision import request_Maestro_productos, request_clasificaciones_Maestro_productos, request_used_categories
import sys, json

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
    err_check = False
    for row in data:
        err_message = []
        row['Material'] = row['Material'].strip()
        row['SPGR'] = row['SPGR'].strip()
        row['TIPO'] = row['TIPO'].strip()
        row['Descripcion'] = row['Descripcion'].strip()
        row['BPU'] = row['BPU'].strip()
        row['BrandCategory'] = row['BrandCategory'].strip()
        row['ApplicationForm'] = row['ApplicationForm'].strip()
        row['SPGR_historico'] = row['SPGR_historico'].strip()

        material = row.get('Material','')
        bpu = row.get('BPU', '')
        brandCategory = row.get('BrandCategory','')
        applicationForm = row.get('ApplicationForm','')
        tipo = row.get('TIPO','')

        err_row = False
        if bpu.upper() not in maestro_bpu_upper:
            err_row = True
            err_message.append(f'La descripción {bpu} de BPU no concuerda con las categorías definidas')    
        else:
            row['BPU'] = maestro_bpu[maestro_bpu_upper.index(row['BPU'].upper())]
        if brandCategory.upper() not in maestro_randCategory_upper:
            err_row = True
            err_message.append(f'La descripción {brandCategory} de BrandCategory no concuerda con las categorías definidas')
        else:
            row['BrandCategory'] = maestro_randCategory[maestro_randCategory_upper.index(row['BrandCategory'].upper())]
        if applicationForm.upper() not in maestro_applicationForm_upper:
            err_row = True
            err_message.append(f'La descripción {applicationForm} de ApplicationForm no concuerda con las categorías definidas')
        else:
            row['ApplicationForm'] = maestro_applicationForm[maestro_applicationForm_upper.index(row['ApplicationForm'].upper())]
        if tipo.upper() not in maestro_tipo_upper:
            err_row = True
            err_message.append(f'La descripción {tipo} de TIPO no concuerda con las categorías definidas')
        else:
            row['TIPO'] = maestro_tipo[maestro_tipo_upper.index(row['TIPO'].upper())]
        
        if err_row:
            material_err.append({ 'material': material, 'errores': err_message })
            
    new_data = list( { each['Material'] : each for each in data }.values() )
    if material_err:
        err_check = True
    return err_check, material_err, new_data

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

def getSizebyColumnName(size_list, name):
    try:
        values_list = [ x['size'] if x['name']==name else 'NULL' for x in size_list]
        value = list(filter(lambda a: a != 'NULL', values_list))[0]
        return value
    except:
        return 0