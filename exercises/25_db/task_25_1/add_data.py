import glob
import os
import re
import sqlite3
import yaml


def parse_snooping(filename):
    switch = filename.split('_')[0]
    regex = re.compile(r'(?P<mac>\S+)\s+(?P<ip>\S+)\s+\d+\s+\S+\s+(?P<vlan>\d+)\s+(?P<intf>\S+)')
    with open(filename) as f:
        result = [m.groups() + (switch,) for m in regex.finditer(f.read())]
    return result


def add_data(db_filename, query, data):
    connection = sqlite3.connect(db_filename)
    for row in data:
        try:
            with connection:
                connection.execute(query, row)
        except sqlite3.IntegrityError as err:
            print(f'При добавлении данных {row} возникла ошибка {err}')
    connection.close()

def add_switches(db_filename, sw_file):
    db_exists = os.path.exists(db_filename)
    if not db_exists:
        print('База данных не существует. Перед добавлением данных, ее надо создать')
        return
    with open(sw_file) as f:
        parsed = yaml.safe_load(f)
    switches = list(parsed['switches'].items())
    query = 'INSERT into switches values (?, ?)'
    print('Добавляю данные в таблицу switches...')
    add_data(db_filename, query, switches)
    

def add_dhcp_snooping(db_filename, snooping_files):
    db_exists = os.path.exists(db_filename)
    if not db_exists:
        print('База данных не существует. Перед добавлением данных, ее надо создать')
        return
    query = ('INSERT into dhcp (mac, ip, vlan, interface, switch)'
             'values (?, ?, ?, ?, ?)')
    data = []
    for filename in snooping_files:
        data.extend(parse_snooping(filename))
    print('Добавляю данные в таблицу dhcp...')
    add_data(db_filename, query, data)
    

if __name__ == '__main__':
    db_filename = 'dhcp_snooping.db'
    snooping_files = glob.glob('*_dhcp_snooping.txt')
    add_switches(db_filename, 'switches.yml')
    add_dhcp_snooping(db_filename, snooping_files)
    