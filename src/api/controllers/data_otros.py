import sys
import xlsxwriter

from src.api.hasura_queries.data_otros import *
from src.api.hasura_queries.data_db_main import request_alldata_db_main, request_update_comparacion_sop
from src.api.hasura_queries.data_product_master import request_maestro_categorias
from src.api.services.data_handler import createDBMainFile

def createFileProductosOtros():
    try:
        data = get_productos_otros()
        categorias = request_maestro_categorias()
        app_form_list = [ x['name'] for x in categorias if x['category'] == 'APPLICATIONFORM' ]
        bpu_list = [ x['name'] for x in categorias if x['category'] == 'BPU' ]
        brandcategory_list = [ x['name'] for x in categorias if x['category'] == 'BRANDCATEGORY' ]
        tipo_list = [ x['name'] for x in categorias if x['category'] == 'TIPO' ]
        category_lists = [ app_form_list, bpu_list, tipo_list, brandcategory_list ]
        filename = "Productos_sin_clasificar.xlsx"
        workbook = xlsxwriter.Workbook(f"api/data/{filename}")
        worksheet = workbook.add_worksheet("NoClasificados")
        details = workbook.add_worksheet('details')
        col_num = 0
        for l in category_lists:
            for r, category in enumerate(l):
                details.write(r, col_num, category)
            col_num = col_num + 1
        details.hide()
        if data:
            keys = list(data[0].keys())
            worksheet.write('A1',keys[0])
            worksheet.write('B1',keys[1])
            worksheet.write('C1',keys[2])
            worksheet.write('D1',keys[3])
            worksheet.write('E1',keys[4])
            worksheet.write('F1',keys[5])
            worksheet.write('G1',keys[6])
            worksheet.write('H1',keys[7])
            worksheet.write('I1',keys[8])
            worksheet.write('J1',keys[9])
            worksheet.write('K1',keys[10])
            rowIndex = 2
            for row in data:
                print(f'{rowIndex=}')
                worksheet.write(f'A{rowIndex}', row['BG'])
                worksheet.write(f'B{rowIndex}', row['Material'])
                worksheet.write(f'C{rowIndex}', row['SPGR'])
                worksheet.write(f'D{rowIndex}', row['TIPO'])
                worksheet.write(f'E{rowIndex}', row['Descripcion'])
                worksheet.write(f'F{rowIndex}', row['Portafolio'])
                worksheet.write(f'G{rowIndex}', row['BPU'])
                worksheet.write(f'H{rowIndex}', row['BrandCategory'])
                worksheet.write(f'I{rowIndex}', row['ApplicationForm'])
                worksheet.write(f'J{rowIndex}', row['EAN'])
                worksheet.write(f'K{rowIndex}', row['SPGR_historico'])
                rowIndex+=1
        else:
            worksheet.write(f'A1', 'BG')
            worksheet.write(f'B1', 'Material')
            worksheet.write(f'C1', 'SPGR')
            worksheet.write(f'D1', 'TIPO')
            worksheet.write(f'E1', 'Descripcion')
            worksheet.write(f'F1', 'Portafolio')
            worksheet.write(f'G1', 'BPU')
            worksheet.write(f'H1', 'BrandCategory')
            worksheet.write(f'I1', 'ApplicationForm')
            worksheet.write(f'J1', 'EAN')
            worksheet.write(f'K1', 'SPGR_historico')
        
        worksheet.data_validation('I2:I100', { 'validate': 'list', 'source': '=Details!$A$1:$A$'+str(len(app_form_list)), 'error_message': 'El dato ingresado no concuerda con las categorias definidas' } )
        worksheet.data_validation('G2:G100', { 'validate': 'list', 'source': '=Details!$B$1:$B$'+str(len(bpu_list)), 'error_message': 'El dato ingresado no concuerda con las categorias definidas' } )
        worksheet.data_validation('D2:D100', { 'validate': 'list', 'source': '=Details!$C$1:$C$'+str(len(tipo_list)), 'error_message': 'El dato ingresado no concuerda con las categorias definidas' } )
        worksheet.data_validation('H2:H100', { 'validate': 'list', 'source': '=Details!$D$1:$D$'+str(len(brandcategory_list)), 'error_message': 'El dato ingresado no concuerda con las categorias definidas' } )
        cell_format = workbook.add_format()
        cell_format.set_text_wrap()
        cell_format.set_align('top')
        cell_format.set_align('left=')
        workbook.close()
        return filename
    except:
        print('error createFileProductosOtros :', sys.exc_info())
        return ""

def get_transito_nart(nart):
    try:
        res = request_transito_nart(nart)
        if res:
            return res
        else:
            return { 'error', 'error al obtener datos del nart ingresado' }, 400
    except:
        return { 'error', 'error al obtener datos del nart ingresado' }, 400

def upsert_comparacion_sop(data):
    try:
        unique = list( { str(each['id'])+str(each['brand_category'])+str(each['application_form'])+str(each['bpu']) : each for each in data }.values() )
        res = request_update_comparacion_sop(unique)
        if res:
            return res
        else:
            return { 'error': 'error en la respuesta de actualizacion' }, 400
    except:
        print(sys.exc_info())
        return { 'error': 'error haciendo la peticion de actualizacion' }, 400

def request_db_main(id):
    try:
        data = request_alldata_db_main(id)
        if data == []:
            return ""
        else:
            return createDBMainFile(data,id)
    except:
        return ""