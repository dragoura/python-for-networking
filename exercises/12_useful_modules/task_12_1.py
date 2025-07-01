# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping (запуск ping через subprocess).
IP-адрес считается доступным, если выполнение команды ping отработало с кодом 0 (returncode).
Нюансы: на Windows returncode может быть равен 0 не только, когда ping был успешен,
но для задания нужно проверять именно код. Это сделано для упрощения тестов.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
import subprocess
import pprint

def ping_ip(ip_address):
    reply = subprocess.run(['ping', '-c', '3', '-n', ip_address],
                           stdout=subprocess.DEVNULL)
    return reply.returncode == 0


def ping_ip_addresses(ip_list):
    reachable_ipes = []
    unreachable_ipes = []

    for ip_address in ip_list:
        if ping_ip(ip_address):
            reachable_ipes.append(ip_address)
        else:
            unreachable_ipes.append(ip_address)

    return reachable_ipes, unreachable_ipes


if __name__ == '__main__':
    ip_list = list_of_ips = ["1.1.1.1", "8.8.8.8", "8.8.4.4", "8.8.7.1"]
    print(ping_ip_addresses(ip_list))