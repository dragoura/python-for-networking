# -*- coding: utf-8 -*-
"""
Задание 12.3

Создать функцию print_ip_table, которая отображает таблицу доступных
и недоступных IP-адресов.

Функция ожидает как аргументы два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

"""

from task_12_1 import ping_ip_addresses
from tabulate import tabulate

def print_ip_table(reachable_ip, unreachable_ip):
    ip_table = {'Reachable': reachable_ip, 'Unreachable': unreachable_ip}
    print(tabulate(ip_table, headers='keys'))


if __name__ == '__main__':
    print_ip_table(['1.1.1.1'], ['2.2.2.2'])

    ip_list = list_of_ips = ["1.1.1.1", "8.8.8.8", "8.8.4.4", "8.8.7.1"]
    reachable_ip, unreachable_ip = ping_ip_addresses(ip_list)
    print_ip_table(reachable_ip, unreachable_ip)
