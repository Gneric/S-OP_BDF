from src.api.hasura_queries.data_db_main import *
from datetime import datetime
import sys

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