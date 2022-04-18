from datetime import datetime, time
from ntpath import join
from os import scandir
import pandas as pd
import sys

from src.api.hasura_queries.audit import *
from src.api.hasura_queries.data_inputs import *
from src.api.services.data_handler import *
from src.api.services.global_variables import DATA_PATH, DB_TABLE_AREA

def getData(id, area_id):
    if area_id == 1:
        return requestDataBaseline(id)
    if area_id == 2:
        return requestDataLaunch(id)
    if area_id == 3:
        return requestDataPromo(id)
    if area_id == 4:
        return requestDataValorizacion(id) 
    if area_id == 5:
        return requestDataShoppers(id) 
    else:
        return ""

def checkDeleteTable(area_id, year, month, current_user):
    area_id = int(area_id)
    if int(month) < 10 and len(month) == 1:
        month = f"0{int(month)}"
    if area_id == 1:
        res = deleteDataBaseline(year+month)
        if res != "":
            audit_inputs({"file_id": int(time.time()), "date": datetime.now().strftime('%m/%d/%Y'), "accion": "DELETE", "clasificacion": "BASELINE", "user": current_user})
        return res
    if area_id == 2:
        res = deleteDataLaunch(year+month)
        if res != "":
            audit_inputs({"file_id": int(time.time()), "date": datetime.now().strftime('%m/%d/%Y'), "accion": "DELETE", "clasificacion": "LAUNCH", "user": current_user})
        return res
    if area_id == 3:
        res = deleteDataPromo(year+month)
        if res != "":
            audit_inputs({"file_id": int(time.time()), "date": datetime.now().strftime('%m/%d/%Y'), "accion": "DELETE", "clasificacion": "PROMO", "user": current_user})
        return res
    if area_id == 4:
        res = deleteDataValorizacion(year+month)
        if res != "":
            audit_inputs({"file_id": int(time.time()), "date": datetime.now().strftime('%m/%d/%Y'), "accion": "DELETE", "clasificacion": "VALORIZACION", "user": current_user})
        return res
    if area_id == 5:
        res = deleteDataShoppers(year+month)
        if res != "":
            audit_inputs({"file_id": int(time.time()), "date": datetime.now().strftime('%m/%d/%Y'), "accion": "DELETE", "clasificacion": "SHOPPER", "user": current_user})
        return res
    else:
        return ""

def cloneData(file_id, area_id, current_user):
    try:
        data = []
        if area_id == 1:
            data = requestDataBaseline(file_id)
            if data != "":
                audit_inputs({"file_id": int(time.time()), "date": datetime.now().strftime('%m/%d/%Y'), "accion": f"CLONE {file_id}", "clasificacion": "BASELINE", "user": current_user})
        if area_id == 2:
            data = requestDataLaunch(file_id)
            if data != "":
                audit_inputs({"file_id": int(time.time()), "date": datetime.now().strftime('%m/%d/%Y'), "accion": f"CLONE {file_id}", "clasificacion": "LAUNCH", "user": current_user})
        if area_id == 3:
            data = requestDataPromo(file_id)
            if data != "":
                audit_inputs({"file_id": int(time.time()), "date": datetime.now().strftime('%m/%d/%Y'), "accion": f"CLONE {file_id}", "clasificacion": "PROMO", "user": current_user})
        if area_id == 4:
            data = requestDataValorizacion(file_id)
            if data != "":
                audit_inputs({"file_id": int(time.time()), "date": datetime.now().strftime('%m/%d/%Y'), "accion": f"CLONE {file_id}", "clasificacion": "VALORIZACION", "user": current_user})
        if area_id == 5:
            data = requestDataShoppers(file_id)
            if data != "":
                audit_inputs({"file_id": int(time.time()), "date": datetime.now().strftime('%m/%d/%Y'), "accion": f"CLONE {file_id}", "clasificacion": "SHOPPER", "user": current_user})
        if data == []:
            return "area_id not found"
        formatted_data = data['rows']
        xslx_name = f"{DB_TABLE_AREA[str(area_id)]}"
        xlsx_name_w_ext = f'{xslx_name}.xlsx'
        xslx_path = join(DATA_PATH, xslx_name)
        excel_path = createExcelFile(file_id, area_id, formatted_data, xslx_name, xslx_path)
        if excel_path == "":
            return ""
        return xlsx_name_w_ext
    except:
        return sys.exc_info()[1]

def getTemplates(year, month, area_id):
    try:
        if year == "":
            year = str(datetime.today().strftime('%Y'))
        if month == "":
            month = str(datetime.today().strftime('%m'))
        if DB_TABLE_AREA[str(area_id)] == 'valorizacion':
            return createTemplateValorizacion(f"{DB_TABLE_AREA[str(area_id)]}", year, month)
        if DB_TABLE_AREA[str(area_id)] != 'valorizacion':
            return createTemplate(f"{DB_TABLE_AREA[str(area_id)]}", year, month)
    except:
        print(sys.exc_info()[1])
        return ""

def checkExcelFiles(area_id, year, month, current_user, filename):
    for f in scandir(DATA_PATH):
        xl = pd.ExcelFile(f)
        clasificacion = DB_TABLE_AREA[str(area_id)]
        for sheet in xl.sheet_names:
            if sheet == 'Hoja1' or sheet == DB_TABLE_AREA[str(area_id)]:
                df = pd.read_excel(f, sheet)
                res = {}
                file_id = int(time.time())
                if area_id == 1:
                    res = Loadbaseline(df, year, month, file_id)
                elif area_id == 2:
                    res = LoadLaunch(df, year, month, file_id)
                elif area_id == 3:
                    res = LoadPromo(df, year, month, file_id)
                elif area_id == 4:
                    res = LoadValorizacion(df, year, month, file_id)
                elif area_id == 5:
                    res = LoadShoppers(df, year, month, file_id)
                elif area_id == 9:
                    res = LoadForecast(df, year, month, file_id) 
                else:
                    return { 'error': 'El Area ID enviado no se encuentra en el listado de IDs aprovados' }, 400
                print('CheckAfterLoad')
                err_check = res.get('error', False)
                err_details = res.get('details',[])
                warning_check = res.get('warning', False)
                msg = res.get('message', '')
                if err_check:
                    if err_details:
                        return { 'error': msg, 'details': err_details }, 400
                    else:
                        return { 'error': msg }, 400
                elif warning_check:
                    audit = audit_inputs({"file_id": file_id, "date": datetime.now().strftime('%m/%d/%Y'), "accion": "INSERT", "clasificacion": clasificacion, "user": current_user})
                    reg_file = register_file({'file_id': file_id, "date": datetime.now().strftime('%m/%d/%Y'), "name": filename, "user": current_user })
                    file_data = request_file_data(area_id, msg['file_id'])
                    return { 'result': 'ok', 'warning': err_details, 'file_id': msg['file_id'], 'file_data': file_data}
                else:
                    audit = audit_inputs({"file_id": file_id, "date": datetime.now().strftime('%m/%d/%Y'), "accion": "INSERT", "clasificacion": clasificacion, "user": current_user})
                    reg_file = register_file({'file_id': file_id, "date": datetime.now().strftime('%m/%d/%Y'), "name": filename, "user": current_user })
                    file_data = request_file_data(area_id, msg['file_id'])
                    return { 'result' : 'ok', 'warning': [], 'file_id': msg['file_id'], 'file_data': file_data}
            else:
                return { 'error': f"No se encontro la hoja con el nombre correcto 'Hoja 1' / {DB_TABLE_AREA[area_id]}" }, 400

def checkInfoMonth(year, month):
    if int(month) < 10 and len(month) == 1:
        month = f"0{int(month)}"
    info = requestIDbyPeriod(f"{year}{month}")
    return { 'result' : info }

def delete_file_data(area_id, file_id):
    try:
        if area_id:
            return delete_data_by_file_id(int(area_id), file_id)
        else:
            return { 'error': 'error obteniendo tabla del area enviada' }, 400
    except:
        return { 'error': 'error haciendo la peticion de eliminacion de data' }, 400

def update_changes_bd(data_old):
    try:
        data = list({ each['nart'] : each for each in data_old }.values())
        result = {}
        upd_table = []
        upd_table.append({ 'name': 'BASELINE', 'rows': [{'id':x['id'],'clasificacion':x['clasificacion'],'nart':x['nart'],'year':x['year'],'month':x['month'],'cantidad':x['units']} for x in data if x['clasificacion']=='BASELINE']})
        upd_table.append({ 'name': 'LAUNCH', 'rows': [{'id':x['id'],'clasificacion':x['clasificacion'],'nart':x['nart'],'year':x['year'],'month':x['month'],'cantidad':x['units']} for x in data if x['clasificacion']=='LAUNCH']})
        upd_table.append({ 'name': 'PROMO', 'rows': [{'id':x['id'],'clasificacion':x['clasificacion'],'nart':x['nart'],'year':x['year'],'month':x['month'],'cantidad':x['units'] } for x in data if x['clasificacion']=='PROMO']})
        upd_table.append({ 'name': 'VALORIZACION', 'rows': [{'id':x['id'],'clasificacion':x['clasificacion'],'nart':x['nart'],'year':x['year'],'month':x['month'],'cantidad':x['units'] } for x in data if x['clasificacion']=='VALORIZACION']})
        upd_table.append({ 'name': 'SHOPPER', 'rows': [{'id':x['id'],'clasificacion':x['clasificacion'],'nart':x['nart'],'year':x['year'],'month':x['month'],'cantidad':x['units'] } for x in data if x['clasificacion']=='SHOPPER']})
        for table in upd_table:
            if len(table['rows']) > 0:
                result[table['name']] = updateInputTable(table['name'], table['rows'])
        return result
    except:
        print(sys.exc_info())
        return { 'error': 'error actualizando data' }, 400

def add_new_row(data):
    try:
        table_name = data['clasificacion']
        id = f'{datetime.now().strftime("%Y%m")}'
        if table_name == 'BASELINE':
            return addRow({'id':id,'clasificacion':table_name,'nart':data['nart'],'descripcion':data['descripcion'],'year':data['year'],'month':data['month'],'cantidad':data['cantidad']})
        elif table_name == 'LAUNCH':
            return addRow({'id':id,'clasificacion':table_name, 'canal': data['canal'], 'nart':data['nart'],'descripcion':data['descripcion'],'year':data['year'],'month':data['month'],'cantidad':data['cantidad']})
        elif table_name == 'PROMO':
            return addRow({'id':id, 'clasificacion':table_name, 'tipo_promo':data['tipo_promo'], 'canal': data['canal'], 'application_form': data['application_form'], 'nart':data['nart'], 'descripcion':data['descripcion'], 'year':data['year'], 'month':data['month'], 'cantidad':data['cantidad']})
        elif table_name == 'VALORIZACION':
            return addRow({'id':id,'clasificacion':table_name,'nart':data['nart'],'descripcion':data['descripcion'],'year':data['year'],'month':data['month'],'value':data['value'],'cantidad':data['cantidad']})
        elif table_name == 'SHOPPER':
            return addRow({'id':id,'clasificacion':table_name, 'tipo_promo':data['tipo_promo'], 'canal': data['canal'], 'nart':data['nart'],'descripcion':data['descripcion'],'year':data['year'],'month':data['month'], 'cantidad':data['cantidad']})
    except KeyError as err:
        print(f' Error add_new_row {err}')
        return 0
