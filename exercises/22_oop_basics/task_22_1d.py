# -*- coding: utf-8 -*-

"""
Задание 22.1d

Изменить класс Topology из задания 22.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще
 нет в топологии.
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение
"Соединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Соединение с одним из портов существует


"""
from pprint import pprint


class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)


    def _normalize(self, topology_dict):
        topology = {}
        for key, value in topology_dict.items():
            if not topology.get(value) == key:
                topology[key] = value 
        return topology
    

    def delete_link(self, src_port, dst_port):
        if self.topology.get(src_port) == dst_port:
           del self.topology[src_port]
        elif self.topology.get(dst_port) == src_port:
            del self.topology[dst_port]
        else:
           print('Такого соединения нет')  
    

    def delete_node(self, node):
        original_len = len(self.topology)
        for src_port, dst_port in list(self.topology.items()):
            if node in src_port or node in dst_port:
                del self.topology[src_port]
        if original_len == len(self.topology):
            print('Такого устройства нет')


    def add_link(self, src_port, dst_port):
        all_ports = set(self.topology.keys()) | set(self.topology.values())
        if (self.topology.get(src_port) == dst_port or
            self.topology.get(dst_port) == src_port):
            print('Такое соединение существует')
        elif src_port in all_ports or dst_port in all_ports:
            print('Cоединение с одним из портов существует')
        else:
            self.topology[src_port] = dst_port


if __name__ == '__main__':
    topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
    }
    top = Topology(topology_example)
    top.add_link(("SW18", "Eth0/3"), ("R34", "Eth0/0"))
    top.add_link(("SW118", "Eth0/3"), ("R34", "Eth0/0"))
    pprint(top.topology)
