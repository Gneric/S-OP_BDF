import sys
import json
from openpyxl import Workbook
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
from os.path import join
import xlsxwriter

from api.utils.hasura_api import sendDataBaseline, sendDataForecast, sendDataLaunch, sendDataPromo, sendDataShoppers, sendDataValorizacion
from api.utils.rowsCheker import dataCheck

def Loadbaseline(df, year, month):
    try:
        print('LoadBaseline')
        df = df.melt(id_vars = ["CLASIFICACION", "NART", "DESCRIPCION"], var_name = "FECHA", value_name = "QUANTITY")
        df = df.drop(labels=[0], axis=0)
        df['YEAR'] = df['FECHA'].dt.year
        df['MONTH'] = df['FECHA'].dt.month 
        df["KEY"] = str(year)+str(month)
        d1 = df[["KEY","CLASIFICACION", "NART", "DESCRIPCION","YEAR","MONTH","QUANTITY"]]
        d1 = d1[d1['CLASIFICACION'].notna()]
        d1 = d1[d1['NART'].notna()]
        d1 = d1[d1['DESCRIPCION'].notna()]
        d1 = d1[d1['QUANTITY'].notna()]
        d1.columns = ["id","clasificacion","nart","descripcion","year","month","cantidad"]
        result = d1.to_json(orient="records")
        check_result = dataCheck(result)
        if check_result['error_check']:
            return { 'error': check_result['error_check'], 'warning': False, 'message': 'Error en los datos enviados', 'details': check_result['errors'] }
        parsed = json.loads(result)
        res = sendDataBaseline(parsed)
        if check_result['warn_check']:
            return { 'error': False, 'warning': True, 'message': 'Datos ingresados con errores', 'details': check_result['warnings'] }
        return { 'error': False, 'message': res}
    except KeyError as err:
        error = str(err.__str__()).split(sep=": ")
        column_error = error[1].replace("[","").replace("]","").replace("\"","")
        return { 'error': True, 'message' : f"No se encontraron las columna(s): {column_error} en el archivo 'BASELINE'"}  
    except:
        print('Error load :', sys.exc_info())
        return { 'error': True, 'message' : "Error en el archivo, por favor revisar el modelo de carga" }
    
def LoadLaunch(df, year, month):
    try:
        df = df.melt(id_vars = ["CLASIFICACION", "CANAL", "NART", "DESCRIPCION"], var_name = "FECHA", value_name = "QUANTITY")
        df = df.drop(labels=[0], axis=0)
        df['YEAR'] = df['FECHA'].dt.year
        df['MONTH'] = df['FECHA'].dt.month
        df["KEY"] = str(year)+str(month)
        d1 = df[["KEY","CLASIFICACION", "CANAL", "NART", "DESCRIPCION","YEAR","MONTH","QUANTITY"]]
        d1 = d1[d1['QUANTITY'].notna()]
        d1 = d1[d1['CANAL'].notna()]
        d1 = d1[d1['CLASIFICACION'].notna()]
        d1 = d1[d1['NART'].notna()]
        d1 = d1[d1['DESCRIPCION'].notna()]
        d1.columns = ["id","clasificacion","canal","nart","descripcion","year","month","cantidad"]
        result = d1.to_json(orient="records")
        errors = dataCheck(result)
        if errors:
            return { 'error': True, 'message': 'Error en los datos enviados', 'details': errors }
        parsed = json.loads(result)
        res = sendDataLaunch(parsed)
        return res, ""
    except KeyError as err:
        error = str(err.__str__()).split(sep=": ")
        column_error = error[1].replace("[","").replace("]","").replace("\"","")
        return { 'error': True, 'message' : f"No se encontraron las columna(s): {column_error} en el archivo 'LAUNCH'"}  
    except:
        print('Error load :', sys.exc_info())
        return { 'error': True, 'message' : "Error en el archivo, por favor revisar el modelo de carga"}

def LoadPromo(df, year, month):
    try:
        df = df.melt(id_vars = ["CLASIFICACION", "TIPO_PROMO", "CANAL", "APPLICATION_FORM", "NART", "DESCRIPCION"], var_name = "FECHA", value_name = "QUANTITY")
        df = df.drop(labels=[0], axis=0)
        df['YEAR'] = df['FECHA'].dt.year
        df['MONTH'] = df['FECHA'].dt.month
        df["KEY"] = str(year)+str(month)
        d1 = df[["KEY","CLASIFICACION", "TIPO_PROMO", "CANAL", "APPLICATION_FORM", "NART", "DESCRIPCION", "YEAR", "MONTH", "QUANTITY"]]
        d1 = d1[d1['CLASIFICACION'].notna()]
        d1 = d1[d1['TIPO_PROMO'].notna()]
        d1 = d1[d1['CANAL'].notna()]
        d1 = d1[d1['APPLICATION_FORM'].notna()]
        d1 = d1[d1['NART'].notna()]
        d1 = d1[d1['DESCRIPCION'].notna()]
        d1 = d1[d1['QUANTITY'].notna()]
        d1.columns = ["id","clasificacion","tipo_promo","canal","application_form","nart","descripcion","year","month","cantidad"]
        result = d1.to_json(orient="records")
        errors = dataCheck(result)
        if errors:
            return { 'error': True, 'message': 'Error en los datos enviados', 'details': errors }
        parsed = json.loads(result)
        res = sendDataPromo(parsed)
        return res, ""
    except KeyError as err:
        error = str(err.__str__()).split(sep=": ")
        column_error = error[1].replace("[","").replace("]","").replace("\"","")
        return { 'error': True, 'message' : f"No se encontraron las columna(s): {column_error} en el archivo 'PROMO'"}  
    except:
        print('Error load :', sys.exc_info())
        return { 'error': True, 'message' : "Error en el archivo, por favor revisar el modelo de carga"}

def LoadValorizacion(df, year, month):
    try:
        print('LoadValorizacion')
        new_header = map(lambda x,y: str(x) if str(y)=='nan' else str(x)+'|'+ str(y).upper(), pd.Series(list(df.columns)), pd.Series(list(df.iloc[0])))
        data = df[1:]
        data.columns = new_header
        data = data.melt(id_vars = ["BRAND CATEGORY", "NART", "DESCRIPCION"], var_name = "FECHA_VALUE", value_name = "QUANTITY")
        split = data["FECHA_VALUE"].str.split("|", n = 1, expand = True)
        data["FECHA"] = split[0]
        data["VALUE"] = split[1]
        data.drop(columns = ["FECHA_VALUE"], inplace = True)
        data["FECHA2"] = pd.to_datetime(data["FECHA"], format='%Y-%m-%d')
        data["YEAR"] = data["FECHA2"].dt.year
        data["MONTH"] = data["FECHA2"].dt.month
        data["KEY"] = str(year)+str(month)
        d1 = data[["KEY","BRAND CATEGORY", "NART", "DESCRIPCION", "YEAR", "MONTH", "VALUE", "QUANTITY"]]
        d1 = d1[d1['QUANTITY'].notna()]
        d1 = d1[d1['BRAND CATEGORY'].notna()]
        d1.columns = ["id","brand_category","nart","descripcion","year","month","value","cantidad"]
        result = d1.to_json(orient="records")
        errors = dataCheck(result)
        if errors:
            return { 'error': True, 'message': 'Error en los datos enviados', 'details': errors }   
        parsed = json.loads(result)
        print('result : ', result)
        res = sendDataValorizacion(parsed)
        return res, ""
    except KeyError as err:
        error = str(err.__str__()).split(sep=": ")
        column_error = error[1].replace("[","").replace("]","").replace("\"","")
        return { 'error': True, 'message' : f"No se encontraron las columna(s): {column_error} en el archivo 'VALORZACION'"}  
    except:
        print('Error load :', sys.exc_info())
        return { 'error': True, 'message' : "Error en el archivo, por favor revisar el modelo de carga"}

def LoadShoppers(df, year, month):
    try:
        df = df.melt(id_vars = ["CLASIFICACION", "TIPO_PROMO", "CANAL", "APPLICATION_FORM", "NART", "DESCRIPCION"], var_name = "FECHA", value_name = "QUANTITY")
        df = df.drop(labels=[0], axis=0)
        df['YEAR'] = df['FECHA'].dt.year
        df['MONTH'] = df['FECHA'].dt.month
        df["KEY"] = str(year)+str(month)
        d1 = df[["KEY","CLASIFICACION", "TIPO_PROMO", "CANAL", "APPLICATION_FORM", "NART", "DESCRIPCION", "YEAR", "MONTH", "QUANTITY"]]
        d1 = d1[d1['CLASIFICACION'].notna()]
        d1 = d1[d1['TIPO_PROMO'].notna()]
        d1 = d1[d1['CANAL'].notna()]
        d1 = d1[d1['APPLICATION_FORM'].notna()]
        d1 = d1[d1['NART'].notna()]
        d1 = d1[d1['DESCRIPCION'].notna()]
        d1 = d1[d1['QUANTITY'].notna()]
        d1.columns = ["id","clasificacion","tipo_promo","canal","application_form","nart","descripcion","year","month","cantidad"]
        result = d1.to_json(orient="records")
        errors = dataCheck(result)
        if errors:
            return { 'error': True, 'message': 'Error en los datos enviados', 'details': errors }
        parsed = json.loads(result)
        res = sendDataShoppers(parsed)
        return res, ""
    except KeyError as err:
        error = str(err.__str__()).split(sep=": ")
        column_error = error[1].replace("[","").replace("]","").replace("\"","")
        return { 'error': True, 'message' : f"No se encontraron las columna(s): {column_error} en el archivo 'SHOPPER'"}  
    except:
        print('Error load :', sys.exc_info())
        return { 'error': True, 'message' : "Error en el archivo, por favor revisar el modelo de carga"}


def LoadForecast(df, year, month):
    try:
        df["id"] = str(year)+str(month)
        d1 = df[["id","Input","CLASIF","BPU","Brand Category","Application Form","year","month","R&O","MSO","Net Sales S/. ('000)"]]
        d1.columns = ["id","input","clasificacion","bpu","brand_category","application_form","year","month","r_o","mso","net_sales"]
        d1['year'].fillna(0,inplace=True)
        d1['month'].fillna(0,inplace=True)
        d1['r_o'].fillna(0,inplace=True)
        d1['mso'].fillna(0,inplace=True)
        d1['net_sales'].fillna(0,inplace=True)
        d1.fillna('N/A', inplace=True)
        d1.is_copy = False
        result = d1.to_json(orient="records")
        parsed = json.loads(result)
        res = sendDataForecast(parsed)
        errors = dataCheck(result)
        if errors:
            return { 'error': True, 'message': 'Error en los datos enviados', 'details': errors }
        return res, ""
    except KeyError as err:
        error = str(err.__str__()).split(sep=": ")
        column_error = error[1].replace("[","").replace("]","").replace("\"","")
        return { 'error': True, 'message' : f"No se encontraron las columna(s): {column_error} en el archivo 'FORECAST'"}  
    except:
        print('Error load :', sys.exc_info())
        return { 'error': True, 'message' : "Error en el archivo, por favor revisar el modelo de carga" }


def createExcelFile(values, column_list, file_id, data_path):
    try:
        writer = pd.ExcelWriter(data_path, engine='xlsxwriter')
        df = pd.DataFrame(values, columns=column_list)
        df.to_excel(writer, file_id, index=False)
        writer.save()
        return data_path
    except:
        return ""

def createTemplate(filename, template_path, data_path, year, month):
    try:
        file_path = join(template_path, filename)
        df = pd.read_excel(file_path)
        month_list = []
        curr_month = datetime.strptime("01/"+month+"/"+year, "%d/%m/%Y")
        for _ in range(18): # Avanzando año y medio
            month_list.append(curr_month.strftime("%d/%m/%Y")) 
            next_month = (curr_month.replace(day=1) + timedelta(days=32)).replace(day=1)
            curr_month = next_month
        df = df.reindex(columns=df.columns.tolist() + month_list)
        new_file_path = join(data_path, filename)
        writer = pd.ExcelWriter(new_file_path, engine='xlsxwriter')
        df.to_excel(writer, filename[0:-5], index=False)
        writer.save()
        return filename
    except:
        print(sys.exc_info()[1])
        return ""

def createTemplateValorizacion(filename, template_path, data_path, year, month):
    try:
        file_path = join(template_path, filename)
        df = pd.read_excel(file_path)
        month_list = ['BRAND CATEGORY','NART','DESCRIPCION','VALUES']
        curr_month = datetime.strptime("01/"+month+"/"+year, "%d/%m/%Y")
        df = pd.read_excel(file_path)
        df.loc[1, ['BRAND CATEGORY','NART','DESCRIPCION']] = ''
        for _ in range(18):
            month_list.append(curr_month.strftime("%d/%m/%Y"))
            next_month = (curr_month.replace(day=1) + timedelta(days=32)).replace(day=1)
            curr_month = next_month
        df = df.reindex(columns=month_list)
        df.loc[0, 'VALUES'] = 'pricelist'
        df.loc[1, 'VALUES'] = 'discount'
        df.loc[2, 'VALUES'] = 'rebate'
        df.loc[3, 'VALUES'] = 'com / cop'
        new_file_path = join(data_path, filename)
        writer = pd.ExcelWriter(new_file_path, engine='xlsxwriter')
        df.to_excel(writer, filename[0:-5], index=False)
        writer.save()
        # month_list = []
        # curr_month = datetime.strptime(year+"-"+month+"-01", "%Y-%m-%d")
        # for _ in range(18): # Avanzando año y medio
        #     month_list.append(curr_month.strftime("%Y-%m-%d")) 
        #     next_month = (curr_month.replace(day=1) + timedelta(days=32)).replace(day=1)
        #     curr_month = next_month
        # df = df.reindex(columns=df.columns.tolist() + month_list)
        # new_file_path = join(data_path, filename)
        # writer = pd.ExcelWriter(new_file_path, engine='xlsxwriter')
        # df.to_excel(writer, filename[0:-5], index=False)
        # writer.save()
        return filename
    except:
        print(sys.exc_info()[1])
        return ""

def createFileProductosOtros(data):
    try:
        filename = "Productos_sin_clasificar.xlsx"
        workbook = xlsxwriter.Workbook(f"api/data/{filename}")
        cell_format = workbook.add_format()
        cell_format.set_text_wrap()
        cell_format.set_align('top')
        cell_format.set_align('left=')
        worksheet = workbook.add_worksheet("NoClasificados")
        keys = list(data[0].keys())
        worksheet.write('A1',keys[0])
        worksheet.write('B1',keys[1])
        worksheet.write('C1',keys[2])
        worksheet.write('D1',keys[3])
        worksheet.write('E1',keys[4])
        worksheet.write('F1',keys[5])
        worksheet.write('G1',keys[6])
        worksheet.write('H1',keys[7])
        worksheet.write('I1',keys[8])
        worksheet.write('J1',keys[9])
        rowIndex = 2
        for row in data:
            worksheet.write(f'A{rowIndex}', row['BG'])
            worksheet.write(f'B{rowIndex}', row['Material'])
            worksheet.write(f'C{rowIndex}', row['SPGR'])
            worksheet.write(f'D{rowIndex}', row['TIPO'])
            worksheet.write(f'E{rowIndex}', row['Descripcion'])
            worksheet.write(f'F{rowIndex}', row['Portafolio'])
            worksheet.write(f'G{rowIndex}', row['BPU'])
            worksheet.write(f'H{rowIndex}', row['BrandCategory'])
            worksheet.write(f'I{rowIndex}', row['ApplicationForm'])
            worksheet.write(f'J{rowIndex}', row['EAN'])
            rowIndex+=1
        workbook.close()
        return filename
    except:
        print('error createFileProductosOtros :', sys.exc_info())
        return ""