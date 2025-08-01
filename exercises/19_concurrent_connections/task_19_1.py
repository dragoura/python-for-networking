# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""
from concurrent.futures import ThreadPoolExecutor
import subprocess

def ping_ip(ip_address):
    reply = subprocess.run(['ping', '-c', '3', '-n', ip_address],
                           stdout=subprocess.DEVNULL)
    return reply.returncode == 0


def ping_ip_addresses(ip_list, limit=3):
    reachable_ipes = []
    unreachable_ipes = []

    with ThreadPoolExecutor(max_workers=limit) as executor:
        for ip in ip_list:
            results = executor.map(ping_ip, ip_list)
    for result, ip in zip(results,ip_list):
        if result:
            reachable_ipes.append(ip)
        else:
            unreachable_ipes.append(ip)

    return reachable_ipes, unreachable_ipes


if __name__ == '__main__':
    ip_list = list_of_ips = ["1.1.1.1", "8.8.8.8", "8.8.4.4", "8.8.7.1"]
    print(ping_ip_addresses(ip_list))