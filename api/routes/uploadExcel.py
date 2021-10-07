from flask import request
from werkzeug.utils import secure_filename
from flask_restful import Resource
from ..utils.functions import *
from datetime import datetime

class UploadExcel(Resource):
    def post(self):
        try:
            if 'year' in request.form.keys():
                year = request.form['year']
            if 'month' in request.form.keys():
                month = request.form['month']
            if 'area_id' in request.form.keys():
                area_id = request.form["area_id"]
            if 'excel_file' in request.files.keys():
                files = request.files.getlist('excel_file')
            else:
                return { "error" : "No se encontraron las variables necesarias para el ingreso" }, 400

            if int(month) < 10 and len(str(month)) == 1:
                month = f"0{int(month)}"
            if request.files['excel_file'].filename == '':
                return { "error" : "No se encontro archivo excel adjunto" }, 400
            if datetime.now().strftime('%Y%m') != str(year)+str(month):
                return { "error" : "El periodo enviado no es el actual" }, 400
            
            cleanDataFolder()
            for f in files:
                if allowed_extensions(f.filename) == False:
                    return { "error" : "extension del archivo adjunto no se encuentra en el listado de aprovados" }, 400
                else:
                    f.save(join(data_path, secure_filename(f.filename)))
            
            if checkFiles() == 0:
                return { "error" : 'No files saved' }, 400
            else:                   
                res, res_check = checkExcelFiles(int(area_id), year, month)
                if res_check == "error":
                    return { "error" : res }, 400
                if res == "":
                    return { "error" : "unknown error" }, 400
                else:
                    return { "result" : res }, 200
            
        except:
            return { 'Error' : str(sys.exc_info()[1]) }, 400