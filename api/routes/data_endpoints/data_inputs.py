import sys
from os import getcwd
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename, send_from_directory
from api.utils.functions import *
from flask_restful import Resource, abort
from datetime import datetime
from flask import request


class GetData(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        id = request.json['file_id']
        area_id = request.json['area_id']
        if id == "" or area_id == "":
            return { 'error':'No se encontro parametros de id y/o area' }, 400
        else:
            try:
                res = getData(id, int(area_id))
                if res == "":
                    return { 'error':'error intentando obtener datos' }, 400
                return { "result" : res }, 200
            except:
                return { 'error':'error intentando obtener datos' }, 400

class DeleteData(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()
            year = request.json.get('year','')
            month = request.json.get('month', '')
            area_id = request.json.get('area_id', '')
            if area_id == "" or month == "" or year == "":
                return 'No se encuentran todas las varaibles necesarias', 400
            res = checkDeleteTable(area_id, year, month, current_user)
            if res == "":
                return "Error eliminando data del mes", 400
            else:
                return { "result" : res }
        except:
            return "Error buscando data del mes", 400

class CloneData(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()
            file_id = str(request.json['file_id'])
            area_id = int(request.json['area_id'])
            cleanDataFolder()
            res = cloneData(file_id, area_id, current_user)
            print('res :', res)
            if res == "":
                return "Error clonando data del mes", 400
            else:
                data_path = join(getcwd(),'api','data')
                try:
                    result = send_from_directory(
                        data_path, res, as_attachment=True, environ=request.environ
                    )
                    result.headers['filename'] = res
                    return result
                except FileNotFoundError:
                    abort(404)
        except:
            return f"Error buscando data del mes, {sys.exc_info()[1]}", 400

class GetTemplates(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()
            year = str(request.json['year'])
            month = str(request.json['month'])
            area_id = int(request.json['area_id'])
            cleanDataFolder()
            res = getTemplates(year, month, area_id)
            print('(GetTemplate) res:', res)
            if res == "" or res is None:
                return { 'error': 'error creando template / template vacio' }, 400
            else:
                data_path = join(getcwd(),'api','data')
                try:
                    result = send_from_directory(
                        data_path, res, as_attachment=True, environ=request.environ
                    )
                    result.headers['filename'] = res
                    return result
                except FileNotFoundError:
                    abort(404)
        except:
            return { 'error': 'error creando template' }, 400

class UploadExcel(Resource):
    @jwt_required()
    def post(self):
        try:
            bypass = None
            current_user = get_jwt_identity()
            if 'year' in request.form.keys():
                year = request.form['year']
            if 'month' in request.form.keys():
                month = request.form['month']
            if 'area_id' in request.form.keys():
                area_id = request.form["area_id"]
            if 'bypass' in request.form.keys():
                bypass = request.form["bypass"]
            if 'excel_file' in request.files.keys():
                files = request.files.getlist('excel_file')
            else:
                return { "error" : "No se encontraron las variables necesarias para el ingreso" }, 400
            if int(month) < 10 and len(str(month)) == 1:
                month = f"0{int(month)}"
            if request.files['excel_file'].filename == '':
                return { "error" : "No se encontro archivo excel adjunto" }, 400
            if bypass == None:
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
                res = checkExcelFiles(int(area_id), year, month, current_user, request.files['excel_file'].filename)
                cleanDataFolder()
                return res
        except:
            cleanDataFolder()
            return { 'Error' : str(sys.exc_info()) }, 400

class GetInfoMes(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        year = str(request.json['year'])
        month = str(request.json['month'])
        if year == "" or month == "":
            return 'No se encontro parametros de year y month', 400
        else:
            try:
                res = checkInfoMonth(year, month)
                return res
            except:
                return { 'error', 'error creando template' }, 400

class DeleteFileData(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        area_id = str(request.json['area_id'])
        file_id = str(request.json['file_id'])
        if area_id == "" or file_id == "":
            return { 'error', 'error en la lectura de variables' }
        else:
            try:
                res = delete_file_data(area_id, file_id)
                return res
            except:
                return { 'error', 'error en la eliminacion de data' }, 400

class UpdateDbData(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        data = request.json.get('data', '')
        if data == '':
            return { 'error': 'error en la lectura de data' }, 400
        res = update_changes_bd(data)
        return res

class AddRow(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        data = request.json.get('data', '')
        if data == '':
            return { 'error': 'error en la lectura de data' }, 400
        res = add_new_row(data)
        if res == 0:
            return { 'error': 'error al agregar fila' }, 400
        if type(res) != int and res.get('error','') != '':
            return res, 200
        return { 'result' : 'ok' }, 200