# -*- coding: utf-8 -*-
"""
Задание 11.2

Создать функцию create_network_map, которая обрабатывает
вывод команды show cdp neighbors из нескольких файлов и объединяет его в одну
общую топологию.

У функции должен быть один параметр filenames, который ожидает как аргумент
список с именами файлов, в которых находится вывод команды show cdp neighbors.

Функция должна возвращать словарь, который описывает соединения между
устройствами. Структура словаря такая же, как в задании 11.1:
    {("R4", "Fa0/1"): ("R5", "Fa0/1"),
     ("R4", "Fa0/2"): ("R6", "Fa0/0")}


Cгенерировать топологию, которая соответствует выводу из файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt

Не копировать код функций parse_cdp_neighbors и draw_topology.
Если функция parse_cdp_neighbors не может обработать вывод одного из файлов
с выводом команды, надо исправить код функции в задании 11.1.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
from task_11_1 import parse_cdp_neighbors
from pprint import pprint

infiles = [
    "sh_cdp_n_sw1.txt",
    "sh_cdp_n_r1.txt",
    "sh_cdp_n_r2.txt",
    "sh_cdp_n_r3.txt",
]

def create_network_map(filenames):
    network_map = {}

    for filename in filenames:
        with open(filename) as f:
            parsed = parse_cdp_neighbors(f.read())
            network_map.update(parsed)

    return network_map


## solution without repeating llinks
# def create_network_tree(filenames):
#     network_tree = {}

#     for filename in filenames:
#         with open(filename) as f:
#             parsed = parse_cdp_neighbors(f.read())
#             for key, value in parsed.items():
#                 if not network_tree.get(value) == key:
#                     network_tree[key] = value

#     return network_tree


if __name__ == '__main__':
    topology = create_network_map(infiles)
    # topology = create_network_tree(infiles)
    pprint(topology)