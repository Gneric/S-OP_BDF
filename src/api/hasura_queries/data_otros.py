import sys
from src.api.hasura_queries.base_query import queryHasura

def request_transito_nart(nart):
    try:
        q = """
        query MyQuery($parametro_nart: String = "") {
            function_get_transito_x_nart(args: {parametro_nart: $parametro_nart}) {
                idfecha
                nart
                fechaLlegada
                unidades
            }
        }
        """
        res = queryHasura(q, {'parametro_nart': nart})
        return res["data"]["function_get_transito_x_nart"]
    except:
        print('Error request_transito_nart', sys.exc_info())
        return []

def get_productos_otros():
    try:
        q = """
        query MyQuery {
            Nart_sin_clasificar {
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
        return res['data']['Nart_sin_clasificar']
    except:
        print('error get_productos_otros :', sys.exc_info())
        return []