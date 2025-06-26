# -*- coding: utf-8 -*-
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ignore = ["duplex", "alias", "configuration"]

from sys import argv

input_file = argv[1]
output_file = argv[2]

with open(input_file, "r") as input, open(output_file, "w") as output:
    for line in input:
        if not line.startswith('!'):
            is_clean = True
            for word in ignore:
                if word in line:
                    is_clean = False
                    break 
            if is_clean:
                output.write(line)