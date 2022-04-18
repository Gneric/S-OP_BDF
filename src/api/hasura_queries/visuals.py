import sys
from datetime import datetime, timedelta

from src.api.hasura_queries.base_query import queryHasura
from src.api.services.data_revision import getSizebyColumnName

def db_last_id():
    try:
        query = """
        query BD_LastID {
            rows: BD_LastID(order_by: {month: asc, year: asc}, where: {}) {
                id
                clasificacion
                BPU
                nart
                nartdesc
                SPGR
                spgrdesc
                year
                month
                BrandCategory
                ApplicationForm
                units
                netsales
            }
        }
        """
        res = queryHasura(query)
        size_list = [
            {'name':'id','size':120},{'name':'clasificacion','size':200},{'name':'BPU','size':200},{'name':'nart','size':200},{'name':'nartdesc','size':500},{'name':'SPGR','size':200},{'name':'spgrdesc','size':500},
            {'name':'year','size':120},{'name':'month','size':120},{'name':'BrandCategory','size':200},{'name':'ApplicationForm','size':200},{'name':'units','size':200},{'name':'netsales','size':200}
        ]
        colum_list = []
        for col in res["data"]["rows"][0].keys():
            if col == 'units':
                colum_list.append({'name':col,'prop':col,'size':getSizebyColumnName(size_list,col),'autoSize':True,'sortable':True,'readonly':False})
            elif col not in [x['name'] for x in size_list]:
                colum_list.append({'name': col,'prop': col,'autoSize':True,'sortable':True,'readonly':True})
            else:
                colum_list.append({'name':col,'prop':col,'size':getSizebyColumnName(size_list,col),'autoSize':True,'sortable':True,'readonly':True})
        result = {"columns" : colum_list, "rows" : res["data"]["rows"]}
        return result
    except SystemError as err:
        print(err)
        return ""

def requestVisualBD():
    try:
        query = """
        query BD_syop {
            rows: BD_SOP(order_by: {month: asc, year: asc}, where: {}) {
            id
            clasificacion
            BPU
            nart
            nartdesc
            SPGR
            spgrdesc
            year
            month
            BrandCategory
            ApplicationForm
            units
            netsales   
            }
        }
        """
        res = queryHasura(query)
        columns = [{"name": "id","prop": "id","size": 120},{"name": "clasificacion","prop": "clasificacion","size": 200},{"name": "BPU","prop": "BPU","size": 200},{"name": "nart","prop": "nart","size": 200},{"name": "nartdesc","prop": "nartdesc","size": 500},
                   {"name": "SPGR","prop": "SPGR","size": 200},{"name": "spgrdesc","prop": "spgrdesc","size": 500},{"name": "year","prop": "year","size": 120},{"name": "month","prop": "month","size": 120},{"name": "BrandCategory","prop": "BrandCategory","size": 200},
                   {"name": "ApplicationForm","prop": "ApplicationForm","size": 200},{"name": "units","prop": "units","size": 200},{"name": "netsales","prop": "netsales","size": 200}]
        result = {
            "columns" : columns,
            "rows" : res["data"]["rows"]
        }
        return result
    except SystemError as err:
        print(err)
        return ""

def requestPrepareSummary(filters):
    try:
        query = """
        query BD_Prepare_Summary($customWhere: json = "") {
            function_get_prepare_summary(args: {customWhere: $customWhere}) {
                id
                input
                BPU
                nart
                year
                mes
                units
                netsales
            }
        }
        """
        res = queryHasura(query, { 'customWhere': filters })
        result = {"rows" : res["data"]["function_get_prepare_summary"]}
        return result
    except:
        print('Error requestPrepareSummary :',res)
        return ""


def demand_simulation_units():
    try:
        query = """
        query unitsxBPU {
        rows: BD_unitsxBPUView {
            year
            BPU
            month
            totmesxbpu
            totq1xbpu
            totq2xbpu
            totq3xbpu
            totq4xbpu
            totanoxbpu
            totano
        }
        }
        """
        res = queryHasura(query)
        size_list = [{'name':'year','size':150},{'name':'BPU','size':250},{'name':'month','size':150},{'name':'totmesxbpu','size':150},{'name':'totq1xbpu','size':150},{'name':'totq2xbpu','size':150},{'name':'totq3xbpu','size':150},{'name':'totq4xbpu','size':150},{'name':'totanoxbpu','size':150},{'name':'totano','size':150}]
        colum_list = [{'name': i,'prop': i,'autoSize': True,'sortable': True} if i not in [x['name'] for x in size_list ] else {'name':i,'prop':i,'size':getSizebyColumnName(size_list,i),'autoSize':True,'sortable':True} for i in res["data"]["rows"][0].keys()]
        result = {"columns" : colum_list, "rows" : res["data"]["rows"]}
        return result
    except SystemError as err:
        print(err)
        return ""


def demand_simulation_netsales():
    try:
        query = """
        query unitsxBPU {
        rows: BD_netsalesxBPUView {
            year
            BPU
            month
            totmesxbpu
            totq1xbpu
            totq2xbpu
            totq3xbpu
            totq4xbpu
            totanoxbpu
            totano
        }
        }
        """
        res = queryHasura(query)
        size_list = [{'name':'year','size':150},{'name':'BPU','size':250},{'name':'month','size':150},{'name':'totmesxbpu','size':150},{'name':'totq1xbpu','size':150},{'name':'totq2xbpu','size':150},{'name':'totq3xbpu','size':150},{'name':'totq4xbpu','size':150},{'name':'totanoxbpu','size':150},{'name':'totano','size':150}]
        colum_list = [{'name': i,'prop': i,'autoSize': True,'sortable': True} if i not in [x['name'] for x in size_list ] else {'name':i,'prop':i,'size':getSizebyColumnName(size_list,i),'autoSize':True,'sortable':True} for i in res["data"]["rows"][0].keys()]
        result = {"columns" : colum_list, "rows" : res["data"]["rows"]}
        return result
    except SystemError as err:
        print(err)
        return ""


def demand_simulation_db():
    try:
        query = """
        query DemandSimulation {
        rows: BD_DemandSimulation {    
            BPU
            year
            month
            quarter
            units
            netsales
        }
        }
        """
        res = queryHasura(query)
        size_list = [{'name':'BPU','size':250},{'name':'year','size':150},{'name':'month','size':150},{'name':'quarter','size':150},{'name':'units','size':150},{'name':'netsales','size':150}]
        colum_list = [{'name': i,'prop': i,'autoSize': True,'sortable': True} if i not in [x['name'] for x in size_list ] else {'name':i,'prop':i,'size':getSizebyColumnName(size_list,i),'autoSize':True,'sortable':True} for i in res["data"]["rows"][0].keys()]
        result = {"columns" : colum_list, "rows" : res["data"]["rows"]}
        return result
    except SystemError as err:
        print(err)
        return ""


def fc_simulation():
    try:
        query = """
        query FC_Simulation {
        rows: FC_Simulation {    
            clasificacion
            year
            enero
            febrero
            marzo
            abril
            mayo
            junio
            julio
            agosto
            septiembre
            octubre
            noviembre
            diciembre
        }
        }
        """
        res = queryHasura(query)
        size_list = [{'name':'clasificacion','size':200},{'name':'year','size':120},{'name':'enero','size':200},{'name':'febrero','size':200},{'name':'marzo','size':200},{'name':'abril','size':200},{'name':'mayo','size':200},{'name':'junio','size':200},{'name':'julio','size':200},{'name':'agosto','size':200},{'name':'septiembre','size':200},{'name':'octubre','size':200},{'name':'noviembre','size':200},{'name':'diciembre','size':200}]
        colum_list = [{'name': i,'prop': i,'autoSize': True,'sortable': True} if i not in [x['name'] for x in size_list ] else {'name':i,'prop':i,'size':getSizebyColumnName(size_list,i),'autoSize':True,'sortable':True} for i in res["data"]["rows"][0].keys()]
        result = {"columns" : colum_list, "rows" : res["data"]["rows"]}
        return result
    except SystemError as err:
        print(err)
        return ""

def graph_dataset():
    try:
        query = """
        query
        {
            Grafico_de_Barras_SellIn(order_by:{
                month: desc,
                year: desc
            }) {
                year,
                month,
                sum,
                clasificacion
            }
            Grafico_de_Tendencia_Sellout(order_by:{
                month: desc,
                year: desc
            }) {
                year,
                month,
                sum
            }
        }
        """
        res = queryHasura(query)
        datasets = []
        data = res["data"]
        datos_fijos = { 'REALES': {
                            '2019': {'backgroundColor':'#77aaff','stack':'Stack 0', 'label': "Sell in 2019"},
                            '2020':{'backgroundColor':"#3366ff",'stack':'Stack 1','label': "Sell in 2020"}, 
                            '2021':{'backgroundColor':"#3366ff",'stack':'Stack 2', 'label': "Sell in 2021"}},               
                        'BASELINE':{'backgroundColor': "red",'stack': 'Stack 2', 'label': "Baseline"},
                        'SHOPPER':{'backgroundColor': "green",'stack': 'Stack 2', 'label': "Shopper"},
                        'LAUNCH':{'backgroundColor': "yellow", 'stack': 'Stack 2', 'label': "Launch"},
                        'PROMO': {'backgroundColor': "purple", 'stack': 'Stack 2', 'label': "Promo"},
                        'SELLOUT':{'type': 'line', 'label': "Sell Out 2021"}    }
        sellin = data['Grafico_de_Barras_SellIn']
        sellout = sorted(data['Grafico_de_Tendencia_Sellout'], key=lambda i: i['month'])

        year = f'{datetime.now().strftime("%Y")}'
        month1 = f'{datetime.now().strftime("%m")}'
        month2 = f'{(datetime.now().replace(day=1) - timedelta(days=1)).strftime("%m")}'

        def fillMonths(array):
            month_range = [ i for i in range(12)]
            array_range = []
            for m in month_range:
                try:
                    if array[m]['month']-1 in month_range:
                        array_range.append(array[m]['sum'])
                except:
                        array_range.append(0)
            return array_range

        for input in datos_fijos:
            if input == 'REALES':
                years = list(set([ str(x['year']) for x in sellin if x['clasificacion'] == "REALES"]))
                for k in datos_fijos['REALES']:
                    dataset = datos_fijos['REALES'][k]
                    if k in years:
                        data = [ { 'sum':x['sum'], 'year':x['year'], 'month':x['month'] } for x in sorted(sellin, key=lambda i: i['month']) if x['clasificacion'] == "REALES" and x['year'] == int(k) ]
                        filled_data = fillMonths(data)
                        dataset['data'] = filled_data
                    else:
                        dataset['data'] = [0] * 12
                    datasets.append(dataset)
            else:
                if input == 'SELLOUT':
                    dataset = datos_fijos[input]
                    data = [ { 'sum':x['sum'], 'year':x['year'], 'month':x['month'] } for x in sellout if x['year'] == int(year)]
                    filled_data = fillMonths(data)
                    dataset['data'] = filled_data
                elif input != '':
                    data = sorted([{ 'sum': i['sum'], 'year':i['year'], 'month':i['month']} for i in sellin if i["clasificacion"] == input and i["year"] == int(year) and str(i["month"]) in [month1, month2]], key=lambda i: i['month'])
                    dataset = datos_fijos[input]
                    dataset['data'] = fillMonths(data)
                else:
                    dataset = datos_fijos[input]
                    dataset['data'] = [0] * 12
                datasets.append(dataset)
        return datasets
    except SystemError as err:
        print(err)
        return ""
    except:
        print(sys.exc_info())
        return ""

def request_cobertura(data):
    try:
        q = """
        query MyQuery($customWhere: json = "") {
            function_get_cobertura(args: {customWhere: $customWhere}, order_by: {BPU: asc}) {
                ApplicationForm
                BPU
                BrandCategory
                COBERTURA_FINAL
                COBERTURA_INICIAL
                DESCRIPCION
                FC
                IMPACTO
                NART
                NETSALES_IMPACT
                NSP
                SPGR
                STOCK
                TRANSITO
                id
            }
            function_get_cobertura_totales(args: {customWhere: $customWhere}) {
                NS_IMPACT
                SL_PROYECCION
                TOTALES_FC
                TOTALES_IMPACTO
                TOTALES_NETSALES_IMPACT
            }
            ids {
                id_nm
            }
        }
        """
        res = queryHasura(q, { 'customWhere': data })
        totales_fc = sum( row['TOTALES_FC'] for row in res['data']['function_get_cobertura_totales'] )
        totales_impacto = sum( row['TOTALES_IMPACTO'] for row in res['data']['function_get_cobertura_totales'] )
        totales_netsales_impact = sum( row['TOTALES_NETSALES_IMPACT'] for row in res['data']['function_get_cobertura_totales'] )
        ns_impact = sum( row['NS_IMPACT'] for row in res['data']['function_get_cobertura_totales'] )
        sl_proyeccion = sum( row['SL_PROYECCION'] for row in res['data']['function_get_cobertura_totales'] )
        totales = { 'TOTALES_FC' : totales_fc, 'TOTALES_IMPACTO': totales_impacto, 'TOTALES_NETSALES_IMPACT': totales_netsales_impact, 'NS_IMPACT': ns_impact, 'SL_PROYECCION': sl_proyeccion }
        mes = res["data"]["ids"][0]["id_nm"]
        return { 'data' : res['data']['function_get_cobertura'], 'totales' : totales, 'mes_en_curso': mes }
    except:
        print('error request_cobertura :', sys.exc_info())
        print('result :', res)
        return ""