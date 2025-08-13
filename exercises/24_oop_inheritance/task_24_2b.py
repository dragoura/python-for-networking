# -*- coding: utf-8 -*-

"""
Задание 24.2b

Скопировать класс MyNetmiko из задания 24.2a.

Дополнить функционал метода send_config_set netmiko и добавить в него проверку
на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает
вывод команд.

In [2]: from task_24_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

"""
import re
from netmiko.cisco.cisco_ios import CiscoIosSSH
from pprint import pprint


class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании,
    возникла ошибка.
    """


class MyNetmiko(CiscoIosSSH):
    def __init__(self, **device_params):
        super().__init__(**device_params)
        self.enable()
        
    
    def send_command(self, command):
        output = super().send_command(command)
        self._check_error_in_command(command, output)
        return output
    
    
    def send_config_set(self, commands):
        if isinstance(commands, str):
            commands = [commands]
        results = []
        results.append(self.config_mode())
        for command in commands:
            output = super().send_config_set(command, exit_config_mode=False)
            self._check_error_in_command(command, output)
            results.append(output)
        results.append(self.exit_config_mode())
        return '\n'.join(results)
        
        
    def _check_error_in_command(self, command, output):
        err_template = ('При выполнении команды "{cmd}" на устройстве'
                     '{host} возникла ошибка "{err}"')
        regex = r'% (?P<error>.+)'
        match = re.search(regex, output)
        if match:
            message = err_template.format(cmd=command, host=self.host, err=match.group('error'))
            raise ErrorInCommand(message)
                

if __name__ == '__main__':
    device_params = {
        "device_type": "cisco_ios",
        "ip": "192.168.223.131",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    r1 = MyNetmiko(**device_params)
    commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
    correct_commands = ['logging buffered 20010', 'ip http server']
    pprint(r1.send_config_set(commands_with_errors))
