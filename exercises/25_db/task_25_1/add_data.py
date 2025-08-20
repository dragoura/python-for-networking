import glob
import re
import sqlite3
import yaml

def parse_snooping(filename):
    switch = filename.split('_')[0]
    regex = re.compile(r'(?P<mac>\S+)\s+(?P<ip>\S+)\s+\d+\s+\S+\s+(?P<vlan>\d+)\s+(?P<intf>\S+)')
    with open(filename) as f:
        result = [m.groups() + (switch,) for m in regex.finditer(f.read())]
    return result


def add_data(connection, query, data):
    for row in data:
        try:
            with connection:
                connection.execute(query, row)
        except sqlite3.IntegrityError as err:
            print(f'При добавлении данных {row} возникла ошибка {err}')


def add_switches(db_name, sw_file):
    with open(sw_file) as f:
        parsed = yaml.safe_load(f)
    switches = list(parsed['switches'].items())
    connection = sqlite3.connect(db_name)
    query = 'INSERT into switches values (?, ?)'
    print('Добавляю данные в таблицу switches...')
    add_data(connection, query, switches)
    connection.close()
    

def add_dhcp_snooping(db_name, snooping_files):
    query = ('INSERT into dhcp (mac, ip, vlan, interface, switch)'
             'values (?, ?, ?, ?, ?)')
    data = []
    for filename in snooping_files:
        data.extend(parse_snooping(filename))
    print('Добавляю данные в таблицу dhcp...')
    connection = sqlite3.connect(db_name)
    add_data(connection, query, data)
    connection.close()
    

if __name__ == '__main__':
    snooping_files = glob.glob('*_dhcp_snooping.txt')
    db_filename = 'dhcp_snooping.db'
    add_switches(db_filename, 'switches.yml')
    add_dhcp_snooping(db_filename, snooping_files)
    