# -*- coding: utf-8 -*-

"""
Задание 23.2

Скопировать класс CiscoTelnet из задания 22.2 и добавить классу поддержку
работы в менеджере контекста.
При выходе из блока менеджера контекста должно закрываться соединение.

Пример работы:

In [14]: r1_params = {
    ...:     'ip': '192.168.100.1',
    ...:     'username': 'cisco',
    ...:     'password': 'cisco',
    ...:     'secret': 'cisco'}

In [15]: from task_23_2 import CiscoTelnet

In [16]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:
sh clock
*19:17:20.244 UTC Sat Apr 6 2019
R1#

In [17]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:     raise ValueError('Возникла ошибка')
    ...:
sh clock
*19:17:38.828 UTC Sat Apr 6 2019
R1#
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-17-f3141be7c129> in <module>
      1 with CiscoTelnet(**r1_params) as r1:
      2     print(r1.send_show_command('sh clock'))
----> 3     raise ValueError('Возникла ошибка')
      4

ValueError: Возникла ошибка

Тест проверяет подключение с параметрами из файла devices.yaml. Там должны быть
указаны доступные устройства.
"""
import re
import telnetlib
import time
from pprint import pprint
from textfsm import clitable


class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.host = ip
        self.telnet = telnetlib.Telnet(ip)
        self.telnet.read_until(b'Username')
        self._write_line(username)
        self.telnet.read_until(b'Password')
        self._write_line(password)
        self._write_line('enable')
        self.telnet.read_until(b'Password')
        self._write_line(secret)
        self._write_line('terminal length 0')
        time.sleep(1)
        self.telnet.read_very_eager()


    def _write_line(self, line):
        self.telnet.write(f'{line}\n'.encode('utf-8')) 
   
   
    def send_show_command(self, command, parse=True, templates='templates', index='index'):
        self._write_line(command)
        time.sleep(1)
        output = self.telnet.read_very_eager().decode('utf-8')
        if not parse:
            return output
        attributes_dict = {'Command': command, 'Vendor': 'cisco_ios'}
        cli_table = clitable.CliTable(index, templates)
        cli_table.ParseCmd(output, attributes_dict)
        header = list(cli_table.header) 
        result = [dict(zip(header, row)) for row in cli_table]
        return result
   
   
    def _process_error_in_command(self, command, output, strict):
        error_msg = ('При выполнении команды "{cmd}" '
                     'на устройстве {host} возникла ошибка -> {error}')
        regex = r'% (?P<error>.+)'
        match = re.search(regex, output)
        if match:
            message = error_msg.format(cmd=command, host=self.host, error=match.group('error'))
        if strict:
            raise ValueError(message)
        else:
            print(message)
      
   
    def send_config_commands(self, commands, strict=True):
        if isinstance(commands, str):
            commands = [commands]
      
        results = []
        self._write_line('conf t')
        for command in commands:
            self._write_line(command)
            time.sleep(1)
            result = self.telnet.read_very_eager().decode('utf-8')
            results.append(result)
            self._process_error_in_command(command, result, strict)
        self._write_line('end')
        time.sleep(1)
        results.append(self.telnet.read_very_eager().decode('utf-8'))
        return '\n'.join(results)
    
    
    def __enter__(self):
        return self
    
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.telnet.close()
        

if __name__ == '__main__':
    r1_params = {
        'ip': '192.168.223.131',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco'
        }
    commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
    correct_commands = ['logging buffered 20010', 'ip http server']
    with CiscoTelnet(**r1_params) as r1:
        pprint(r1.send_show_command('sh ip int br'))