from src.api.hasura_queries.base_query import queryHasura
import sys

def requestinfo_db_main(clasificacion, year, month, bpu, brand_category, application_form):
    try:
        variables = { "clasificacion": {"_eq": clasificacion}, "year": {"_eq": year}, "month": {"_eq": month}}
        if bpu:
            variables["bpu"]  = {"_eq": bpu}
        if brand_category:
            variables["brand_category"] = {"_eq": brand_category}
        if application_form:
            variables["application_form"] = {"_eq": application_form}
        query = """
        query MyQuery($variables: DB_Main_bool_exp = {}) {
            DB_Main(where: $variables) {
                id
                clasificacion
                bpu
                brand_category
                application_form
                year
                month
                promo_spgr
                units
                netsales
                ajuste_netsales
                comentario
                canal
            }
        }"""
        res_insert = queryHasura(query, {"variables": variables})
        data = res_insert["data"]["DB_Main"]
        result = { 'result': data }
        return result
    except:
        print(sys.exc_info())
        return 0

def request_id_db_main():
    try:
        query = """
        query MyQuery {
        DB_Main(distinct_on: id) {
            id
        }
        }

        """
        res_insert = queryHasura(query)
        data = res_insert["data"]["DB_Main"][0]["id"]
        return data
    except:
        print(sys.exc_info())
        return 0

def update_db_main_table(data):
    try:
        query = """
        mutation MyMutation($objects: [DB_Main_insert_input!] = {}) {
        insert_DB_Main(objects: $objects, on_conflict: {constraint: DB_Main_pkey, update_columns: [netsales, ajuste_netsales]}) {
            affected_rows
        }
        }
        """
        res = queryHasura(query, {'objects': data})
        print('(update_db_main_table) : ', res)
        return res
    except:
        print('error update_db_main_table :', sys.exc_info())
        print('result :', res)
        return 0

def request_data_last_id(id):
    try:
        if id:
            query = """
            query MyQuery($customWhere: json = "") {
                function_get_view_bd_main_canal_custom_id(args: {customWhere: $customWhere}) {
                    id
                    clasificacion
                    canal
                    bpu
                    brand_category
                    application_form
                    promo_spgr
                    year
                    month
                    units
                    netsales
                    ajuste_netsales
                    comentario
                }
            }
            """
            res = queryHasura(query, { 'customWhere': {"id":{"_eq": id }} })
            return res["data"]["function_get_view_bd_main_canal_custom_id"]
        else:
            query = """
            query MyQuery {
                view_db_main_last_id{
                    id
                    clasificacion
                    canal
                    bpu
                    brand_category
                    application_form
                    promo_spgr
                    year
                    month
                    units
                    netsales
                    ajuste_netsales
                    comentario
                }
            }
            """
            res = queryHasura(query)
            return res["data"]["view_db_main_last_id"]
    except:
        print(sys.exc_info())
        print('request_data_last_id', res)
        return []

def delete_db_main_id():
    try:
        query = """
        mutation MyMutation {
            delete_DB_Main(where: {}) {
                affected_rows
            }
        }
        """
        res = queryHasura(query)
        return res["data"]["delete_DB_Main"]["affected_rows"]
    except:
        print(sys.exc_info())
        return []

def insert_data_db_main(data):
    try:
        query = """
        mutation MyMutation($data: [DB_Main_insert_input!]!) {
            insert_DB_Main(objects: $data, on_conflict: {constraint: DB_Main_pkey, update_columns: [units, netsales, ajuste_netsales, comentario]}) {
                    affected_rows
            }
        }
        """
        res = queryHasura(query, {'data': data })
        return res["data"]["insert_DB_Main"]["affected_rows"]
    except:
        print(sys.exc_info())
        print('error insert_data_db_main', res)
        return 0

def request_data_comparacion_sop():
    try:
        q = """
        query MyQuery {
            Comparacion_SOP_M1_FC_view {
                id
                application_form
                brand_category
                bpu
                dif_abs_financial
                dif_abs_lastyear
                dif_abs_m1
                financial
                lastsop_eur
                lastsop_pen
                lastyear
                sop_m1
                var_porc_financial
                var_porc_lastyear
                var_porc_m1
            }
        }
        """
        res = queryHasura(q)
        return res['data']['Comparacion_SOP_M1_FC_view']
    except:
        print('Error request_data_comparacion_sop ', sys.exc_info())
        return []

def delete_data_comparacion_sop():
    try:
        q ="""mutation MyMutation {
            delete_Comparacion_SOP_M1_FC(where: {}) {
                affected_rows
            }
        }
        """
        res = queryHasura(q)
        return 'ok'
    except:
        print('Error delete_data_comparacion_sop', sys.exc_info())
        return ""

def request_upsert_comparacion_sop(data):
    try:
        for row in data:
            row.update({ 'comment': '' })
        q = """
        mutation MyMutation($objects: [Comparacion_SOP_M1_FC_insert_input!] = {}) {
            insert_Comparacion_SOP_M1_FC(objects: $objects, on_conflict: {constraint: Comparacion_SOP_M1_FC_pkey1, 
                update_columns: [comment, dif_abs_financial, dif_abs_lastyear, dif_abs_m1, financial, lastsop_eur, lastsop_pen, lastyear, sop_m1, var_porc_financial, var_porc_lastyear, var_porc_m1]}) {
                affected_rows
            }
        }
        """
        res = queryHasura(q, { 'objects': data })
        if res:
            return res['data']['insert_Comparacion_SOP_M1_FC']['affected_rows']
        else:
            return 0
    except:
        print('Error request_upsert_comparacion_sop ', sys.exc_info())
        return 0

def request_update_comparacion_sop(data):
    try:
        q = """
        mutation MyMutation($objects: [Comparacion_SOP_M1_FC_insert_input!] = {}) {
            insert_Comparacion_SOP_M1_FC(objects: $objects, on_conflict: {constraint: Comparacion_SOP_M1_FC_pkey1, 
                update_columns: [comment, dif_abs_financial, dif_abs_lastyear, dif_abs_m1, financial, lastsop_eur, lastsop_pen, lastyear, sop_m1, var_porc_financial, var_porc_lastyear, var_porc_m1]}) {
                affected_rows
            }
        }
        """
        res = queryHasura(q, { 'objects': data })
        if res:
            return { 'result': 'ok' }
        else:
            return { 'error': 'error en la respuesta de actualizacion' }, 400
    except:
        print('Error request_upsert_comparacion_sop ', sys.exc_info())
        return { 'error': 'error en la respuesta de actualizacion' }, 400

def request_alldata_db_main(id):
    try:
        query = """
        query MyQuery($customWhere: json) {
            function_get_database(args: {customWhere: $customWhere}) {
                id
                clasificacion
                canal
                bpu
                brand_category
                application_form
                nart
                spgr
                descripcion
                year
                month
                units
                netsales
            }
        }
        """
        res = queryHasura(query, { 'customWhere': {"id":[id]}})
        data = res["data"]["function_get_database"]
        return data
    except:
        print(sys.exc_info())
        print(res)
        return []

def request_data_db_main():
    try:
        q = """
        query MyQuery {
        DB_Main {
            id
            month
            netsales
            promo_spgr
            units
            year
            comentario
            clasificacion
            canal
            brand_category
            bpu
            application_form
            ajuste_netsales
        }
        }
        """
        res = queryHasura(q)
        return res["data"]["DB_Main"]
    except:
        print('Error request_data_db_main', res)
        print(sys.exc_info())
        return []

def backup_db_main(data):
    try:
        query = """
        mutation MyMutation($data: [Cierre_mes_sop_insert_input!] = {}) {
            insert_Cierre_mes_sop(objects: $data, on_conflict: {constraint: Cierre_mes_sop_pkey, update_columns: [units, netsales, ajuste_netsales, comentario]}) {
                affected_rows
            }
        }
        """
        res = queryHasura(query, {'data': data })
        return res["data"]["insert_Cierre_mes_sop"]["affected_rows"]
    except:
        print('Error backup_db_main', sys.exc_info())
        print(res)
        return 0

def request_curr_comparacion_sop():
    try:
        q = """
        query MyQuery {
            Comparacion_SOP_M1_FC {
                id
                application_form
                brand_category
                bpu
                dif_abs_financial
                dif_abs_lastyear
                dif_abs_m1
                financial
                lastsop_eur
                lastsop_pen
                lastyear
                sop_m1
                var_porc_financial
                var_porc_lastyear
                var_porc_m1
                comment
            }
        }
        """
        res = queryHasura(q)
        return res['data']['Comparacion_SOP_M1_FC']
    except:
        print('Error request_curr_comparacion_sop', sys.exc_info())
        return []

def backup_comparacion_sop(data):
    try:
        q = """
        mutation MyMutation($objects: [Cierre_Comparacion_SOP_M1_FC_insert_input!] = {}) {
            insert_Cierre_Comparacion_SOP_M1_FC(objects: $objects, on_conflict: {constraint: Cierre_Comparacion_SOP_M1_FC_pkey, update_columns: [lastsop_pen, lastsop_eur, lastyear, dif_abs_m1, dif_abs_lastyear, dif_abs_financial, var_porc_m1, var_porc_lastyear, var_porc_financial, financial, sop_m1, comment]}) {
                affected_rows
            }
        }
        """
        res = queryHasura(q, { 'objects': data })
        if res:
            return res['data']['insert_Cierre_Comparacion_SOP_M1_FC']['affected_rows']
        else:
            return 0
    except:
        print('Error backup_comparacion_sop ', sys.exc_info())
        print(res)
        return 0

def insert_multiple_rows(rows):
    try:
        q = """
        mutation MyMutation($objects: [DB_Main_insert_input!] = {}) {
        insert_DB_Main(objects: $objects, on_conflict: {constraint: DB_Main_pkey, update_columns: [units, netsales, ajuste_netsales, comentario]}) {
            affected_rows
        }
        }
        """
        res = queryHasura(q, {'objects' : rows})
        return res["data"]["insert_DB_Main"]["affected_rows"]
    except:
        print('error insert_multiple_rows :', sys.exc_info())
        print('result :', res)
        return ""

