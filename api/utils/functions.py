from api.utils.hasura_api import *
from api.utils.dataLoader import LoadForecast, LoadLaunch, LoadProducts, LoadPromo, LoadShoppers, LoadValorizacion, Loadbaseline, createCloneMaestro, createDBMainFile, createExcelFile, createTemplate, createTemplateValorizacion
from os import getcwd, scandir, unlink, listdir
from pathlib import Path
from os.path import join
import pandas as pd
import bcrypt
from datetime import datetime
import time

from api.utils.rowsCheker import checkExistingCategories, dataMaestroCheck

data_path = join(getcwd(),'api','data')
template_path = join(getcwd(),'api','templates')
def cleanDataFolder():
    for file in Path(data_path).glob('*.xlsx'):
        unlink(file)

ALLOWED_EXT = set(['xlsx','xls'])
def allowed_extensions(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

ALLOWED_NAMES = set(['BASELINE','LAUNCH','PROMO','VALORIZACION','PRODUCTOS'])
def allowed_names(filename):
    return '.' in filename and filename.rsplit(' - ', 1)[0] in ALLOWED_NAMES

def checkFiles():
    return len(listdir(data_path))


db_table_area = {"1":"baseline" ,"2":"launch", "3":"promo", "4":"valorizacion", "5":"shopper"}

def checkExcelFiles(area_id, year, month, current_user, filename):
    for f in scandir(data_path):
        xl = pd.ExcelFile(f)
        clasificacion = db_table_area[str(area_id)]
        for sheet in xl.sheet_names:
            if sheet == 'Hoja1' or sheet == db_table_area[str(area_id)]:
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
                return { 'error': f"No se encontro la hoja con el nombre correcto 'Hoja 1' / {db_table_area[area_id]}" }, 400

def checkExcelProduct():
    try:
        for file in scandir(data_path):
            xl = pd.ExcelFile(file)
            for sheet in xl.sheet_names:
                df = pd.read_excel(file, sheet)
                res = LoadProducts(df)
                return res
    except:
        print('error checkExcelProduct :', sys.exc_info())
        return { 'error': 'error en la lectura de archivo' }, 400

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

def checkInfoMonth(year, month):
    if int(month) < 10 and len(month) == 1:
        month = f"0{int(month)}"
    info = requestIDbyPeriod(f"{year}{month}")
    return { 'result' : info }


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
        xslx_name = f"{db_table_area[str(area_id)]}"
        xlsx_name_w_ext = f'{xslx_name}.xlsx'
        xslx_path = join(data_path, xslx_name)
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
        if db_table_area[str(area_id)] == 'valorizacion':
            return createTemplateValorizacion(f"{db_table_area[str(area_id)]}", year, month)
        if db_table_area[str(area_id)] != 'valorizacion':
            return createTemplate(f"{db_table_area[str(area_id)]}", year, month)
    except:
        print(sys.exc_info()[1])
        return ""

def logUser(email, password):
    user_info = checkPassword(email)
    if user_info == None:
        return None
    else:
        if bcrypt.checkpw(password.encode('utf-8'), user_info.get('hash_password').encode('utf-8')):
            return checkUser(email)
        else:
            return None

def createUser(new_user):
    try:
        hash_pwd = bcrypt.hashpw(new_user['password'].encode('utf-8'), bcrypt.gensalt())
        decoded_pwd = hash_pwd.decode('utf-8')
        user = {
            "mail": new_user['mail'],
            "hash_password": decoded_pwd,
            "userName": new_user['username'],
            "phone": new_user['phone'],
            "isEnabled": new_user['isEnabled'],
            "name": new_user['name'],
            "role": new_user['role']
        }
        check_mail = checkMailExists(user['mail'])
        if check_mail != "":
            return { 'error' : 'el correo ingresado ya se encuentra registrado' }, 400
        res = insertUser(user)
        if res != "":
            return { 'result': "ok" }, 200
        else:
            return { 'error': 'error ingresando usuario' }, 400
    except:
        print(sys.exc_info()[1])
        return { 'error' : 'Failed to registerUser' }, 400

def userInfo(data = {}, id = ""):
    try:
        if data != {}:
            res = listUsers(data)
            return { 'result' : res }
        if id != "":
            res = listUserbyID(id)
            return { 'result' : res }
        else:
            return { 'error': 'no se encontro data para la busqueda' }, 400
    except:
        print(sys.exc_info()[1])
        return { "error" : "Error al retornar informacion de ususarios" }
 
def modUser(user, permissions):
    try:
        pwd = checkPassword(user['mail'])
        user['hash_password'] = pwd["hash_password"]
        permission2 = [{'userID': user['userID'], 'permissionID': p['permissionID'], 'isEnabled': p['isEnabled']} for p in permissions ]
        res = modifyUser(user, permission2)
        if res == "":
            return { "error": "error al modificar el usuario" }, 400
        else:
            return { "result" : "ok" }
    except:
        print(sys.exc_info()[1])
        return { "error" : "Error al retornar respuesta del servidor" }, 400

def pwdChange(user_id, pwd, new_pwd):
    try:
        user_info = checkPasswordByID(user_id)
        if user_info == "":
            return { 'error' : 'No existe usuario' }
        if bcrypt.checkpw(pwd.encode('utf-8'), user_info.get('hash_password').encode('utf-8')):
            hashed_pwd = bcrypt.hashpw(new_pwd.encode('utf-8'), bcrypt.gensalt())
            decoded_pwd = hashed_pwd.decode("utf-8")
            res = changepw(user_id, hashed_pwd.decode('utf-8'))
            if res != "":
                return { "result" : "ok" }, 200
            else:
                return { "error", "error al cambiar la contraseña" }, 400
        else:
            { "error" : "La contraseña ingresada con coincide con la contraseña actual" }, 400
    except:
        print(sys.exc_info()[1])
        return { "error" : "Error al cambiar la contraseña del usuario" }, 400

def getVisualBD():
    return db_last_id()

def get_db_historico():
    return requestVisualBD()

def getPrepareSummary(filters):
    return requestPrepareSummary(filters)

def getSimulationUnits():
    return demand_simulation_units()

def getSimmulationNetSales():
    return demand_simulation_netsales()

def getDemandSimulationDB():
    return demand_simulation_db()

def getFCSimulation():
    return fc_simulation()

def getGraphDataset():
    return graph_dataset()

def getActionTest(numbers):
    return request_action_test(numbers)

def getPermissionbyActions(action):
    try:
        permission_list = getPermissions(action)
        return  { 'result' : permission_list }, 200
    except:
        print(sys.exc_info()[1])
        return { "error" : "Error al retornar permisos" }, 400

def updatePermissions(permissions):
    try:
        rows_affected = updatePermissionByList(permissions)
        if rows_affected == "":
            return { "error" : "Error al actualizar permisos" }, 400
        else:
            return { 'result' : 'ok' }, 200
    except:
        print(sys.exc_info()[1])
        return { "error" : "Error al actualizar permisos" }, 400

def generate_token(user):
    is_admin = user['role'] == "Admin"
    user_roles = ["user"]
    admin_roles = ["user","admin"]
    payload =  str(user['id'])
    hasura_token = {
        "hasura_claims": {
            "x-hasura-allowed-roles" : admin_roles if is_admin else user_roles,
            "x-hasura-default-role": "admin" if is_admin else "user",
            "x-hasura-user-id": str(user['id'])
        }
    }
    return payload, hasura_token

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

def add_multiple_rows(data):
    try:
        rows = []
        table_name = data['clasificacion']
        id = request_id_db_main()
        bpu = data.get('bpu','')
        brand_category = data.get('brand_category','')
        application_form = data.get('application_form','')
        promo_spgr = data.get('promo_spgr','')
        units = data.get('units', 0)
        netsales = data.get('netsales', 0)
        ajuste_netsales = data.get('ajuste_netsales', 0)
        comentario = data.get('comentario','')
        canal = data.get('canal','')
        for year in data['year']:
            for month in data['month']:
                rows.append({
                    'id':id,
                    'clasificacion':table_name,
                    'bpu':bpu,
                    'brand_category':brand_category,
                    'application_form':application_form,
                    'promo_spgr':promo_spgr,
                    'year':year,
                    'month':month,
                    'units': units,
                    'netsales': netsales,
                    'ajuste_netsales': ajuste_netsales,
                    'comentario': comentario,
                    'canal': canal
                })
        res = insert_multiple_rows(rows)
        if res == "":
            return { 'error': 'error insertando data' }, 400
        else:
            return { 'result' : 'ok' }
    except KeyError as err:
        print('error add_multiple_rows :', err)


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

def request_productos_otros():
    try:
        data = get_productos_otros()
        return data
    except:
        print(sys.exc_info())
        ""

def getinfo_db_main(data):
    try:
        return requestinfo_db_main(data['clasificacion'], data['year'], data['month'], data['bpu'], data['brand_category'], data['application_form'])
    except:
        print(sys.exc_info())
        return { 'error': 'error actualizando data' }, 400

def update_db_main(data_old):
    try:
        id = request_id_db_main()
        data = list( { str(each['id'])+str(each['clasificacion'])+str(each['bpu'])+str(each['brand_category'])+str(each['application_form'])+str(each['promo_spgr'])+str(each['year'])+str(each['month']) : each for each in data_old }.values() )
        for i in data:
            if i['id'] == 0: #Si es comodin
                if i['promo_spgr'] == "" or i['ajuste_netsales'] == 0:
                    data.remove(i)
                else:
                    i['id'] = id
        update = update_db_main_table(data)
        #audit = audit_db_main(data)
        return update
    except:
        print(sys.exc_info())
        return { 'error': 'error actualizando data' }, 400

def request_cargar_db_main(id):
    try:
        data = request_data_last_id(id)
        curr_month = f'{datetime.now().strftime("%Y%m")}'
        if id:
            if data == []:
                return { 'error': f'no se encontro data en el mes enviado - {id}' }, 400
        else:
            if data == [] or data[0]["id"] < curr_month :
                return { 'error': f'no se encontro data en el mes actual - {curr_month}' }, 400
        del_res = delete_db_main_id()
        res = insert_data_db_main(data)

        data_comparacion = request_data_comparacion_sop()
        del_res = delete_data_comparacion_sop()
        res_comp = request_upsert_comparacion_sop(data_comparacion)
        if id:
            return { 'ok': f'{res} filas ingresadas a la tabla de datos Maestra y {res_comp} filas ingresadas a la tabla de compraciones SOP - Custom ID: {id}'}, 200
        else:
            return { 'ok': f'{res} filas ingresadas a la tabla de datos Maestra y {res_comp} filas ingresadas a la tabla de compraciones SOP - Regular ID: {curr_month}'}, 200
    except:
        return { 'error': 'error cargando nuevos datos' }, 400

def request_db_main(id):
    try:
        data = request_alldata_db_main(id)
        if data == []:
            return ""
        else:
            return createDBMainFile(data,id)
    except:
        return ""

def request_cerrar_mes():
    try:
        data = request_data_db_main()
        if data != []:
            del_res = backup_db_main(data)
            data_comparacion = request_curr_comparacion_sop()
            del_res_sop = backup_comparacion_sop(data_comparacion)
            return { 'ok': f'{del_res} filas ingresadas a la tabla de SOP Backup y {del_res_sop} filas a cierre de comparaciones'}
        else:
           print(sys.exc_info())
           return { 'error': 'no se encontraron datos del mes en curso' }, 400
    except:
        print(sys.exc_info())
        return { 'error': 'error cargando nuevos datos' }, 400

def getInfoTimeline(permissionID, timelineID):
    try:
        res = requestinfo_timeline(permissionID, timelineID)
        if res:
            return res
        else:
            return { 'error': 'error en la busqueda de informacion' }, 400
    except:
        return { 'error': 'error en la busqueda de informacion' }, 400

def setInfoTimeline(data):
    try:
        res = request_setinfo_timeline(data)
        if res:
            return res
        else:
            return { 'error': 'error en el retorno de informacion' }, 400
    except:
        return { 'error': 'error en la busqueda de informacion' }, 400

def request_info_cobertura(data):
    try:
        res = request_cobertura(data)
        if res:
            return { 'result': res }
        else:
            return { 'error': 'error al retornar informacion' }, 400
    except:
        return { 'error': 'error haciendo la peticion de informacion' }, 400

def delete_file_data(area_id, file_id):
    try:
        if area_id:
            return delete_data_by_file_id(int(area_id), file_id)
        else:
            return { 'error': 'error obteniendo tabla del area enviada' }, 400
    except:
        return { 'error': 'error haciendo la peticion de eliminacion de data' }, 400

def request_update_product(data):
    try:
        unique = list( { each['Material'] : each for each in data }.values() )
        err_check, err_message, new_data = dataMaestroCheck(unique)
        if err_check:
            return { 'error': err_message }, 400
        else:
            res = upload_data_maestro(new_data)
            if res:
                return res
            else:
                return { 'error': 'error al retornar peticion de actualizacion' }, 400
    except:
        print(sys.exc_info())
        return { 'error': 'error haciendo la peticion de actualizacion' }, 400

def request_upload_product(data):
    try:
        for row in data:
            for key, value in data.items():
                data[key] = value.upper().strip()
        res = upload_data_maestro(data)
        if res:
            return res
        else:
            return { 'error': 'error al retornar peticion de actualizacion' }, 400
    except:
        return { 'error': 'error haciendo la peticion de actualizacion' }, 400

def cloneMaestro():
    try:
        data =  request_data_maestro()
        res = createCloneMaestro(data)
        return res
    except:
        return { 'error':'error obteniendo datos' }, 400

def get_category_items(data):
    try:
        res = request_categories(data)
        if res == "":
            return { 'error': 'error en la actualizacion de la base de datos' }, 400
        else:
            return { 'result' : 'ok' }
    except:
        return { 'error': 'error insertando/actualizando datos' }, 400

def getUpsertCategory(data):
    try:
        unique = list( { each['name']+each['category'] : each for each in data }.values() )
        check_res = checkExistingCategories(unique)
        if check_res:
            return { 'error': 'errores en la verificacion de datos', 'error_details': check_res }, 400
        res = request_upsert_maestro_categorias(unique)
        if res == "":
            return { 'error': 'error en la actualizacion de la base de datos' }, 400
        else:
            return { 'result' : 'ok' }
    except:
        return { 'error': 'error insertando/actualizando datos' }, 400

def delete_category_items(data):
    try:
        res = request_delete_category_items(data)
        if res == "":
            return { 'error': 'error en la actualizacion de la base de datos' }, 400
        else:
            return { 'result' : 'ok' }
    except:
        return { 'error': 'error insertando/actualizando datos' }, 400
    
def get_transito_nart(nart):
    try:
        res = request_transito_nart(nart)
        if res:
            return res
        else:
            return { 'error', 'error al obtener datos del nart ingresado' }, 400
    except:
        return { 'error', 'error al obtener datos del nart ingresado' }, 400

def upsert_comparacion_sop(data):
    try:
        unique = list( { str(each['id'])+str(each['brand_category'])+str(each['application_form'])+str(each['bpu']) : each for each in data }.values() )
        res = request_update_comparacion_sop(unique)
        if res:
            return res
        else:
            return { 'error': 'error en la respuesta de actualizacion' }, 400
    except:
        print(sys.exc_info())
        return { 'error': 'error haciendo la peticion de actualizacion' }, 400

def upsert_conversion_moneda(data):
    try:
        unique = list( { str(each['year'])+str(each['moneda'])+str(each['valor']) : each for each in data }.values() )
        filtered_unique = [ each for each in unique if len(str(each['year'])) == 4 and each['valor'] > 0 ]
        res = request_update_conversion_moneda(filtered_unique)
        if res:
            return { 'result': f'ok - {res} filas afectadas' }
        else:
            return { 'error': 'error en la respuesta de actualizacion' }, 400
    except:
        return { 'error': 'error en la respuesta de actualizacion' }, 400

def get_conversion_moneda():
    try:
        res = request_conversion_moneda()
        if res != '':
            return res
        return { 'error': 'error en la obtencion de datos' }, 400
    except:
        return { 'error': 'error en la obtencion de datos' }, 400