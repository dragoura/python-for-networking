# -*- coding: utf-8 -*-
"""
Задание 21.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM.
  Например, templates/sh_ip_int_br.template
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt
и шаблоне templates/sh_ip_int_br.template.
"""
import textfsm
from netmiko import ConnectHandler
from pprint import pprint


def parse_output_to_dict(template, command_output):
    with open(template) as templ:
        fsm = textfsm.TextFSM(templ)
        parsed_output = fsm.ParseText(command_output)
    header = fsm.header
    result = [dict(zip(header, line)) for line in parsed_output]
    return result


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
    result = parse_output_to_dict("templates/sh_ip_int_br.template", output)
    pprint(result)