# -*- coding: utf-8 -*-
"""
Задание 7.3a

Сделать копию скрипта задания 7.3.

Переделать скрипт: Отсортировать вывод по номеру VLAN

В результате должен получиться такой вывод:
10       01ab.c5d0.70d0      Gi0/8
10       0a1b.1c80.7000      Gi0/4
100      01bb.c580.7000      Gi0/1
200      0a4b.c380.7c00      Gi0/2
200      1a4b.c580.7000      Gi0/6
300      0a1b.5c80.70f0      Gi0/7
300      a2ab.c5a0.700e      Gi0/3
500      02b1.3c80.7b00      Gi0/5
1000     0a4b.c380.7d00      Gi0/9

Обратите внимание на vlan 1000 - он должен выводиться последним.
Правильной сортировки можно добиться, если vlan будет числом, а не строкой.

Подсказка: Для сортировки удобно сначала создать список списков такого типа,
а потом сортировать.

[[100, '01bb.c580.7000', 'Gi0/1'],
 [200, '0a4b.c380.7c00', 'Gi0/2'],
 [300, 'a2ab.c5a0.700e', 'Gi0/3'],
 [10, '0a1b.1c80.7000', 'Gi0/4'],
 [500, '02b1.3c80.7b00', 'Gi0/5'],
 [200, '1a4b.c580.7000', 'Gi0/6'],
 [300, '0a1b.5c80.70f0', 'Gi0/7'],
 [10, '01ab.c5d0.70d0', 'Gi0/8'],
 [1000, '0a4b.c380.7d00', 'Gi0/9']]

Сортировка должна быть по первому элементу (vlan), а если первый элемент одинаковый,
то по второму. Так работает по умолчанию функция sorted и метод sort, если сортировать
список списков выше.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

template = "{:<9}{:<20}{}"
mac_address_table = []

with open("CAM_table.txt", "r") as f:
    for line in f:
        line_list = line.strip().split()
        if line_list and line_list[0].isdigit():
            mac_address_line = [int(line_list[0]), line_list[1], line_list[3]]
            mac_address_table.append(mac_address_line)

mac_address_table.sort()

for line in mac_address_table:
    print(template.format(line[0], line[1], line[2]))