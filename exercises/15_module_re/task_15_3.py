# -*- coding: utf-8 -*-
"""
Задание 15.3

Создать функцию convert_ios_nat_to_asa, которая конвертирует правила NAT
из синтаксиса cisco IOS в cisco ASA.

Функция ожидает такие аргументы:
- имя файла, в котором находится правила NAT Cisco IOS
- имя файла, в который надо записать полученные правила NAT для ASA

Функция ничего не возвращает.

Проверить функцию на файле cisco_nat_config.txt.

Пример правил NAT cisco IOS
ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

И соответствующие правила NAT для ASA:
object network LOCAL_10.1.2.84
 host 10.1.2.84
 nat (inside,outside) static interface service tcp 22 20022
object network LOCAL_10.1.9.5
 host 10.1.9.5
 nat (inside,outside) static interface service tcp 22 20023

В файле с правилами для ASA:
- не должно быть пустых строк между правилами
- перед строками "object network" не должны быть пробелы
- перед остальными строками должен быть один пробел

Во всех правилах для ASA интерфейсы будут одинаковыми (inside,outside).
"""

import re

# # first variant
# def convert_ios_nat_to_asa(ios_filename, asa_filename):
#     with open(ios_filename) as input, open(asa_filename, 'w') as output:
#         output.writelines(re.sub(r'.* ([\d.]+) (\d+) .* (\d+)', 
#                      r'object network LOCAL_\1\n' \
#                      r' host \1\n' \
#                      r' nat (inside,outside) static interface service tcp \2 \3',
#                      input.read()))
        

# improved second variant
def convert_ios_nat_to_asa(ios_filename, asa_filename):
    regex = r'tcp (?P<l_ip>\S+) +(?P<lport>\d+) +interface +\S+ (?P<outside_port>\d+)'
    asa_template = (
        'object network LOCAL_{l_ip}\n'
        ' host {l_ip}\n' \
        ' nat (inside,outside) static interface service tcp {lport} {outside_port}\n')
    
    with open(ios_filename) as input, open(asa_filename, 'w') as output:
        data = re.finditer(regex, input.read())
        for match in data:
            output.write(asa_template.format(**match.groupdict()))


if __name__ == '__main__':
    convert_ios_nat_to_asa('cisco_nat_config.txt', 'cisco_asa_config.txt')