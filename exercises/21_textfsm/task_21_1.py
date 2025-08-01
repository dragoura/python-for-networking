# -*- coding: utf-8 -*-
"""
Задание 21.1

Создать функцию parse_command_output. Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM
  Например, templates/sh_ip_int_br.template
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список:
* первый элемент - это список с названиями столбцов
* остальные элементы это списки, в котором находятся результаты обработки вывода

Проверить работу функции на выводе команды sh ip int br с оборудования
и шаблоне templates/sh_ip_int_br.template.

"""
import textfsm
from netmiko import ConnectHandler
from pprint import pprint


def parse_command_output(template, command_output):
    with open(template) as templ:
        fsm = textfsm.TextFSM(templ)
        parsed_output = fsm.ParseText(command_output)
        header = fsm.header
    return [header] + parsed_output


if __name__ == "__main__":
    r1_params = {
        "device_type": "cisco_ios",
        "host": "192.168.223.131",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    with ConnectHandler(**r1_params) as r1:
        r1.enable()
        output = r1.send_command("sh ip int br")
    result = parse_command_output("templates/sh_ip_int_br.template", output)
    pprint(result)
