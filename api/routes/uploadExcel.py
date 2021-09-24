from flask import request
from werkzeug.utils import secure_filename
from flask_restful import Resource
from ..utils.functions import *

class UploadExcel(Resource):
    def post(self):
        if 'excel_file' not in request.files:
            return 'No se encontro excel file', 400
        #if request.args['area_id'] == "": 
        #    return 'No se encontro area id', 400
        else:
            cleanDataFolder()
            try:
                errors = []
                files = request.files.getlist('excel_file')
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
                    res = checkExcelFiles()
                    if res == "":
                        return "Error al subir el archivo", 400
                    else:
                        return { "result" : res }, 200
            except SystemError as Err:
                print("ERROR : ", Err)
                return 'Resource not found', 400