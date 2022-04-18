
from os import scandir
import pandas as pd

from src.api.hasura_queries.data_product_master import *
from src.api.services.data_handler import LoadProducts, createCloneMaestro
from src.api.services.data_revision import checkExistingCategories, dataMaestroCheck
from src.api.services.global_variables import DATA_PATH

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

def checkExcelProduct():
    try:
        for file in scandir(DATA_PATH):
            xl = pd.ExcelFile(file)
            for sheet in xl.sheet_names:
                df = pd.read_excel(file, sheet)
                res = LoadProducts(df)
                return res
    except:
        print('error checkExcelProduct :', sys.exc_info())
        return { 'error': 'error en la lectura de archivo' }, 400

def cloneMaestro():
    try:
        data =  request_data_maestro()
        res = createCloneMaestro(data)
        return res
    except:
        return { 'error':'error obteniendo datos' }, 400

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