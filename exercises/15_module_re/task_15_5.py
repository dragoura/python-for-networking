# -*- coding: utf-8 -*-
"""
Задание 15.5

Создать функцию generate_description_from_cdp, которая ожидает как аргумент
имя файла, в котором находится вывод команды show cdp neighbors.

Функция должна обрабатывать вывод команды show cdp neighbors и генерировать
на основании вывода команды описание для интерфейсов.

Например, если у R1 такой вывод команды:
R1>show cdp neighbors
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
SW1              Eth 0/0           140          S I      WS-C3750-  Eth 0/1

Для интерфейса Eth 0/0 надо сгенерировать такое описание
description Connected to SW1 port Eth 0/1

Функция должна возвращать словарь, в котором ключи - имена интерфейсов,
а значения - команда задающая описание интерфейса:
'Eth 0/0': 'description Connected to SW1 port Eth 0/1'


Проверить работу функции на файле sh_cdp_n_sw1.txt.
"""

import re
from pprint import pprint

## with for
# def generate_description_from_cdp(filename):
#     result = {}
#     template = 'description Connected to {0} port {1}'
#     with open(filename) as f:
#         for line in f:
#             match = re.search(r'(?P<device>\S+) +'
#                               r'(?P<l_intf>\S+ \S+) +'
#                               r'\d+ + [RSI ]* + \S+ +'
#                               r'(?P<r_intf>\S+ \S+)', line)
#             if match:
#                 result[match.group('l_intf')] = template.format(match.group('device'), match.group('r_intf'))
            
#     return result

# with dict comprehension
def generate_description_from_cdp(filename):
    regex = re.compile(r'(?P<device>\S+) +'
                       r'(?P<l_intf>\S+ \S+) +'
                       r'\d+ +[RSI ]* +\S+ +'
                       r'(?P<r_intf>\S+ \S+)')
    
    with open(filename) as f:
        match_iter = regex.finditer(f.read())
        template = 'description Connected to {0} port {1}'
        result = {m.group('l_intf'): 
                  template.format(m.group('device'), m.group('r_intf')) 
                  for m in match_iter}
    
    return result


if __name__ == '__main__':
    pprint(generate_description_from_cdp('sh_cdp_n_sw1.txt'))