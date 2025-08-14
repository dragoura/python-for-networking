import os
import sqlite3

def create_schema(db_filename, schema_filename):
    db_exists = os.path.exists(db_filename)
    if db_exists:
        print('База данных существует')
        return
    print('Создаю базу данных...')
    with open(schema_filename) as f:
        schema = f.read()
    conn = sqlite3.connect(db_filename)
    conn.executescript(schema)
    conn.close()
    
    
if __name__ == '__main__':
    db_filename = 'dhcp_snooping.db'
    schema_filename = 'dhcp_snooping_schema.sql'
    create_schema(db_filename, schema_filename)