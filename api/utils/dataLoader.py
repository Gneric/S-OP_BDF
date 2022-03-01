import sys
import json
import re
import pandas as pd
import string
from datetime import datetime, timedelta
import xlsxwriter
from api.utils.hasura_api import sendDataBaseline, sendDataForecast, sendDataLaunch, sendDataPromo, sendDataShoppers, sendDataValorizacion, upload_data_maestro
from api.utils.rowsCheker import dataCheck, dataMaestroCheck

def Loadbaseline(df, year, month, file_id):
    try:
        print('LoadBaseline w file id :', file_id)
        df = df.melt(id_vars = ["CLASIFICACION", "NART", "DESCRIPCION"], var_name = "FECHA", value_name = "QUANTITY")
        df = df.drop(labels=[0], axis=0)
        df['YEAR'] = df['FECHA'].dt.year
        df['MONTH'] = df['FECHA'].dt.month 
        df["KEY"] = str(year)+str(month)
        df["FILE_ID"] = file_id
        df["DESCRIPCION"] = ""
        d1 = df[["KEY","CLASIFICACION", "NART", "DESCRIPCION","YEAR","MONTH","QUANTITY","FILE_ID"]]
        d1 = d1[d1['CLASIFICACION'].notna()]
        d1 = d1[d1['NART'].notna()]
        d1 = d1[d1['QUANTITY'].notna()]
        d1.columns = ["id","clasificacion","nart","descripcion","year","month","cantidad","file_id"]
        d1 = d1.groupby(["id","clasificacion","nart","descripcion","year","month","file_id"]).sum().reset_index()
        result = d1.to_json(orient="records")
        check_result = dataCheck(result)
        if check_result['error_check'] == True:
            return { 'error': check_result['error_check'], 'warning': False, 'message': 'Error en los datos enviados', 'details': check_result['errors'] }
        parsed = json.loads(result)
        res = sendDataBaseline(parsed)
        if check_result['warning_check'] == True:
            return { 'error': False, 'warning': True, 'message': res, 'details': check_result['warnings'] }
        return { 'error': False, 'message': res }
    except KeyError as err:
        error = str(err.__str__()).split(sep=": ")
        column_error = error[1].replace("[","").replace("]","").replace("\"","")
        return { 'error': True, 'message' : f"No se encontraron las columna(s): {column_error} en el archivo 'BASELINE'"}  
    except:
        print('Error load :', sys.exc_info())
        return { 'error': True, 'message' : "Error en el archivo, por favor revisar el modelo de carga" }
    
def LoadLaunch(df, year, month, file_id):
    try:
        print('LoadLaunch w file id :', file_id)
        df = df.melt(id_vars = ["CLASIFICACION", "CANAL", "NART", "DESCRIPCION"], var_name = "FECHA", value_name = "QUANTITY")
        df = df.drop(labels=[0], axis=0)
        df['YEAR'] = df['FECHA'].dt.year
        df['MONTH'] = df['FECHA'].dt.month
        df["KEY"] = str(year)+str(month)
        df["FILE_ID"] = file_id
        df["DESCRIPCION"] = ""
        d1 = df[["KEY","CLASIFICACION", "CANAL", "NART", "DESCRIPCION","YEAR","MONTH","QUANTITY","FILE_ID"]]
        d1 = d1[d1['QUANTITY'].notna()]
        d1 = d1[d1['CANAL'].notna()]
        d1 = d1[d1['CLASIFICACION'].notna()]
        d1 = d1[d1['NART'].notna()]
        d1.columns = ["id","clasificacion","canal","nart","descripcion","year","month","cantidad","file_id"]
        d1 = d1.groupby(["id","clasificacion","canal","nart","descripcion","year","month","file_id"]).sum().reset_index()
        result = d1.to_json(orient="records")
        check_result = dataCheck(result)
        if check_result['error_check'] == True:
            return { 'error': check_result['error_check'], 'warning': False, 'message': 'Error en los datos enviados', 'details': check_result['errors'] }
        parsed = json.loads(result)
        res = sendDataLaunch(parsed)
        if check_result['warning_check'] == True:
            return { 'error': False, 'warning': True, 'message': res, 'details': check_result['warnings'] }
        return { 'error': False, 'message': res }
    except KeyError as err:
        error = str(err.__str__()).split(sep=": ")
        column_error = error[1].replace("[","").replace("]","").replace("\"","")
        return { 'error': True, 'message' : f"No se encontraron las columna(s): {column_error} en el archivo 'LAUNCH'"}  
    except:
        print('Error load :', sys.exc_info())
        return { 'error': True, 'message' : "Error en el archivo, por favor revisar el modelo de carga"}

def LoadPromo(df, year, month, file_id):
    try:
        df = df.melt(id_vars = ["CLASIFICACION", "TIPO_PROMO", "CANAL", "APPLICATION_FORM", "NART", "DESCRIPCION"], var_name = "FECHA", value_name = "QUANTITY")
        df = df.drop(labels=[0], axis=0)
        df['YEAR'] = df['FECHA'].dt.year
        df['MONTH'] = df['FECHA'].dt.month
        df["KEY"] = str(year)+str(month)
        df["FILE_ID"] = file_id
        df["APPLICATION_FORM"] = ""
        df["DESCRIPCION"] = ""
        d1 = df[["KEY","CLASIFICACION", "TIPO_PROMO", "CANAL", "APPLICATION_FORM", "NART", "DESCRIPCION", "YEAR", "MONTH", "QUANTITY","FILE_ID"]]
        d1 = d1[d1['CLASIFICACION'].notna()]
        d1 = d1[d1['TIPO_PROMO'].notna()]
        d1 = d1[d1['CANAL'].notna()]
        d1 = d1[d1['NART'].notna()]
        d1 = d1[d1['QUANTITY'].notna()]
        d1.columns = ["id","clasificacion","tipo_promo","canal","application_form","nart","descripcion","year","month","cantidad","file_id"]
        d1 = d1.groupby(["id","clasificacion","tipo_promo","canal","application_form","nart","descripcion","year","month","file_id"]).sum().reset_index()
        result = d1.to_json(orient="records")
        check_result = dataCheck(result)
        if check_result['error_check'] == True:
            return { 'error': check_result['error_check'], 'warning': False, 'message': 'Error en los datos enviados', 'details': check_result['errors'] }
        parsed = json.loads(result)
        res = sendDataPromo(parsed)
        if check_result['warning_check'] == True:
            return { 'error': False, 'warning': True, 'message': res, 'details': check_result['warnings'] }
        return { 'error': False, 'message': res }
    except KeyError as err:
        error = str(err.__str__()).split(sep=": ")
        column_error = error[1].replace("[","").replace("]","").replace("\"","")
        return { 'error': True, 'message' : f"No se encontraron las columna(s): {column_error} en el archivo 'PROMO'"}  
    except:
        print('Error load :', sys.exc_info())
        return { 'error': True, 'message' : "Error en el archivo, por favor revisar el modelo de carga"}

def LoadValorizacion(df, year, month, file_id):
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
        data["FILE_ID"] = file_id
        data["BRAND CATEGORY"] = ""
        d1 = data[["KEY","BRAND CATEGORY", "NART", "DESCRIPCION", "YEAR", "MONTH", "VALUE", "QUANTITY","FILE_ID"]]
        d1 = d1[d1['QUANTITY'].notna()]
        d1 = d1[d1['BRAND CATEGORY'].notna()]
        d1['DESCRIPCION'] = 'NULL'
        d1 = d1[d1.QUANTITY != 0]
        d1.columns = ["id","brand_category","nart","descripcion","year","month","value","cantidad","file_id"]
        d1 = d1.drop_duplicates(subset=["id","brand_category","nart","descripcion","year","month","value","file_id"])
        result = d1.to_json(orient="records")
        check_result = dataCheck(result)
        if check_result['error_check'] == True:
            return { 'error': check_result['error_check'], 'warning': False, 'message': 'Error en los datos enviados', 'details': check_result['errors'] }
        parsed = json.loads(result)
        res = sendDataValorizacion(parsed)
        if check_result['warning_check'] == True:
            return { 'error': False, 'warning': True, 'message': res, 'details': check_result['warnings'] }
        return { 'error': False, 'message': res }
    except KeyError as err:
        error = str(err.__str__()).split(sep=": ")
        column_error = error[1].replace("[","").replace("]","").replace("\"","")
        return { 'error': True, 'message' : f"No se encontraron las columna(s): {column_error} en el archivo 'VALORZACION'"}  
    except:
        print('Error load :', sys.exc_info())
        return { 'error': True, 'message' : "Error en el archivo, por favor revisar el modelo de carga"}

def LoadShoppers(df, year, month, file_id):
    try:
        df = df.melt(id_vars = ["CLASIFICACION", "TIPO_PROMO", "CANAL", "APPLICATION_FORM", "NART", "DESCRIPCION"], var_name = "FECHA", value_name = "QUANTITY")
        df = df.drop(labels=[0], axis=0)
        df['YEAR'] = df['FECHA'].dt.year
        df['MONTH'] = df['FECHA'].dt.month
        df["KEY"] = str(year)+str(month)
        df["FILE_ID"] = file_id
        df["APPLICATION_FORM"] = ""
        df["DESCRIPCION"] = ""
        d1 = df[["KEY","CLASIFICACION", "TIPO_PROMO", "CANAL", "APPLICATION_FORM", "NART", "DESCRIPCION", "YEAR", "MONTH", "QUANTITY","FILE_ID"]]
        d1 = d1[d1['CLASIFICACION'].notna()]
        d1 = d1[d1['TIPO_PROMO'].notna()]
        d1 = d1[d1['CANAL'].notna()]
        d1 = d1[d1['NART'].notna()]
        d1 = d1[d1['QUANTITY'].notna()]
        d1.columns = ["id","clasificacion","tipo_promo","canal","application_form","nart","descripcion","year","month","cantidad","file_id"]
        d1 = d1.groupby(["id","clasificacion","tipo_promo","canal","application_form","nart","descripcion","year","month","file_id"]).sum().reset_index()
        result = d1.to_json(orient="records")
        check_result = dataCheck(result)
        if check_result['error_check'] == True:
            return { 'error': check_result['error_check'], 'warning': False, 'message': 'Error en los datos enviados', 'details': check_result['errors'] }
        parsed = json.loads(result)
        res = sendDataShoppers(parsed)
        if check_result['warning_check'] == True:
            return { 'error': False, 'warning': True, 'message': res, 'details': check_result['warnings'] }
        return { 'error': False, 'message': res }
    except KeyError as err:
        print('Error load Shopper:', sys.exc_info())
        error = str(err.__str__()).split(sep=": ")
        column_error = error[1].replace("[","").replace("]","").replace("\"","")
        return { 'error': True, 'message' : f"No se encontraron las columna(s): {column_error} en el archivo 'SHOPPER'"}  
    except:
        print('Error load Shopper:', sys.exc_info())
        return { 'error': True, 'message' : "Error en el archivo, por favor revisar el modelo de carga"}


def LoadForecast(df, year, month, file_id):
    try:
        df["id"] = str(year)+str(month)
        df["FILE_ID"] = file_id
        d1 = df[["id","Input","CLASIF","BPU","Brand Category","Application Form","year","month","R&O","MSO","Net Sales S/. ('000)","FILE_ID"]]
        d1["BPU"] = d1["BPU"].replace([0,'','0'], 'N/A')
        d1["Brand Category"] = ""
        d1["Application Form"] = ""
        d1.columns = ["id","input","clasificacion","bpu","brand_category","application_form","year","month","r_o","mso","net_sales","file_id"]
        d1['year'].fillna(0,inplace=True)
        d1['month'].fillna(0,inplace=True)
        d1['r_o'].fillna(0,inplace=True)
        d1['mso'].fillna(0,inplace=True)
        d1['net_sales'].fillna(0,inplace=True)
        d1.fillna('N/A', inplace=True)
        d1.is_copy = False
        d1.groupby(["nart"]).sum()
        result = d1.to_json(orient="records")
        check_result = dataCheck(result)
        if check_result['error_check'] == True:
            return { 'error': check_result['error_check'], 'warning': False, 'message': 'Error en los datos enviados', 'details': check_result['errors'] }
        parsed = json.loads(result)
        res = sendDataForecast(parsed)
        if check_result['warning_check'] == True:
            return { 'error': False, 'warning': True, 'message': res, 'details': check_result['warnings'] }
        return { 'error': False, 'message': res }
    except KeyError as err:
        print('Error load :', sys.exc_info())
        error = str(err.__str__()).split(sep=": ")
        column_error = error[1].replace("[","").replace("]","").replace("\"","")
        return { 'error': True, 'message' : f"No se encontraron las columna(s): {column_error} en el archivo 'FORECAST'"}  
    except:
        print('Error load :', sys.exc_info())
        return { 'error': True, 'message' : "Error en el archivo, por favor revisar el modelo de carga" }

def LoadProducts(df):
    try:
        df = df[["BG","Material","SPGR","TIPO","Descripcion","Portafolio","BPU","BrandCategory","ApplicationForm","EAN"]]
        df["EAN"] = df["EAN"].replace([0,'','0'], 'N/A')
        df = df.fillna('')
        df["BG"] = df["BG"].apply(str)
        df["Material"] = df["Material"].apply(str)
        df["SPGR"] = df["SPGR"].apply(str)
        df["EAN"] = df["EAN"].apply(str)
        result = df.to_json(orient="records")
        check_result = dataMaestroCheck(result)
        parsed = json.loads(check_result)
        res = upload_data_maestro(parsed)
        return res
    except KeyError as err:
        print('Error load :', sys.exc_info())
        error = str(err.__str__()).split(sep=": ")
        column_error = error[1].replace("[","").replace("]","").replace("\"","")
        return { 'error': True, 'message' : f"No se encontraron las columna(s): {column_error} en el archivo 'PRODUCTS'"}  
    except:
        print('Error load :', sys.exc_info())
        return { 'error': True, 'message' : "Error en el archivo, por favor revisar el modelo de carga" }
    


def createExcelFile(file_id, area_id, data, xslx_name, xslx_path):
    try:
        year = file_id[:4]
        month = file_id[4:]
        # De data por lineas a df
        if area_id == 4:
            df = pd.read_json(json.dumps(data), orient='records')
            indexes = [ str(x) for x in df.columns if str(x) not in ["year", "month", "value", "cantidad"]]
            df["value"] = df["value"].map({ 'price list': 1, 'discount': 2, 'rebates':3, 'com / cop': 4 })
            df["periodo"] = (df["year"].astype(int)+df["month"].astype(int)).astype(str)+"-"+df["value"].astype(str)
            df = pd.pivot_table(df, index=indexes,columns=["periodo"],values="cantidad", fill_value=0).reset_index()
            json_data = df.to_json(orient="records")
            json_list = json.loads(json_data)

            filename_w_ext = f"{xslx_name}.xlsx"
            filename_path = f'api/data/{filename_w_ext}'
            workbook = xlsxwriter.Workbook(f'api/data/{filename_w_ext}')
            worksheet = workbook.add_worksheet(xslx_name)
            worksheet.write('A1','BRAND CATEGORY')
            worksheet.write('B1','NART')
            worksheet.write('C1','DESCRIPCION')
            mnth = 4
            curr_month = datetime.strptime(year+"-"+month+"-01", '%Y-%m-%d')
            for _ in range(18):
                date_format = workbook.add_format({'num_format': 'mm-yyyy'})
                worksheet.write_datetime(f'{checkColumnByRange(mnth)}1', curr_month, date_format)
                worksheet.write_datetime(f'{checkColumnByRange(mnth+1)}1', curr_month, date_format)
                worksheet.write_datetime(f'{checkColumnByRange(mnth+2)}1', curr_month, date_format)
                worksheet.write_datetime(f'{checkColumnByRange(mnth+3)}1', curr_month, date_format)
                worksheet.write(f'{checkColumnByRange(mnth)}2', 'price list')
                worksheet.write(f'{checkColumnByRange(mnth+1)}2', 'discount')
                worksheet.write(f'{checkColumnByRange(mnth+2)}2', 'rebate')
                worksheet.write(f'{checkColumnByRange(mnth+3)}2', 'comp / cop')
                next_month = (curr_month.replace(day=1) + timedelta(days=32)).replace(day=1)
                curr_month = next_month
                mnth += 4
            row_num = 2
            for row in json_list:
                col_num = 1
                dic_row = dict(row)
                dic_row.pop("id")
                for key in dic_row:
                    if re.match('[0-9]{4}-[0-9]{1}', key):
                        if int(key[5:]) in [ 2, 3 ]:
                            percent_fmt = workbook.add_format({'num_format': '0.00%'})
                            worksheet.write(f'{checkColumnByRange(col_num)}{row_num + 1}', dic_row[key], percent_fmt)
                        else:
                            worksheet.write(f'{checkColumnByRange(col_num)}{row_num + 1}', dic_row[key])
                    else:
                        worksheet.write(f'{checkColumnByRange(col_num)}{row_num + 1}', dic_row[key])
                    col_num = col_num + 1
                row_num = row_num + 1
            workbook.close()
            return filename_path
        else:
            df = pd.read_json(json.dumps(data), orient='records')
            indexes = [ str(x) for x in df.columns if str(x) not in ["year", "month", "value", "cantidad"]]
            df["periodo"] = df["year"]+df["month"]
            df = pd.pivot_table(df, index=indexes,columns=["periodo"],values="cantidad", fill_value=0).reset_index()
            json_data = df.to_json(orient="records")
            json_list = json.loads(json_data)

            filename_w_ext = f"{xslx_name}.xlsx"
            filename_path = f'api/data/{filename_w_ext}'
            workbook = xlsxwriter.Workbook(filename_path)
            worksheet = workbook.add_worksheet(xslx_name)
            if xslx_name == 'promo' or xslx_name == 'shopper':
                mnth = 7
                worksheet.write('A1','CLASIFICACION')
                worksheet.write('B1','TIPO_PROMO')
                worksheet.write('C1','CANAL')
                worksheet.write('D1','APPLICATION_FORM')
                worksheet.write('E1','NART')
                worksheet.write('F1','DESCRIPCION')
                curr_month = datetime.strptime(year+"-"+month+"-01", '%Y-%m-%d')
                for _ in range(mnth, mnth+18):
                    date_format = workbook.add_format({'num_format': 'mm-yyyy'})
                    worksheet.write_datetime(f'{checkColumnByRange(_)}1', curr_month, date_format)
                    next_month = (curr_month.replace(day=1) + timedelta(days=32)).replace(day=1)
                    curr_month = next_month
                row_num = 1
                for row in json_list:
                    col_num = 1
                    dic_row = dict(row)
                    dic_row.pop("id")
                    for key in dic_row:
                        worksheet.write(f'{checkColumnByRange(col_num)}{row_num + 1}', dic_row[key])
                        col_num = col_num + 1
                    row_num = row_num + 1
            elif xslx_name == 'launch':
                mnth = 5
                worksheet.write('A1','CLASIFICACION')
                worksheet.write('B1','CANAL')
                worksheet.write('C1','NART')
                worksheet.write('D1','DESCRIPCION')
                curr_month = datetime.strptime(year+"-"+month+"-01", '%Y-%m-%d')
                for _ in range(mnth, mnth+18):
                    date_format = workbook.add_format({'num_format': 'mm-yyyy'})
                    worksheet.write_datetime(f'{checkColumnByRange(_)}1', curr_month, date_format)
                    next_month = (curr_month.replace(day=1) + timedelta(days=32)).replace(day=1)
                    curr_month = next_month
                row_num = 1
                for row in json_list:
                    col_num = 1
                    dic_row = dict(row)
                    dic_row.pop("id")
                    for key in dic_row:
                        worksheet.write(f'{checkColumnByRange(col_num)}{row_num + 1}', dic_row[key])
                        col_num = col_num + 1
                    row_num = row_num + 1
            else:
                mnth = 4
                worksheet.write('A1','CLASIFICACION')
                worksheet.write('B1','NART')
                worksheet.write('C1','DESCRIPCION')
                curr_month = datetime.strptime(year+"-"+month+"-01", '%Y-%m-%d')
                for _ in range(mnth, mnth+18):
                    date_format = workbook.add_format({'num_format': 'mm-yyyy'})
                    worksheet.write_datetime(f'{checkColumnByRange(_)}1', curr_month, date_format)
                    next_month = (curr_month.replace(day=1) + timedelta(days=32)).replace(day=1)
                    curr_month = next_month
                row_num = 1
                for row in json_list:
                    col_num = 1
                    dic_row = dict(row)
                    dic_row.pop("id")
                    for key in dic_row:
                        worksheet.write(f'{checkColumnByRange(col_num)}{row_num + 1}', dic_row[key])
                        col_num = col_num + 1
                    row_num = row_num + 1
            workbook.close()
            return filename_path
    except:
        print('error createExcelFile :', sys.exc_info())
        return ""


def checkColumnByRange(mnth):
    num2alpha = dict(zip(range(1, 27), string.ascii_uppercase))
    ltr = ""
    fltr = ""
    if mnth >= 53:
        fltr = "B"
        ltr = num2alpha[mnth-52]
    if mnth > 26 and mnth < 53:
        fltr = "A"
        ltr = num2alpha[mnth-26]
    if mnth <= 26:
        ltr = num2alpha[mnth]
    return fltr+ltr

def createTemplate(filename, year, month):
    try:
        filename_w_ext = f"{filename}.xlsx"
        print(filename)
        workbook = xlsxwriter.Workbook(f'api/data/{filename_w_ext}')
        worksheet = workbook.add_worksheet(filename)
        if filename == 'promo' or filename == 'shopper':
            mnth = 7
            worksheet.write('A1','CLASIFICACION')
            worksheet.write('B1','TIPO_PROMO')
            worksheet.write('C1','CANAL')
            worksheet.write('D1','APPLICATION_FORM')
            worksheet.write('E1','NART')
            worksheet.write('F1','DESCRIPCION')
        elif filename == 'launch':
            mnth = 5
            worksheet.write('A1','CLASIFICACION')
            worksheet.write('B1','CANAL')
            worksheet.write('C1','NART')
            worksheet.write('D1','DESCRIPCION')
        else:
            mnth = 4
            worksheet.write('A1','CLASIFICACION')
            worksheet.write('B1','NART')
            worksheet.write('C1','DESCRIPCION')
        curr_month = datetime.strptime(year+"-"+month+"-01", '%Y-%m-%d')
        for _ in range(mnth, mnth+18):
            date_format = workbook.add_format({'num_format': 'mm-yyyy'})
            worksheet.write_datetime(f'{checkColumnByRange(_)}1', curr_month, date_format)
            next_month = (curr_month.replace(day=1) + timedelta(days=32)).replace(day=1)
            curr_month = next_month
        workbook.close()
        return filename_w_ext
    except:
        print(sys.exc_info()[1])
        return ""

def createTemplateValorizacion(filename, year, month):
    try:
        filename_w_ext = f"{filename}.xlsx"
        workbook = xlsxwriter.Workbook(f'api/data/{filename_w_ext}')
        worksheet = workbook.add_worksheet(filename)
        worksheet.write('A1','BRAND CATEGORY')
        worksheet.write('B1','NART')
        worksheet.write('C1','DESCRIPCION')
        mnth = 4
        curr_month = datetime.strptime(year+"-"+month+"-01", '%Y-%m-%d')
        for _ in range(18):
            date_format = workbook.add_format({'num_format': 'mm-yyyy'})
            worksheet.write_datetime(f'{checkColumnByRange(mnth)}1', curr_month, date_format)
            worksheet.write_datetime(f'{checkColumnByRange(mnth+1)}1', curr_month, date_format)
            worksheet.write_datetime(f'{checkColumnByRange(mnth+2)}1', curr_month, date_format)
            worksheet.write_datetime(f'{checkColumnByRange(mnth+3)}1', curr_month, date_format)
            worksheet.write(f'{checkColumnByRange(mnth)}2', 'price list')
            worksheet.write(f'{checkColumnByRange(mnth+1)}2', 'discount')
            worksheet.write(f'{checkColumnByRange(mnth+2)}2', 'rebates')
            worksheet.write(f'{checkColumnByRange(mnth+3)}2', 'com / cop')
            next_month = (curr_month.replace(day=1) + timedelta(days=32)).replace(day=1)
            curr_month = next_month
            mnth += 4
        workbook.close()
        return filename_w_ext
    except:
        print(sys.exc_info())
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
        if data:
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
                worksheet.write(f'A{rowIndex}', row['ApplicationForm'])
                worksheet.write(f'B{rowIndex}', row['BG'])
                worksheet.write(f'C{rowIndex}', row['BPU'])
                worksheet.write(f'D{rowIndex}', row['BrandCategory'])
                worksheet.write(f'E{rowIndex}', row['Descripcion'])
                worksheet.write(f'F{rowIndex}', row['EAN'])
                worksheet.write(f'G{rowIndex}', row['Material'])
                worksheet.write(f'H{rowIndex}', row['Portafolio'])
                worksheet.write(f'I{rowIndex}', row['SPGR'])
                worksheet.write(f'J{rowIndex}', row['TIPO'])
                rowIndex+=1
        else:
            worksheet.write('A1','ApplicationForm')
            worksheet.write('B1','BG')
            worksheet.write('C1','BPU')
            worksheet.write('D1','BrandCategory')
            worksheet.write('E1','Descripcion')
            worksheet.write('F1','EAN')
            worksheet.write('G1','Material')
            worksheet.write('H1','Portafolio')
            worksheet.write('I1','SPGR')
            worksheet.write('J1','TIPO')
        workbook.close()
        return filename
    except:
        print('error createFileProductosOtros :', sys.exc_info())
        return ""

def createCloneMaestro(data):
    try:
        filename = "Maestro_productos.xlsx"
        workbook = xlsxwriter.Workbook(f"api/data/{filename}")
        cell_format = workbook.add_format()
        cell_format.set_text_wrap()
        cell_format.set_align('top')
        cell_format.set_align('left=')
        worksheet = workbook.add_worksheet("Productos")
        if data:
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
                ean_format = workbook.add_format({'num_format': '0'})
                worksheet.write(f'A{rowIndex}', row['ApplicationForm'])
                worksheet.write(f'B{rowIndex}', row['BG'])
                worksheet.write(f'C{rowIndex}', row['BPU'])
                worksheet.write(f'D{rowIndex}', row['BrandCategory'])
                worksheet.write(f'E{rowIndex}', row['Descripcion'])
                worksheet.write(f'F{rowIndex}', row['EAN'].replace('.0',''))
                worksheet.write(f'G{rowIndex}', row['Material'])
                worksheet.write(f'H{rowIndex}', row['Portafolio'])
                worksheet.write(f'I{rowIndex}', row['SPGR'])
                worksheet.write(f'J{rowIndex}', row['TIPO'])
                rowIndex+=1
        else:
            worksheet.write('A1','ApplicationForm')
            worksheet.write('B1','BG')
            worksheet.write('C1','BPU')
            worksheet.write('D1','BrandCategory')
            worksheet.write('E1','Descripcion')
            worksheet.write('F1','EAN')
            worksheet.write('G1','Material')
            worksheet.write('H1','Portafolio')
            worksheet.write('I1','SPGR')
            worksheet.write('J1','TIPO')
        workbook.close()
        return filename
    except:
        print('error createFileProductosOtros :', sys.exc_info())
        return ""