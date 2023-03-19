import random
import network
import variables as var


class Search:
    '''
    Класс для широковещательного поиска в локальной сети
    '''
    A_SEARCH = 'search'
    A_STOP_SCAN = 'stop_scan'

    def __init__(self, pid: int, my_n: int, my_public_key: int):
        self.my_pid = pid
        self.my_n = my_n
        self.my_public_key = my_public_key
        self.port_no = var.PORT_NO
        self.my_socket = network.Networking('UDP', broadcast=True)
        self.my_socket.bind()

    def send_action(self, action: str, data: dict):
        '''
        Форматирует JSON для обмена командами и отправляет его
        :param action: имя команды
        :param data: доп. данные
        '''
        data = data or {}
        self.my_socket.send_json_broadcast({'action': action, 'sender': self.my_pid, **data})

    def is_message_for_me(self, d: dict) -> bool:
        '''
        Проверяет, относится ли принятый пакет к нашему протоколу обнаружения
        (1) должен быть определнный action
        (2) отправитель sender должен быть не я, а кто-то другой
        '''
        temp = d and d.get('action') in [self.A_SEARCH, self.A_STOP_SCAN] and d.get('sender') != self.my_pid
        return temp

    def run(self) -> tuple:
        '''
        Запуск поиска по локальной сети
        :return: кортедж((ip адрес, port), pid, n, public_key)
        '''
        while True:
            self.send_action(self.A_SEARCH, {'n': self.my_n, 'public_key':self.my_public_key}) #  рассылаем всем сообщение A_SEARCH, n, public_key
            data, addr = self.my_socket.recv_json_until(self.is_message_for_me, timeout=5.0) #  ждем приемлемого ответа не более 5 секунд
            print('data run', data)
            if data: #  если нам что-то пришло
                action, sender, n, public_key = data['action'], data['sender'], data['n'], data['public_key']
                if action == self.A_SEARCH: #  кто-то нам отправил A_SEARCH
                    print('send stop scan')
                    self.send_action(self.A_STOP_SCAN, {'to_pid': sender, 'n': self.my_n, 'public_key':self.my_public_key}) #  отсылаем ему сообщение A_STOP_SCAN, указав его PID, n, public_key
                elif action == self.A_STOP_SCAN:
                    if data['to_pid'] != self.my_pid:
                        continue  # это не нам; игнорировать!
                self.my_socket.__del__()
                print('addr,sender', addr, sender)
                return addr, sender, n, public_key


if __name__ == '__main__':
    print('Testing the Search.')
    pid = random.getrandbits(64)
    print('pid =', pid)
    info = Search(pid)
    info.run()
    print('success: ', info)
