# -*- coding: utf-8 -*-
"""
Задание 15.1a

Скопировать функцию get_ip_from_cfg из задания 15.1 и переделать ее таким образом,
чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

В словарь добавлять только те интерфейсы, на которых настроены IP-адреса.

Например (взяты произвольные адреса):
{'FastEthernet0/1': ('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2': ('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""

import re
from pprint import pprint

# # first variant with for
# def get_ip_from_cfg(filename):
#     intf_dict = {}
#     regex = (r'interface (?P<intf>\S+)| ip address (?P<ip>\S+) (?P<mask>\S+)')

#     with open(filename) as f:
#         match_iter = re.finditer(regex, f.read())
#         for match in match_iter:
#             if match.lastgroup == 'intf':
#                 intf = match.group(match.lastgroup)
#             else:
#                 _, ip, prefix = match.groups()
#                 intf_dict[intf] = (ip, prefix)

#     return intf_dict


# second variant with dict comprehension
def get_ip_from_cfg(filename):
    with open(filename) as f:
        regex = (r'interface (?P<intf>\S+)\n'
                 r'( .*\n)*'
                 r' ip address (?P<ip>\S+) (?P<mask>\S+)')
        match_iter = re.finditer(regex, f.read())

    intf_dict = {m.group('intf'): m.group('ip', 'mask') for m in match_iter}
    return intf_dict


if __name__ == '__main__':
    pprint(get_ip_from_cfg('config_r2.txt'))