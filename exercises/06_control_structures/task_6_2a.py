# -*- coding: utf-8 -*-
"""
Задание 6.2a

Сделать копию скрипта задания 6.2.

Добавить проверку введенного IP-адреса.
Адрес считается корректно заданным, если он:
   - состоит из 4 чисел (а не букв или других символов)
   - числа разделенны точкой
   - каждое число в диапазоне от 0 до 255

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'

Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

ip = input("Enter ip address in format a.b.c.d: ")
octs = ip.split('.')
is_correct_ip = True

if ip.count('.') != 3:
    is_correct_ip = False
else:
    for oct in octs:
        if not (oct.isdigit() and int(oct) in range(256)):
            is_correct_ip = False
            break

if is_correct_ip:
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
else:
    print("неправильный ip-адрес")

