

from os import listdir, unlink, getcwd
from os.path import join
from pathlib import Path

DATA_PATH = join(getcwd(),'src','data')

def cleanDataFolder():
    for file in Path(DATA_PATH).glob('*.xlsx'):
        unlink(file)

ALLOWED_EXT = set(['xlsx','xls'])
def allowed_extensions(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

ALLOWED_NAMES = set(['BASELINE','LAUNCH','PROMO','VALORIZACION','PRODUCTOS'])
def allowed_names(filename):
    return '.' in filename and filename.rsplit(' - ', 1)[0] in ALLOWED_NAMES

def checkFiles():
    return len(listdir(DATA_PATH))

AREA_BY_TABLE = {
    "Maestro_baseline" : { "area_id" : 1, "area_name" : "Supply"},
    "Maestro_launch" : { "area_id" : 2, "area_name" : "Marketing"},
    "Maestro_promo" : { "area_id" : 3, "area_name" : "Ventas"},
    "Maestro_valorizacion" : { "area_id" : 4, "area_name" : "Finanzas"},
    "Maestro_Shopper" : { "area_id" : 5, "area_name" : "Shopper"},
}

DB_TABLE_AREA = {
    "1":"baseline",
    "2":"launch",
    "3":"promo",
    "4":"valorizacion",
    "5":"shopper"
}

