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


db_table_area = {
    "1" : "baseline",
    "2" : "launch",
    "3" : "promo",
    "4" : "valorizacion"
}
def checkExcelFiles(area_id, year, month):
    for f in scandir(data_path):
        xl = pd.ExcelFile(f)
        for sheet in xl.sheet_names:
            if sheet == 'Hoja1':
                df = pd.read_excel(f, sheet)
                if area_id == 1:
                    return Loadbaseline(df, year, month)
                if area_id == 2:
                    return LoadLaunch(df, year, month)
                if area_id == 3:
                    return LoadPromo(df, year, month)
                if area_id == 4:
                    return LoadValorizacion(df, year, month)
                else:
                    return ""

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
    if int(month) < 10 and len(month) == 1:
        month = f"0{int(month)}"
    info = requestIDbyPeriod(f"{year}{month}")
    return { 'result' : info }


def checkDeleteTable(area_id, year, month):
    area_id = int(area_id)
    if int(month) < 10 and len(month) == 1:
        month = f"0{int(month)}"
    if area_id == 1:
        return deleteDataBaseline(year+month)
    if area_id == 2:
        return deleteDataLaunch(year+month)
    if area_id == 3:
        return deleteDataPromo(year+month)
    if area_id == 4:
        return deleteDataValorizacion(year+month)
    else:
        return ""

     