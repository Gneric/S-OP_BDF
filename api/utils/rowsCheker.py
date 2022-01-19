def dataCheck(data):
    print('Data check')
    with open('readme.txt', 'w') as f:
        f.write(data)
    err = []
    for row in list(data):
        index = data.index(row)
        if index == 3:
            print('Index :', index)
            print('Row : ', row)
            print(f'ROW {3} : {row}')
        # Check data
        # if row.get('nart', 'N/A') == False:
        #     err.append({ 'fila': index, 'columna': 'NART', 'error': 'Nart vacio' })
        # if row.get('cantidad', 0) == False:
        #     err.append({ 'fila': index, 'columna': 'CANTIDAD', 'error': 'Cantidad vacia o 0' })
    return err
