from src.api.hasura_queries.base_query import queryHasura
import sys

def request_Maestro_productos():
    try:
        q = "query MyQuery {Maestro_productos(distinct_on: Material) { Material } } "
        res = queryHasura(q)
        p = [  x['Material'] for x in res['data']["Maestro_productos"] ]
        return p
    except:
        print('err request_Maestro_productos :', sys.exc_info())
        return []

def request_used_categories():
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
        category_names = [ row['name'].upper()+row['category'].upper() for row in res["data"]["Maestro_categorias"] ] 
        return category_names
    except:
        print('error request_used_categories:', sys.exc_info())
        print('result :', res)
        return ""

def request_clasificaciones_Maestro_productos():
    try:
        q = "query MyQuery { Maestro_categorias { category name } }"
        res = queryHasura(q)
        p = res['data']["Maestro_categorias"]
        return p
    except:
        print('err request_Maestro_productos :', sys.exc_info())
        return []