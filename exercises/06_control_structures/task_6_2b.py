# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'
Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

while True:
    ip = input("Enter ip address in format a.b.c.d: ")
    octs = ip.split(".")

    is_correct_ip = True
    if ip.count('.') == 3:
        for oct in octs:
            if not (oct.isdigit() and int(oct) in range(256)):
                is_correct_ip = False
                break
    else:
        is_correct_ip = False
    
    if is_correct_ip:
        break
    else:
        print("Неправильный IP-адрес")

oct1 = int(octs[0])
if 1 <= oct1 and oct1 <= 223:
    print("unicast")
elif 224 <= oct1 and oct1 <= 239:
    print("multicast") 
elif ip == '255.255.255.255':
    print("local broadcast") 
elif ip == '0.0.0.0':
    print("unassigned") 
else:
    print("unused")