# -*- coding: utf-8 -*-
"""
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт: Скрипт не должен выводить на стандартрый поток вывода команды,
в которых содержатся слова из списка ignore.

При этом скрипт также не должен выводить строки, которые начинаются на !.

Проверить работу скрипта на конфигурационном файле config_sw1.txt.
Имя файла передается как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ignore = ["duplex", "alias", "configuration"]

from sys import argv

file_name = argv[1]

with open(file_name, "r") as f:
    for line in f:
        if not line.startswith('!'):
            is_clean = True
            for word in ignore:
                if word in line:
                    is_clean = False
                    break 
            if is_clean:
                print(line.rstrip('\n'))


# # with any
# with open(file_name, "r") as f:
#     for line in f:
#         if not line.startswith('!'):
#             if not any([word in line for word in ignore]):
#                 print(line.rstrip('\n'))

# # with set
# with open(file_name) as f:
#     for line in f:
#         words = line.split()
#         words_intersect = set(words) & set(ignore)
#         if not line.startswith("!") and not words_intersect:
#             print(line.rstrip())