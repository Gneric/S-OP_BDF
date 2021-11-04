from flask_jwt_extended.utils import create_refresh_token, decode_token
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from datetime import timedelta

from api.routes.login import LogIn
from api.routes.welcome import Welcome
from api.routes.users import ChangePassword, ModifyUser, CreateUser, UserList
from api.routes.visuals import GetVisualBD, PrepareSummary
from api.routes.permissions import GetPermissions, UpdatePermissions
from api.routes.data import GetData, DeleteData, CloneData, UploadExcel, GetTemplates, GetInfoMes


app = Flask(__name__)
app.config['SECRET_KEY'] = "bZwk/=X48SnCtUEWpzH2RcJP-6yeVAKTrBvDsuM_mfFj9dxqGh"
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=2)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=24)
app.config["PROPAGATE_EXCEPTIONS"] = True
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

api.add_resource(Welcome, '/api/')

api.add_resource(GetData, '/api/get_excel_data')
api.add_resource(DeleteData, '/api/del_data')
api.add_resource(CloneData, '/api/clone_data')
api.add_resource(UploadExcel, '/api/upload_excel')
api.add_resource(GetTemplates, '/api/getTemplate')
api.add_resource(GetInfoMes, '/api/get_info')

api.add_resource(LogIn, '/api/login')
api.add_resource(CreateUser, '/api/add_user')
api.add_resource(ModifyUser, '/api/modify_user')
api.add_resource(UserList, '/api/user_info')
api.add_resource(ChangePassword, '/api/change_pwd')

api.add_resource(GetPermissions, '/api/get_permission')
api.add_resource(UpdatePermissions, '/api/update_permissions')

api.add_resource(GetVisualBD, '/api/getVisualBD')
api.add_resource(PrepareSummary, '/api/prepare_summary')


if __name__ == '__main__':
  from waitress import serve
  serve(app, host="0.0.0.0", port=3100, threads=8)
  #app.run(host='0.0.0.0', port=3100, debug=True)