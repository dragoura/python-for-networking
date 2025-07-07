# -*- coding: utf-8 -*-
"""
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.

Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример итогового списка:
["Loopback0", "Tunnel0", "Ethernet0/1", "Ethernet0/3.100", "Ethernet1/0"]

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.
"""
import re
from pprint import pprint


def get_ints_without_description(filename):
    result = []

    with open(filename) as f:
        blocks = re.split(r'\n!', f.read())
        for block in blocks:
            intf_match = re.search('^interface (\S+)', block, re.MULTILINE)
            if intf_match and not re.search(r'^\sdescription ', block, re.MULTILINE):
                result.append(intf_match.group(1))

    return result


if __name__ == '__main__':
    pprint(get_ints_without_description('config_r1.txt'))
