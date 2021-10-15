from flask_jwt_extended.utils import create_refresh_token, decode_token
from api.routes.modifyUser import ModifyUser
from api.routes.welcome import Welcome
from api.routes.userList import UserList
from api.routes.cloneData import CloneData
from api.routes.getInfoMes import GetInfoMes
from api.routes.getTemplates import GetTemplates
from api.routes.uploadExcel import UploadExcel
from api.routes.getData import GetData
from api.routes.deleteData import DeleteData

from api.routes.login import LogIn
from api.routes.signin import SignIn

from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager, get_jwt_identity, create_access_token, jwt_required

from datetime import timedelta


app = Flask(__name__)
app.config['SECRET_KEY'] = "3jeYU\@++MhuRc6LmNXYD+ddq&M%jP@:uK2^SSB"
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=24)
jwt = JWTManager(app)
CORS(app, expose_headers=["filename"])
api = Api(app)

@app.route("/api/refresh", methods=["POST"])
def refresh():
    token = request.json.get('refreshToken', '')
    identity = decode_token(token)["sub"]
    if token == '':
      return { 'error': 'token no enviado' }, 400
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    return { "accessToken" : access_token, "refreshToken": refresh_token }

@jwt.token_verification_failed_loader
def token_verification_failed_loader_callback(jwt_header, jwt_payload):
  return { "error" : "token invalido" }  

@jwt.invalid_token_loader
def invalid_token_loader_callback(jwt_header):
  return { "error" : "token invalido" } 

@jwt.unauthorized_loader
def unauthorized_loader_callback(jwt_header):
  return { "error" : "token no enviado" }

api.add_resource(Welcome, '/api/')
api.add_resource(UploadExcel, '/api/upload_excel')
api.add_resource(GetData, '/api/get_excel_data')
api.add_resource(GetInfoMes, '/api/get_info')
api.add_resource(DeleteData, '/api/del_data')
api.add_resource(CloneData, '/api/clone_data')
api.add_resource(GetTemplates, '/api/getTemplate')
api.add_resource(UserList, '/api/user_info')

api.add_resource(LogIn, '/api/login')
api.add_resource(SignIn, '/api/signin')
api.add_resource(ModifyUser, '/api/modify_user')

if __name__ == '__main__':
  from waitress import serve
  serve(app, host="0.0.0.0", port=3100, threads=8)
  #app.run(host='0.0.0.0', port=3100, debug=True)