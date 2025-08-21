import os
import re
import sqlite3
import yaml
from tabulate import tabulate


def db_exists(db_file, command):
    db_exists = os.path.exists(db_file)
    if db_exists:
        return True
    else:
        print(f"База данных не существует. Перед {command} данных ее надо создать")
        return False


def create_db(db_file, schema_filename):
    db_exists = os.path.exists(db_file)
    if db_exists:
        print('База данных существует')
        return
    with open(schema_filename) as f:
        schema = f.read()
    conn = sqlite3.connect(db_file)
    conn.executescript(schema)
    conn.close()
    

def add_data_to_db(connection, query, data):
    for row in data:
        try:
            with connection:
                connection.execute(query, row)
        except sqlite3.IntegrityError as err:
            print(f"При добавлении данных {row} возникла ошибка {err}")


def add_data_switches(db_file, filenames):
    if not db_exists(db_file, "добавлением"):
        return
    connection = sqlite3.connect(db_file)
    parsed = {}
    for filename in filenames:
        with open(filename) as f:
            parsed.update(yaml.safe_load(f))
    switches = list(parsed["switches"].items())
    query = "INSERT into switches values (?, ?)"
    print("Добавляю данные в таблицу switches...")
    add_data_to_db(connection, query, switches)
    connection.close()
 
 
# set active result
def parse_snooping(filename):
    switch = re.search(r"(\w+)_dhcp_snooping.txt", filename).group(1)
    regex = re.compile(r"(?P<mac>\S+)\s+(?P<ip>\S+)\s+\d+\s+\S+\s+(?P<vlan>\d+)\s+(?P<intf>\S+)")
    with open(filename) as f:
        result = [m.groups() + (switch, 1) for m in regex.finditer(f.read())]
    return result   


def add_data(db_file, filenames):
    if not db_exists(db_file, "добавлением"):
        return
    if (isinstance(filenames, str)):
        filenames = [filenames]
    connection = sqlite3.connect(db_file)
    connection.execute("UPDATE dhcp set active = 0")
    connection.commit()
    connection.execute("DELETE from dhcp WHERE last_active < datetime('now', '-7 days')")
    connection.commit()
    data = []
    for filename in filenames:
        data.extend(parse_snooping(filename))
    query_replace = "REPLACE INTO dhcp VALUES (?, ?, ?, ?, ?, ?, datetime('now'))"
    add_data_to_db(connection, query_replace, data)
    connection.close()


def print_db_data(result, active):
    if result:
        print(
            "\n{active} записи:\n".format(active="Активные" if active else "Неактивные")
        )
        print(tabulate(result))
        
        
def get_data(db_file, key, value):
    if not db_exists(db_file, "чтением"):
        return
    query_dict = {
        "vlan": f"select * from dhcp where vlan = ? AND active = ?",
        "mac": f"select * from dhcp where mac = ? AND active = ?",
        "ip": f"select * from dhcp where ip = ? AND active = ?",
        "interface": f"select * from dhcp where interface = ? AND active = ?",
        "switch": f"select * from dhcp where switch = ? AND active = ?",
    }
    
    if key not in query_dict.keys():
        print("Данный параметр не поддерживается.")
        print("Допустимые значения параметров: " + ", ".join(query_dict.keys()))
        return
    connection = sqlite3.connect(db_file)
    query = query_dict[key]
    for active in (1, 0):
        result = list(connection.execute(query, (value, active)))
        print_db_data(result, active)
    connection.close()


def get_all_data(db_file):
    if not db_exists(db_file, "чтением"):
        return
    connection = sqlite3.connect(db_file)
    query = f"SELECT * from dhcp WHERE active = ?"
    for active in (1, 0):
        result = list(connection.execute(query, (active, )))
        print_db_data(result, active)
    connection.close()
