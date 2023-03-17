import random
import network
import variables as var


class Search:
    '''
    Класс для широковещательного поиска в локальной сети
    '''
    A_SEARCH = 'search'
    A_STOP_SCAN = 'stop_scan'

    def __init__(self, pid):
        assert pid
        self._my_pid = pid
        self.port_no = var.PORT_NO
        self.my_socket = network.Networking('UDP', broadcast=True)
        self.my_socket.bind()

    def send_action(self, action: str, data=None):
        '''
        Форматирует JSON для обмена командами
        :param action: имя команды
        :param data: доп. данные, если надо
        '''
        data = data or {}
        self.my_socket.send_json_broadcast({'action': action, 'sender': self._my_pid, **data})

    def is_message_for_me(self, d: dict) -> bool:
        '''
        Проверяет, относится ли принятый пакет к нашему протоколу обнаружения
        (1) должен быть определнный action
        (2) отправитель sender должен быть не я, а кто-то другой
        '''
        temp = d and d.get('action') in [self.A_SEARCH, self.A_STOP_SCAN] and d.get('sender') != self._my_pid
        return temp

    def run(self) -> tuple:
        '''
        Запуск поиска по локальной сети
        :return: кортедж((ip адрес, port), pid)
        '''
        while True:
            self.send_action(self.A_SEARCH) #  рассылаем всем сообщение A_SEARCH
            data, addr = self.my_socket.recv_json_until(self.is_message_for_me, timeout=5.0) #  ждем приемлемого ответа не более 5 секунд
            if data: #  если нам что-то пришло
                action, sender = data['action'], data['sender']
                if action == self.A_SEARCH: #  кто-то нам отправил A_SEARCH
                    self.send_action(self.A_STOP_SCAN, {'to_pid': sender}) #  отсылаем ему сообщение остановить сканирование A_STOP_SCAN, указав его PID
                #elif action == self.A_STOP_SCAN: #  если оно не дошло? тот пир продолжит сканировать дальше...
                #    if data['to_pid'] != self._my_pid: #  если получили сообщение остановить сканирование, нужно выяснить нам ли оно предназначено
                #        continue  # это не нам; игнорировать!
                self.my_socket.__del__()
                print('addr,sender', addr, sender)
                return addr, sender


if __name__ == '__main__':
    print('Testing the Search.')
    pid = random.getrandbits(64)
    print('pid =', pid)
    info = Search(pid)
    info.run()
    print('success: ', info)
