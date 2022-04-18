import sys

from src.api.hasura_queries.base_query import queryHasura
from src.api.services.data_revision import getSizebyColumnName
from src.api.services.global_variables import AREA_BY_TABLE

def requestIDbyPeriod(period):
    try:
        query = """
        query MyQuery($id: String) {
            Maestro_baseline(distinct_on: id, where: {id: {_iregex: $id}}) {
                id
            }
            Maestro_launch(distinct_on: id, where: {id: {_iregex: $id}}) {
                id
            }
            Maestro_promo(distinct_on: id, where: {id: {_iregex: $id}}) {
                id
            }
            Maestro_valorizacion(distinct_on: id, where: {id: {_iregex: $id}}) {
                id
            }
            Maestro_Shopper(distinct_on: id, where: {id: {_iregex: $id}}) {
                id
            }
        }
        """
        res_insert = queryHasura(query, {"id" : period[:3]})
        result = []    
        for file in res_insert["data"]:
            data = []
            file_data = []
            file_id = ""
            if len(res_insert["data"][file]) > 0:
                for mes in res_insert["data"][file]:
                    if mes["id"] == period:
                        q = """ 
                        query MyQuery($id: String = "", $area_id: Int) {
                        view_info_inputs_by_id(where: {id: {_eq: $id}, area_id: {_eq: $area_id}}) {
                            file_id
                            name
                            user
                            date
                        }
                        }
                        """
                        res = queryHasura(q, {'id': period, 'area_id': AREA_BY_TABLE[file]["area_id"]})
                        if res.get('data', []):
                            file_data = res["data"]["view_info_inputs_by_id"]
                            file_id = period
                    if mes["id"] <= period:
                        data.append({"file_id" : mes["id"], "mes": mes["id"][0:4]+"-"+mes["id"][4:]})
                result.append({ "area_id" : AREA_BY_TABLE[file]["area_id"], "area_name" : AREA_BY_TABLE[file]["area_name"], "file_id" : file_id, "data" : data, "file_data": file_data })
            else:
                result.append({ "area_id" : AREA_BY_TABLE[file]["area_id"], "area_name" : AREA_BY_TABLE[file]["area_name"], "file_id" : "", "data": []})
        return result
    except:
        print("error on requestIDbyPeriod")
        print(sys.exc_info()[1])
        return ""

def request_file_data(area_id, file_id):
    try:
        q = """ 
        query MyQuery($id: String = "", $area_id: Int) {
            view_info_inputs_by_id(where: {id: {_eq: $id}, area_id: {_eq: $area_id}}) {
                file_id
                name
                user
                date
            }
        }
        """
        res = queryHasura(q, {'id': str(file_id), 'area_id': int(area_id)})
        return res["data"]["view_info_inputs_by_id"]
    except:
        print('Error request_file_data :', sys.exc_info())
        return []

def delete_data_by_file_id(area_id, file_id):
    try:
        print(1)
        tbl_name = ""
        res_tbl = ""
        if area_id == 1:
            tbl_name = "baseline"
            res_tbl = "delete_Maestro_baseline"
        elif area_id == 2:
            tbl_name = "launch"
            res_tbl = "delete_Maestro_launch"
        elif area_id == 3:
            tbl_name = "promo"
            res_tbl = "delete_Maestro_promo"
        elif area_id == 4:
            tbl_name = "valorizacion"
            res_tbl = "delete_Maestro_valorizacion"
        elif area_id == 5:
            tbl_name = "Shopper"
            res_tbl = "delete_Maestro_Shopper"
        if area_id not in [1,2,3,4,5]:
            return { 'error': 'no se encuentra tabla correspondiente con el area_id enviada' }, 400
        q = """
        mutation MyMutation($_eq: numeric = "") {
            delete_Maestro_"""+tbl_name+"""(where: {file_id: {_eq: $_eq}}) {
                returning {
                    id
                    file_id
                }
            }
        }
        """
        res = queryHasura(q, {'_eq': file_id})
        tbl_name = f"delete_Maestro_{tbl_name}"
        result = res["data"][res_tbl]["returning"]
        q = """ 
        query MyQuery($id: String, $area_id: Int) {
            search_info_inputs_by_id(args: {id: $id, area: $area_id}) {
                file_id
                name
                date
                user
            }
        }
        """
        res_info = queryHasura(q, {'id': file_id, 'area_id': area_id})
        file_data = res_info["data"]["search_info_inputs_by_id"]
        if file_id == "" or file_data == []:
            return { 'file_id': "", "file_data": [] }
        else:
            return { 'file_id': file_id, "file_data": file_data}
    except:
        print('Error delete_data_by_file_id :', sys.exc_info())
        return { 'error': 'error haciendo la peticion de eliminacion de data' }, 400

def updateInputTable(table_name, rows):
    try:
        if table_name == 'BASELINE':
            rows_affected = 0
            for row in rows:
                query = """ 
                mutation MyMutation($id:String, $nart: String, $year: numeric, $month: numeric, $cantidad: numeric) {
                update_Maestro_baseline(where: {id: {_eq: $id}, nart: {_eq: $nart}, year: {_eq: $year}, month: {_eq: $month}}, _set: {cantidad: $cantidad}) {affected_rows}}
                """
                res = queryHasura(query, { 'id': row['id'], 'nart': row['nart'], 'year': row['year'], 'month': row['month'], 'cantidad': row['cantidad']})
                rows_affected += res['data']['update_Maestro_baseline']['affected_rows']
            return rows_affected
        elif table_name == 'LAUNCH':
            rows_affected = 0
            for row in rows:
                query = """ 
                mutation MyMutation($id:String, $nart: String, $year: numeric, $month: numeric, $cantidad: numeric) {
                update_Maestro_launch(where: {id: {_eq: $id}, nart: {_eq: $nart}, year: {_eq: $year}, month: {_eq: $month}}, _set: {cantidad: $cantidad}) {affected_rows}} 
                """
                res = queryHasura(query, { 'id': row['id'], 'nart': row['nart'], 'year': row['year'], 'month': row['month'], 'cantidad': row['cantidad']})
                rows_affected += res['data']['update_Maestro_launch']['affected_rows']
            return rows_affected
        elif table_name == 'PROMO':
            rows_affected = 0
            for row in rows:
                query = """ 
                mutation MyMutation($id: String, $nart: String = "", $year: numeric = "",$month: numeric = "", $cantidad: numeric = "") {
                update_Maestro_promo(where: {id: {_eq: $id}, nart: {_eq: $nart}, year: {_eq: $year}, month: {_eq: $month}, cantidad: {_eq: $cantidad}}) {affected_rows}}
                """
                res = queryHasura(query, { 'id': row['id'], 'nart': row['nart'], 'year': row['year'], 'month': row['month'], 'cantidad': row['cantidad']})
                rows_affected += res['data']['update_Maestro_promo']['affected_rows']
            return rows_affected
        elif table_name == 'SHOPPER':
            rows_affected = 0
            for row in rows:
                query = """ 
                mutation MyMutation($id: String = "", $nart: String = "", $year: numeric = "", $month: numeric = "", $cantidad: numeric = "") {
                update_Maestro_Shopper(where: {id: {_eq: $id}, nart: {_eq: $nart}, year: {_eq: $year}, month: {_eq: $month}, cantidad: {_eq: $cantidad}}) {affected_rows}}
                """
                res = queryHasura(query, { 'id': row['id'], 'nart': row['nart'], 'year': row['year'], 'month': row['month'], 'cantidad': row['cantidad']})
                rows_affected += res['data']['update_Maestro_Shopper']['affected_rows']
            return rows_affected
    except SyntaxError as err:
        print(err)
        return 0

def addRow(row):
    try:
        table_name = row['clasificacion']
        if table_name == 'BASELINE':
            query = """mutation MyMutation($objects: [Maestro_baseline_insert_input!]!) { insert_Maestro_baseline(objects: $objects) {affected_rows}} """
            res = queryHasura(query, { 'objects' : row })
            error = res.get('errors', '')
            if error == '':
                return res['data']['insert_Maestro_baseline']['affected_rows']
            else:
                if error[0]['extensions']['code'] == 'constraint-violation':
                    return { 'error': 'la fila ingresada ya existe' }
                else:
                    return 0
        elif table_name == 'LAUNCH':
            query = """mutation MyMutation($objects: [Maestro_launch_insert_input!]!) {insert_Maestro_launch(objects: $objects) {affected_rows }}"""
            res = queryHasura(query, { 'objects' : row })
            error = res.get('errors', '')
            if error == '':
                return res['data']['insert_Maestro_launch']['affected_rows']
            else:
                if error[0]['extensions']['code'] == 'constraint-violation':
                    return { 'error': 'la fila ingresada ya existe' }
                else:
                    return 0   
        elif table_name == 'PROMO':
            query = """mutation MyMutation($objects: [Maestro_promo_insert_input!]!) {insert_Maestro_promo(objects: $objects) {affected_rows}}"""
            res = queryHasura(query, { 'objects' : row })
            error = res.get('errors', '')
            if error == '':
                return res['data']['insert_Maestro_promo']['affected_rows']
            else:
                if error[0]['extensions']['code'] == 'constraint-violation':
                    return { 'error': 'la fila ingresada ya existe' }
                else:
                    return 0
        elif table_name == 'SHOPPER':
            query = """mutation MyMutation($objects: [Maestro_Shopper_insert_input!]!) {insert_Maestro_Shopper(objects: $objects) {affected_rows}}"""
            res = queryHasura(query, { 'objects' : row })
            error = res.get('errors', '')
            if error == '':
                return res['data']['insert_Maestro_Shopper']['affected_rows']
            else:
                if error[0]['extensions']['code'] == 'constraint-violation':
                    return { 'error': 'la fila ingresada ya existe' }
                else:
                    return 0   
        elif table_name == 'VALORIZACION':
            query = """mutation MyMutation($objects: [Maestro_valorizacion_insert_input!]!) {insert_Maestro_valorizacion(objects: $objects) {affected_rows}}"""
            res = queryHasura(query, { 'objects' : row })
            error = res.get('errors', '')
            if error == '':
                return res['data']['insert_Maestro_valorizacion']['affected_rows']
            else:
                if error[0]['extensions']['code'] == 'constraint-violation':
                    return { 'error': 'la fila ingresada ya existe' }
                else:
                    return 0
    except SyntaxError as err:
        print(f' Error addRow {err}')
        return 0

def requestDataBaseline(id):
    try:
        query = """
        query MyQuery($id: String) {
            Maestro_baseline(where: {id: {_eq: $id}}) {
                id
                clasificacion
                nart
                descripcion
                year
                month
                cantidad
            }
        }
        """
        res_select = queryHasura(query, {"id" : id })
        if len(res_select["data"]["Maestro_baseline"]) < 1:
            return "No existen datos para los parametros igresados"
        size_list = [{'name':'clasificacion','size':120}, {'name':'descripcion','size':500},{'name':'nart','size':200}]
        colum_list = [{'name': i,'prop': i,'autoSize': True,'sortable': True} if i not in [x['name'] for x in size_list ] else {'name':i,'prop':i,'size':getSizebyColumnName(size_list,i),'autoSize':True,'sortable':True} for i in res_select["data"]["Maestro_baseline"][0].keys()]
        result = {
            "columns" : colum_list,
            "rows" : res_select["data"]["Maestro_baseline"]
        }
        return result
    except:
        print('error requestDataBaseline :', sys.exc_info())
        return ""

def sendDataBaseline(data):
    try:
        query = """
        mutation MyMutation($objects: [Maestro_baseline_insert_input!]!) {
            insert_Maestro_baseline(objects: $objects, on_conflict: {constraint: Maestro_baseline_pkey1, update_columns: cantidad}) {
                returning {
                    id
                }
            }
        }
        """
        res_insert = queryHasura(query, {"objects" : data})
        result = { "file_id" : res_insert["data"]["insert_Maestro_baseline"]["returning"][0]["id"], "area_name" : AREA_BY_TABLE["Maestro_baseline"]["area_name"]}
        return result
    except:
        return ""

def deleteDataBaseline(id):
    try:
        query = """
        mutation MyMutation($id: String) {
            delete_Maestro_baseline(where: {id: {_eq: $id}}) {
                affected_rows
            }
        }
        """
        res_delete = queryHasura(query, {"id" : id })
        result = {
            "deleted_rows" : res_delete["data"]["delete_Maestro_baseline"]["affected_rows"]
        }
        return result
    except SystemError as err:
        print(err)
        return ""

def requestDataLaunch(id):
    try:
        query = """
        query MyQuery($id: String) {
            Maestro_launch(where: {id: {_eq: $id}}) {
                id
                clasificacion
                canal
                nart
                descripcion
                year
                month
                cantidad
            }
        }
        """
        res_select = queryHasura(query, {"id" : id })
        if len(res_select["data"]["Maestro_launch"]) < 1:
            return "No existen datos para los parametros igresados"
        size_list = [{'name':'clasificacion','size':120} ,{'name':'canal','size':100},{'name':'descripcion','size':500},{'name':'nart','size':200}]
        colum_list = [{'name': i,'prop': i,'autoSize': True,'sortable': True} if i not in [x['name'] for x in size_list ] else {'name':i,'prop':i,'size':getSizebyColumnName(size_list,i),'autoSize':True,'sortable':True} for i in res_select["data"]["Maestro_launch"][0].keys()]
        result = {
            "columns" : colum_list,
            "rows" : res_select["data"]["Maestro_launch"]
        }
        return result
    except SystemError as err:
        print(err)
        return ""

def sendDataLaunch(data):
    query = """
    mutation MyMutation($objects: [Maestro_launch_insert_input!] = {}) {
        insert_Maestro_launch(objects: $objects, on_conflict: {constraint: Maestro_launch_pkey, update_columns: cantidad}) {
            returning {
                id
            }
        }
    }
    """
    res_insert = queryHasura(query, {"objects" : data})
    result = { "file_id" : res_insert["data"]["insert_Maestro_launch"]["returning"][0]["id"], "area_name" : AREA_BY_TABLE["Maestro_launch"]["area_name"]}
    return result

def deleteDataLaunch(id):
    try:
        query = """
        mutation MyMutation($id: String) {
            delete_Maestro_launch(where: {id: {_eq: $id}}) {
                affected_rows
            }
        }
        """
        res_delete = queryHasura(query, {"id" : id })
        result = {
            "deleted_rows" : res_delete["data"]["delete_Maestro_launch"]["affected_rows"]
        }
        return result
    except SystemError as err:
        print(err)
        return ""

def requestDataPromo(id):
    query = """
    query MyQuery($id: String) {
        Maestro_promo(where: {id: {_eq: $id}}) {
            id
            clasificacion
            tipo_promo
            canal
            application_form
            nart
            descripcion
            year
            month
            cantidad
        }
    }
    """
    res_select = queryHasura(query, {"id" : id })
    if len(res_select["data"]["Maestro_promo"]) < 1:
        return "No existen datos para los parametros igresados"
    size_list = [{'name':'clasificacion','size':120}, {'name':'canal','size':100},{'name':'application_form','size':120}, {'name':'descripcion','size':500},{'name':'nart','size':200}]
    colum_list = [{'name': i,'prop': i,'autoSize': True,'sortable': True} if i not in [x['name'] for x in size_list ] else {'name':i,'prop':i,'size':getSizebyColumnName(size_list,i),'autoSize':True,'sortable':True} for i in res_select["data"]["Maestro_promo"][0].keys()]
    result = {
        "columns" : colum_list,
        "rows" : res_select["data"]["Maestro_promo"]
    }
    return result
    
def sendDataPromo(data):
    query = """
    mutation MyMutation($objects: [Maestro_promo_insert_input!] = {}) {
        insert_Maestro_promo(objects: $objects, on_conflict: {constraint: Maestro_promo_pkey, update_columns: cantidad}) {
            returning {
                id
            }
        }
    }
    """
    res_insert = queryHasura(query, {"objects" : data})
    result = { "file_id" : res_insert["data"]["insert_Maestro_promo"]["returning"][0]["id"], "area_name" : AREA_BY_TABLE["Maestro_promo"]["area_name"]}
    return result

def deleteDataPromo(id):
    try:
        query = """
        mutation MyMutation($id: String) {
            delete_Maestro_promo(where: {id: {_eq: $id}}) {
                affected_rows
            }
        }
        """
        res_delete = queryHasura(query, {"id" : id })
        result = {
            "deleted_rows" : res_delete["data"]["delete_Maestro_promo"]["affected_rows"]
        }
        return result
    except SystemError as err:
        print(err)
        return ""

def requestDataValorizacion(id):
    query = """
    query MyQuery($id: String) {
        Maestro_valorizacion(where: {id: {_eq: $id}}) {
            id
            brand_category
            nart
            descripcion
            year
            month
            value
            cantidad
        }
    }
    """
    res_select = queryHasura(query, {"id" : id })
    if len(res_select["data"]["Maestro_valorizacion"]) < 1:
        return "No existen datos para los parametros igresados"

    size_list = [{'name':'brand_category','size':120} , {'name':'descripcion','size':500},{'name':'nart','size':200}]
    colum_list = [{'name': i,'prop': i,'autoSize': True,'sortable': True} if i not in [x['name'] for x in size_list ] else {'name':i,'prop':i,'size':getSizebyColumnName(size_list,i),'autoSize':True,'sortable':True} for i in res_select["data"]["Maestro_valorizacion"][0].keys()]
    result = {
        "columns" : colum_list,
        "rows" : res_select["data"]["Maestro_valorizacion"]
    }
    return result
    
def sendDataValorizacion(data):
    query = """
    mutation MyMutation($objects: [Maestro_valorizacion_insert_input!] = {}) {
        insert_Maestro_valorizacion(objects: $objects, on_conflict: {constraint: Maestro_valorizacion_pkey, update_columns: [cantidad, file_id]}) {
            returning {
                id
            }
        }
    }
    """
    res_insert = queryHasura(query, {"objects" : data})
    result = { "file_id" : res_insert["data"]["insert_Maestro_valorizacion"]["returning"][0]["id"], "area_name" : AREA_BY_TABLE["Maestro_valorizacion"]["area_name"]}
    return result

def deleteDataValorizacion(id):
    try:
        query = """
        mutation MyMutation($id: String){
            delete_Maestro_valorizacion(where: {id: {_eq: $id}}) {
                affected_rows
            }
        }
        """
        res_delete = queryHasura(query, {"id" : id })
        result = {
            "deleted_rows" : res_delete["data"]["delete_Maestro_valorizacion"]["affected_rows"]
        }
        return result
    except SystemError as err:
        print(err)
        return ""

def requestDataShoppers(id):
    query = """
    query MyQuery($id: String) {
        Maestro_Shopper(where: {id: {_eq: $id}}) {
            id
            clasificacion
            tipo_promo
            canal
            application_form
            nart
            descripcion
            year
            month
            cantidad
        }
    }
    """
    res_select = queryHasura(query, {"id" : id })

    if len(res_select["data"]["Maestro_Shopper"]) < 1:
        return "No existen datos para los parametros igresados"

    size_list = [{'name':'clasificacion','size':120},{'name':'nart','size':170},{'name':'descripcion','size':500}]
    colum_list = [{'name': i,'prop': i,'autoSize': True,'sortable': True} if i not in [x['name'] for x in size_list ] else {'name':i,'prop':i,'size':getSizebyColumnName(size_list,i),'autoSize':True,'sortable':True} for i in res_select["data"]["Maestro_Shopper"][0].keys()]
    result = {
        "columns" : colum_list,
        "rows" : res_select["data"]["Maestro_Shopper"]
    }
    return result

def sendDataShoppers(data):
    try:
        query = """
        mutation MyMutation($objects: [Maestro_Shopper_insert_input!] = {}) {
            insert_Maestro_Shopper(objects: $objects, on_conflict: {constraint: Maestro_Shoppers_pkey, update_columns: cantidad}) {
                returning {
                id
                }
            }
        }
        """
        res_insert = queryHasura(query, {"objects" : data})
        result = { "file_id" : res_insert["data"]["insert_Maestro_Shopper"]["returning"][0]["id"], "area_name" : AREA_BY_TABLE["Maestro_Shopper"]["area_name"]}
        return result
    except:
        print('error sendDataShoppers :', sys.exc_info())
        return ""

def deleteDataShoppers(id):
    try:
        query = """
        mutation MyMutation($id: String) {
            delete_Maestro_Shopper(where: {id: {_eq: $id}}) {
                affected_rows
            }
        }
        """
        res_delete = queryHasura(query, {"id" : id })
        result = {
            "deleted_rows" : res_delete["data"]["delete_Maestro_Shopper"]["affected_rows"]
        }
        return result
    except SystemError as err:
        print(err)
        return ""

def sendDataForecast(data):
    query = """
    mutation MyMutation($objects: [Forecast_insert_input!] = {}) {
    insert_Forecast(objects: $objects, on_conflict: {constraint: Forecast_pkey, update_columns: [r_o, mso, net_sales]}) {
        affected_rows
    }
    }
    """
    res_insert = queryHasura(query, {"objects" : data})
    result = { "file_id" : res_insert["data"]["insert_Forecast"]["affected_rows"], "area_name" : "Forecast" }
    return result