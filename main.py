#!/home/overlord/apps/S-OP_BDF/env/bin/python

from api.routes.getInfoMes import GetInfoMes
from api.routes.welcome import Welcome
from api.routes.uploadExcel import UploadExcel
from api.routes.getData import GetData
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(Welcome, '/')
api.add_resource(UploadExcel, '/upload_excel')
api.add_resource(GetData, '/get_excel_data')
api.add_resource(GetInfoMes, '/get_info')

if __name__ == '__main__':
  from waitress import serve
  serve(app, host="0.0.0.0", port=3100, threads=8)
  #app.run(host='0.0.0.0', port=3006, debug=True)