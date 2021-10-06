from api.routes.cloneData import CloneData
from api.routes.getInfoMes import GetInfoMes
from api.routes.getTemplates import GetTemplates
from api.routes.signin import SignIn
from api.routes.welcome import Welcome
from api.routes.uploadExcel import UploadExcel
from api.routes.getData import GetData
from api.routes.deleteData import DeleteData
from api.routes.login import LogIn
from flask import Flask
from flask_cors import CORS
from flask_restful import Api


app = Flask(__name__)
api = Api(app)
CORS(app, expose_headers=["filename"])

api.add_resource(Welcome, '/api/')
api.add_resource(UploadExcel, '/api/upload_excel')
api.add_resource(GetData, '/api/get_excel_data')
api.add_resource(GetInfoMes, '/api/get_info')
api.add_resource(DeleteData, '/api/del_data')
api.add_resource(CloneData, '/api/clone_data')
api.add_resource(GetTemplates, '/api/getTemplate')


api.add_resource(LogIn, '/api/auth/login')
api.add_resource(SignIn, '/api/auth/signin')

if __name__ == '__main__':
  from waitress import serve
  serve(app, host="0.0.0.0", port=3100, threads=8)
  #app.run(host='0.0.0.0', port=3100, debug=True)