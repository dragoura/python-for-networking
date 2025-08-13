# -*- coding: utf-8 -*-

"""
Задание 24.2d

Скопировать класс MyNetmiko из задания 24.2c или задания 24.2b.

Добавить параметр ignore_errors в метод send_config_set.
Если передано истинное значение, не надо выполнять проверку на ошибки и метод должен
работать точно так же как метод send_config_set в netmiko.
Если значение ложное, ошибки должны проверяться.

По умолчанию ошибки должны игнорироваться.


In [2]: from task_24_2d import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [6]: r1.send_config_set('lo')
Out[6]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [7]: r1.send_config_set('lo', ignore_errors=True)
Out[7]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [8]: r1.send_config_set('lo', ignore_errors=False)
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-8-704f2e8d1886> in <module>()
----> 1 r1.send_config_set('lo', ignore_errors=False)

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
        
    
    def send_command(self, command, *args, **kwargs):
        output = super().send_command(command, *args, **kwargs)
        self._check_error_in_command(command, output)
        return output
    
    
    def send_config_set(self, commands, ignore_errors=True):
        if ignore_errors:
            output = super().send_config_set(commands)
            return output
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
    