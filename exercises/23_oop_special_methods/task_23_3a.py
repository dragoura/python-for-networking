# -*- coding: utf-8 -*-

"""
Задание 23.3a

В этом задании надо сделать так, чтобы экземпляры класса Topology
были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 22.1x или задания 23.3.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
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
            
            
    def __add__(self, other):
        topology_dict = self.topology.copy()
        topology_dict.update(other.topology)
        return Topology(topology_dict)
    
    
    def __iter__(self):
        return iter(self.topology.items())


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
    for link in top:
        print(link)
    