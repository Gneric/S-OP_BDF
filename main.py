from flask_jwt_extended.utils import create_refresh_token, decode_token
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token

from api.config import app_config

from api.routes.login import LogIn
from api.routes.welcome import Welcome
from api.routes.users import ChangePassword, ModifyUser, CreateUser, UserList
from api.routes.visuals import DemandSimulation, FCSimulation, GetBDHistorico, GetCobertura, GetVisualBD, GraphDataset, PrepareSummary, NetSalesxPBU, UnitsxBPU
from api.routes.permissions import GetPermissions, UpdatePermissions
from api.routes.timeline import GetInfoTimeline, SetInfoTimeline
from api.routes.data_endpoints.data_db_main import *
from api.routes.data_endpoints.data_inputs import *
from api.routes.data_endpoints.data_product_master import *
from api.routes.data_endpoints.data_otros import *

app = Flask(__name__)
app.config.from_object(app_config)
jwt = JWTManager(app)
CORS(app, expose_headers=["filename"], resources={r"*": {"origins": "*"}})
api = Api(app)

@app.route("/api/refresh", methods=["POST"])
def refresh():
    token = request.json.get('refreshToken', '')
    payload = decode_token(token)['sub']
    hasura_token = {}
    hasura_token["hasura_claims"] = decode_token(token)['hasura_claims']
    print(payload)
    if token == '':
      return { 'error': 'token no enviado' }, 401
    access_token = create_access_token(identity=payload, additional_claims=hasura_token)
    refresh_token = create_refresh_token(identity=payload, additional_claims=hasura_token)
    return { "accessToken" : access_token, "refreshToken": refresh_token }

@jwt.token_verification_failed_loader
def token_verification_failed_loader_callback(jwt_header, jwt_payload):
  response = { "error" : "token invalido" }, 401
  return response

@jwt.invalid_token_loader
def invalid_token_loader_callback(jwt_header):
  response = { "error" : "token invalido" }, 401
  return response

@jwt.unauthorized_loader
def unauthorized_loader_callback(jwt_header):
  response = { "error" : "token invalido" }, 401
  return response

@jwt.expired_token_loader
def expired_token_loader_callback(jwt_header, two):
  response = { "error" : "token expirado" }, 401
  return response

@jwt.needs_fresh_token_loader
def needs_fresh_token_loader(jwt_header):
  response = { "error" : "token invalido" }, 401
  return response

# root
api.add_resource(Welcome, '/api/')
# data
api.add_resource(GetData, '/api/get_excel_data')
api.add_resource(DeleteData, '/api/del_data')
api.add_resource(CloneData, '/api/clone_data')
api.add_resource(GetTemplates, '/api/getTemplate')
api.add_resource(UploadExcel, '/api/upload_excel')
api.add_resource(GetInfoMes, '/api/get_info')
api.add_resource(DeleteFileData, '/api/del_file_data')
api.add_resource(UpdateDbData, '/api/update_inputs')
api.add_resource(AddRow, '/api/new_row')
# data - Maestro Productos
api.add_resource(UpdateProduct, '/api/update_product')
api.add_resource(UploadProduct, '/api/upload_excel_product')
api.add_resource(CloneProduct, '/api/clone_product')
api.add_resource(UpsertCategoryItem, '/api/upsert_category')
api.add_resource(DeleteCategoryItem, '/api/delete_category')
# data - DB_Main
api.add_resource(CargarDBMain, '/api/cargar_db_main')
api.add_resource(CerrarMesDBMain, '/api/cerrar_db_main')
api.add_resource(GetInfoDB_Main, '/api/info_db_main')
api.add_resource(UpdateDB_Main, '/api/update_db_main')
api.add_resource(AddMultipleRows, '/api/new_multiple_rows')
# data - Otros
api.add_resource(GetProductosSinClasificar, '/api/productos_sin_clasificar')
api.add_resource(GetTransitoNart, '/api/get_transito_nart')
api.add_resource(UpsertComparacionSOP, '/api/upsert_comparacionSOP')
api.add_resource(GetDBSOP, '/api/get_db_sop')
api.add_resource(SaveRiskOPS, '/api/save_risk_ops')
# user
api.add_resource(LogIn, '/api/login')
api.add_resource(CreateUser, '/api/add_user')
api.add_resource(ModifyUser, '/api/modify_user')
api.add_resource(UserList, '/api/user_info')
api.add_resource(ChangePassword, '/api/change_pwd')
# permissions
api.add_resource(GetPermissions, '/api/get_permission')
api.add_resource(UpdatePermissions, '/api/update_permissions')
# timeline
api.add_resource(GetInfoTimeline, '/api/getinfo_timeline')
api.add_resource(SetInfoTimeline, '/api/setinfo_timeline')
# visuals
api.add_resource(GetVisualBD, '/api/getVisualBD')
api.add_resource(GetBDHistorico, '/api/get_historico')
api.add_resource(PrepareSummary, '/api/prepare_summary')
api.add_resource(UnitsxBPU, '/api/unitxbpu')
api.add_resource(NetSalesxPBU, '/api/salesxbpu')
api.add_resource(DemandSimulation, '/api/demand_simulation')
api.add_resource(FCSimulation, '/api/fc_simulation')
api.add_resource(GraphDataset, '/api/graph_dataset')
api.add_resource(GetCobertura, '/api/cobertura_graph')
# currency
api.add_resource(SetCurrency, '/api/set_currency')
api.add_resource(GetCurrency, '/api/get_currency')

if __name__ == '__main__':
  from waitress import serve
  serve(app, host="0.0.0.0", port=3100, threads=8)
  #app.run(host='0.0.0.0', port=3100, debug=True)