from api.utils.dataLoader import *
from os import getcwd, scandir, remove, listdir
from os.path import join
import pandas as pd




data_path = join(getcwd(),'api','data')
def cleanDataFolder():
    for file in scandir(data_path):
        remove(file)

ALLOWED_EXT = set(['xlsx','xls'])
def allowed_extensions(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

ALLOWED_NAMES = set(['BASELINE','LAUNCH','PROMO','VALORIZACION','PRODUCTOS'])
def allowed_names(filename):
    return '.' in filename and filename.rsplit(' - ', 1)[0] in ALLOWED_NAMES

def checkFiles():
    dir_files = listdir(data_path)
    n_files = len(dir_files)
    return n_files

def checkExcelFiles():
    for f in scandir(data_path):
        print("Excel File Name : ", f.name)
        xl = pd.ExcelFile(f)
        print("Sheet Names", xl.sheet_names)
        for sheet in xl.sheet_names:
            if sheet == 'Hoja1':
                df = pd.read_excel(f, sheet)
                if 'BASELINE' in f.name:
                    return Loadbaseline(df)
                if 'LAUNCH' in f.name:
                    return LoadLaunch(df)
                if 'PROMO' in f.name:
                    return LoadPromo(df)
                if 'VALORIZACION' in f.name:
                    return LoadValorizacion(df)
                else:
                    return '.'

db_table_area = {
    "1" : "baseline",
    "2" : "launch",
    "3" : "promo",
    "4" : "valorizacion"
}
def getData(id, area_id):
    area = db_table_area[str(area_id)]
    if area == "baseline":
        return requestDataBaseline(id)
    elif area == "launch":
        return requestDataLaunch(id)
    elif area == "promo":
        return requestDataPromo(id)
    elif area == "valorizacion":
        return requestDataValorizacion(id) 
    else:
        print("Area no encontrada")
        return '.'

def checkInfoMonth(year, month):
    if int(month) < 10:
        month = f"0{month}"
    info = requestIDbyPeriod(f"{year}{month}")
    return { 'result' : info }
     