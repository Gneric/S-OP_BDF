import sys
from src.api.hasura_queries.base_query import queryHasura


def update_maestro_productos(data):
    try:
        q = """
        mutation MyMutation($objects: [Maestro_productos_insert_input!] = {}) {
            insert_Maestro_productos(objects: $objects, on_conflict: {constraint: Maestro_productos_pkey, update_columns: [ApplicationForm, BG, SPGR, TIPO, Descripcion, BrandCategory, Portafolio, BPU, EAN, SPGR_historico]}) {
                affected_rows
            }
        }
        """
        res = queryHasura(q, {'objects': data})
        return res['data']['rowsaffected']
    except:
        print('error update_maestro_productos : ', sys.exc_info())
        return 0

def upload_data_maestro(data):
    try:
        q = """
        mutation MyMutation($objects: [Maestro_productos_insert_input!] = {}) {
            insert_Maestro_productos(objects: $objects, on_conflict: {constraint: Maestro_productos_pkey, update_columns: [ApplicationForm, BG, BPU, BrandCategory, Descripcion, EAN, Material, Portafolio, SPGR, TIPO, SPGR_historico]}) {
                affected_rows
            }
        }
        """
        res = queryHasura(q, {'objects': data})
        aff_rows = res["data"]["insert_Maestro_productos"]["affected_rows"]
        if aff_rows:
            return { 'result': 'ok' }
        else:
            return { 'error': 'error en la respuesta de actualizacion' }, 400
    except:
        print('error update_producto_maestro:', sys.exc_info())
        print('result :', res)
        return { 'error': 'error en la respuesta de actualizacion' }, 400

def request_data_maestro():
    try:
        q = """
        query MyQuery {
            Maestro_productos {
                BG
                Material
                SPGR
                TIPO
                Descripcion
                Portafolio
                BPU
                BrandCategory
                ApplicationForm
                EAN
                SPGR_historico
            }
        }
        """
        res = queryHasura(q)
        return res["data"]["Maestro_productos"]
    except:
        print('error request_data_maestro:', sys.exc_info())
        print('result :', res)
        return { 'error': 'error en la obtencion de datos maestro' }, 400

def request_maestro_categorias():
    try:
        q = """
        query MyQuery {
            Maestro_categorias {
                name
                category
            }
        }
        """
        res = queryHasura(q)
        return res["data"]["Maestro_categorias"]
    except:
        print('error request_upsert_maestro_categorias:', sys.exc_info())
        print('result :', res)
        return ""

def request_upsert_maestro_categorias(data):
    try:
        q = """
        mutation MyMutation($objects: [Maestro_categorias_insert_input!] = {}) {
        insert_Maestro_categorias(objects: $objects, on_conflict: {constraint: Maestro_categorias_pkey, update_columns: name}) {
            affected_rows
        }
        }
        """
        res = queryHasura(q, { 'objects': data })
        return res["data"]["insert_Maestro_categorias"]["affected_rows"]
    except:
        print('error request_upsert_maestro_categorias:', sys.exc_info())
        print('result :', res)
        return ""

def request_used_categories():
    try:
        q = """
        query MyQuery {
        Maestro_categorias {
            id
            name
            category
        }
        }
        """
        res = queryHasura(q)
        return res["data"]["Maestro_categorias"]
    except:
        print('error request_upsert_maestro_categorias:', sys.exc_info())
        print('result :', res)
        return ""


def request_delete_category_items(data):
    try:
        q = """
        mutation MyMutation($_in: [Int!]) {
        delete_Maestro_categorias(where: {id: {_in: $_in}}) {
            affected_rows
        }
        }
        """
        res = queryHasura(q, {'_in': data})
        return res["data"]["delete_Maestro_categorias"]["affected_rows"]
    except:
        print('error request_delete_category_items:', sys.exc_info())
        print('result :', res)
        return ""
