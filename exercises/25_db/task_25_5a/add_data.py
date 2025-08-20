import glob
import os
import re
import sqlite3
import yaml
from tabulate import tabulate


# set active result
def parse_snooping(filename):
    switch = re.search(r"(\w+)_dhcp_snooping.txt", filename).group(1)
    regex = re.compile(r"(?P<mac>\S+)\s+(?P<ip>\S+)\s+\d+\s+\S+\s+(?P<vlan>\d+)\s+(?P<intf>\S+)")
    with open(filename) as f:
        result = [m.groups() + (switch, 1) for m in regex.finditer(f.read())]
    return result


def add_data(connection, query, data):
    for row in data:
        try:
            with connection:
                connection.execute(query, row)
        except sqlite3.IntegrityError as err:
            print(f"При добавлении данных {row} возникла ошибка {err}")


def add_switches(db_name, sw_file):
    connection = sqlite3.connect(db_name)
    with open(sw_file) as f:
        parsed = yaml.safe_load(f)
    switches = list(parsed["switches"].items())
    query = "INSERT into switches values (?, ?)"
    print("Добавляю данные в таблицу switches...")
    add_data(connection, query, switches)
    connection.close()
    

def add_dhcp_snooping(db_name, snooping_files):
    connection = sqlite3.connect(db_name)
    connection.execute("UPDATE dhcp set active = 0")
    connection.execute("DELETE from dhcp WHERE last_active < datetime('now', '-7 days')")
    connection.commit()
    print("Добавляю данные в таблицу dhcp...")
    data = []
    for filename in snooping_files:
        data.extend(parse_snooping(filename))
    query_replace = "REPLACE INTO dhcp VALUES (?, ?, ?, ?, ?, ?, datetime('now'))"
    add_data(connection, query_replace, data)
    connection.close()
    
    
def show_all_db_data(db_name):
    connection = sqlite3.connect(db_name)
    query = "SELECT * from dhcp"
    result = [row for row in connection.execute(query)]
    connection.close()
    print("В таблице dhcp такие записи:")
    print(tabulate(result))
    

if __name__ == "__main__":
    snooping_files = glob.glob("new_data/*_dhcp_snooping.txt")
    db_filename = "dhcp_snooping.db"
    db_exists = os.path.exists(db_filename)
    if db_exists:
        add_switches(db_filename, "switches.yml")
        add_dhcp_snooping(db_filename, snooping_files)
        show_all_db_data(db_filename)
    else:
        print("База данных не существует. Перед добавлением данных ее надо создать")
    