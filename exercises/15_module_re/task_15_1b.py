# -*- coding: utf-8 -*-
"""
Задание 15.1b

Проверить работу функции get_ip_from_cfg из задания 15.1a
на конфигурации config_r2.txt.

Обратите внимание, что на интерфейсе e0/1 назначены два IP-адреса:
interface Ethernet0/1
 ip address 10.255.2.2 255.255.255.0
 ip address 10.254.2.2 255.255.255.0 secondary

А в словаре, который возвращает функция get_ip_from_cfg, интерфейсу Ethernet0/1
соответствует только один из них.

Скопировать функцию get_ip_from_cfg из задания 15.1a и переделать ее таким
образом, чтобы в значении словаря она возвращала список кортежей
для каждого интерфейса.
Если на интерфейсе назначен только один адрес, в списке будет один кортеж.
Если же на интерфейсе настроены несколько IP-адресов, то в списке будет
несколько кортежей. Ключом остается имя интерфейса.

Проверьте функцию на конфигурации config_r2.txt и убедитесь, что интерфейсу
Ethernet0/1 соответствует список из двух кортежей.

Обратите внимание, что в данном случае, можно не проверять корректность
IP-адреса, диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""
import re
from pprint import pprint


def get_ip_from_cfg(filename):
    intf_dict = {}
    regex = re.compile(r"^interface (?P<intf>\S+)"
             r"|address (?P<ip>\S+) (?P<mask>\S+)")
    
    with open(filename) as f:
        for line in f:
            match = regex.search(line)
            if match:
                if match.lastgroup == 'intf':
                    intf = match.group(match.lastgroup)
                elif match.lastgroup == 'mask':
                    intf_dict.setdefault(intf, [])
                    intf_dict[intf].append(match.group('ip', 'mask'))

    return intf_dict


if __name__ == '__main__':
    pprint(get_ip_from_cfg('config_r2.txt'))
