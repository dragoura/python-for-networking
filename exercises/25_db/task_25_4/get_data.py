import sqlite3
from pprint import pprint
from tabulate import tabulate


def manage_get_func(argv, db_filename):
    if len(argv) == 0:
        show_all_db_data(db_filename)
    elif len(argv) == 2:
        show_db_data_with_param(db_filename, *argv)
    else:
        print("Пожалуйста, введите два или ноль аргументов")
        

def print_db_data(result, active):
    if result:
        print(
            "\n{active} записи:\n".format(active="Активные" if active else "Неактивные")
        )
        print(tabulate(result))
        
        
def show_all_db_data(db_filename):
    print("В таблице dhcp такие записи:")
    connection = sqlite3.connect(db_filename)
    query = f"SELECT * from dhcp WHERE active = ?"
    for active in (1, 0):
        result = list(connection.execute(query, (active, )))
        print_db_data(result, active)
    connection.close()
   

def show_db_data_with_param(db_filename, param_name, param_value):
    query_dict = {
        "vlan": f"select * from dhcp where vlan = ? AND active = ?",
        "mac": f"select * from dhcp where mac = ? AND active = ?",
        "ip": f"select * from dhcp where ip = ? AND active = ?",
        "interface": f"select * from dhcp where interface = ? AND active = ?",
        "switch": f"select * from dhcp where switch = ? AND active = ?",
    }
    
    if param_name not in query_dict.keys():
        print("Данный параметр не поддерживается.")
        print("Допустимые значения параметров: " + ", ".join(query_dict.keys()))
        return
    print("Информация об устройствах с такими параметрами: {} {}".format(param_name, param_value))
    connection = sqlite3.connect(db_filename)
    query = query_dict[param_name]
    for active in (1, 0):
        result = list(connection.execute(query, (param_value, active)))
        print_db_data(result, active)
    connection.close()
