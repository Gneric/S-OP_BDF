
import sys
from src.api.hasura_queries.base_query import queryHasura


def audit_inputs(row):
    try:
        q = """
        mutation MyMutation($objects: [auditorias_auditoria_input_insert_input!] = {}) {
        insert_auditorias_auditoria_input(objects: $objects) {
            affected_rows
        }
        }
        """
        res_audit = queryHasura(q, {"objects": row})
        return res_audit['data']['insert_auditorias_auditoria_input']['affected_rows']
    except:
        print('Error audit_inputs :', sys.exc_info())
        return ""

def register_file(row):
    try:
        q = """
        mutation MyMutation($objects: [file_manager_insert_input!] = {}) {
            insert_file_manager(objects: $objects) {
                affected_rows
            }
        }
        """
        res = queryHasura(q, {"objects": [row]})
        return res['data']['insert_file_manager']['affected_rows']
    except:
        print('Error registrando file :', sys.exc_info())
        return ""