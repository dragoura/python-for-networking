import sqlite3
from tabulate import tabulate


def manage_get_func(argv, db_filename):
    if len(argv) == 0:
        show_all_db_data(db_filename)
    elif len(argv) == 2:
        show_db_data_with_param(db_filename, *argv)
    else:
        print('Пожалуйста, введите два или ноль аргументов')
        
        
def show_all_db_data(db_filename):
    connection = sqlite3.connect(db_filename)
    query = f'SELECT * from dhcp'
    result = [row for row in connection.execute(query)]
    connection.close()
    print('В таблице dhcp такие записи:')
    print(tabulate(result))
    

def show_db_data_with_param(db_filename, param_name, param_value):
    query_dict = {
        'vlan': 'select * from dhcp where vlan = ?',
        'mac': 'select * from dhcp where mac = ?',
        'ip': 'select * from dhcp where ip = ?',
        'interface': 'select * from dhcp where interface = ?',
        'switch': 'select * from dhcp where switch = ?',
        }
    
    if param_name not in query_dict.keys():
        print('Данный параметр не поддерживается.')
        print('Допустимые значения параметров: ' + ", ".join(query_dict.keys()))
        return
    print('Информация об устройствах с такими параметрами: {} {}'.format(param_name, param_value))
    connection = sqlite3.connect(db_filename)
    query = query_dict[param_name]
    result = [row for row in connection.execute(query, (param_value, ))]
    connection.close()
    print(tabulate(result))
    