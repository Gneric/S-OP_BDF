from flask import request
from werkzeug.utils import secure_filename
from flask_restful import Resource
from ..utils.functions import *

class UploadExcel(Resource):
    def post(self):
        errors = []
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
                return 'No se encuentran todas las varaibles necesarias', 400

            if int(month) < 10 and len(str(month)) == 1:
                month = f"0{int(month)}"
            if 'excel_file' not in request.files:
                return 'No se encontro excel file', 400
            if datetime.now().strftime('%Y%m') != str(year)+str(month):
                return "El periodo enviado no es el actual", 400 
            
            cleanDataFolder()
            for f in files:
                if allowed_extensions(f.filename) == False:
                    errors.append({f"{f.filename}": 'File type is not allowed'})
                if allowed_names(f.filename) == False:
                    errors.append({f"{f.filename}": 'File name is not on listed aproved filenames'})
                else:
                    f.save(join(data_path, secure_filename(f.filename)))
            
            n_files = checkFiles()
            if n_files == 0:
                return 'No files saved', 400
            else:                   
                res = checkExcelFiles(area_id, year, month)
                if res == "":
                    return "Error al subir el archivo", 400
                else:
                    return { "result" : res }, 200
        except SystemError as Err:
            print("ERROR : ", Err)
            return { 'Error' : errors }, 400