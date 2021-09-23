from datetime import datetime
import json
import pandas as pd

from api.utils.hasura_api import *

def Loadbaseline(df):
    df = df.melt(id_vars = ["CLASIFICACION", "NART", "DESCRIPCION"], var_name = "FECHA", value_name = "QUANTITY")
    df = df.drop(labels=[0], axis=0)
    df['YEAR'] = df['FECHA'].dt.year
    df['MONTH'] = df['FECHA'].dt.month 
    df["KEY"] = datetime.now().strftime("%Y%m")
    d1 = df[["KEY","CLASIFICACION", "NART", "DESCRIPCION","YEAR","MONTH","QUANTITY"]]
    d1 = d1[d1['CLASIFICACION'].notna()]
    d1 = d1[d1['NART'].notna()]
    d1 = d1[d1['DESCRIPCION'].notna()]
    d1 = d1[d1['QUANTITY'].notna()]
    d1.columns = ["id","clasificacion","nart","descripcion","year","month","cantidad"]
    result = d1.to_json(orient="records")
    parsed = json.loads(result)
    res = sendDataBaseline(parsed)
    return res
    
def LoadLaunch(df):
    df = df.melt(id_vars = ["CLASIFICACION", "CANAL", "NART", "DESCRIPCION"], var_name = "FECHA", value_name = "QUANTITY")
    df = df.drop(labels=[0], axis=0)
    df['YEAR'] = df['FECHA'].dt.year
    df['MONTH'] = df['FECHA'].dt.month
    df["KEY"] = datetime.now().strftime("%Y%m")
    d1 = df[["KEY","CLASIFICACION", "CANAL", "NART", "DESCRIPCION","YEAR","MONTH","QUANTITY"]]
    d1 = d1[d1['QUANTITY'].notna()]
    d1 = d1[d1['CANAL'].notna()]
    d1 = d1[d1['CLASIFICACION'].notna()]
    d1 = d1[d1['NART'].notna()]
    d1 = d1[d1['DESCRIPCION'].notna()]
    d1.columns = ["id","clasificacion","canal","nart","descripcion","year","month","cantidad"]
    result = d1.to_json(orient="records")
    parsed = json.loads(result)
    res = sendDataLaunch(parsed)
    return res

def LoadPromo(df):
    df = df.melt(id_vars = ["CLASIFICACION", "TIPO_PROMO", "CANAL", "APPLICATION_FORM", "NART", "DESCRIPCION"], var_name = "FECHA", value_name = "QUANTITY")
    df = df.drop(labels=[0], axis=0)
    df['YEAR'] = df['FECHA'].dt.year
    df['MONTH'] = df['FECHA'].dt.month
    df["KEY"] = datetime.now().strftime("%Y%m")
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
    parsed = json.loads(result)
    #print(json.dumps(parsed, indent=4))
    res = sendDataPromo(parsed)
    return res

def LoadValorizacion(df):
    new_header = map(lambda x,y: str(x) if str(y)=='nan' else str(x)+'|'+ str(y).upper(), pd.Series(list(df.columns)), pd.Series(list(df.iloc[0])))
    data = df[1:]
    data.columns = new_header
    data = data.melt(id_vars = ["CLASIFICACION", "NART", "DESCRIPCION"], var_name = "FECHA_VALUE", value_name = "QUANTITY")
    split = data["FECHA_VALUE"].str.split("|", n = 1, expand = True)
    data["FECHA"] = split[0]
    data["VALUE"] = split[1]
    data.drop(columns = ["FECHA_VALUE"], inplace = True)
    data["FECHA2"] = pd.to_datetime(data["FECHA"], format='%Y-%m-%d')
    data["YEAR"] = data["FECHA2"].dt.year
    data["MONTH"] = data["FECHA2"].dt.month
    data["KEY"] = datetime.now().strftime("%Y%m")
    d1 = data[["KEY","CLASIFICACION", "NART", "DESCRIPCION", "YEAR", "MONTH", "VALUE", "QUANTITY"]]
    d1 = d1[d1['QUANTITY'].notna()]
    d1.columns = ["id","clasificacion","nart","descripcion","year","month","value","cantidad"]
    result = d1.to_json(orient="records")
    parsed = json.loads(result)
    #print(json.dumps(parsed, indent=4))
    res = sendDataValorizacion(parsed)
    return res