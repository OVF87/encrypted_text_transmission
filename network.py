import socket
import json
import time
import variables as var

class Networking:
    '''
    Класс для создания сетевого подключения
    '''
    def __init__(self, type_socket, broadcast=False):
        self.BUFFER_SIZE = var.BUFFER_SIZE # размер буфера для примем сообщений
        self.port_no = var.PORT_NO
        self.timeout = var.TIME_OUT
        self.my_socket = self.get_socket(type_socket, broadcast=broadcast)

    @classmethod
    def get_socket(cls, type_socket, broadcast=False, timeout=var.TIME_OUT):
        '''
        Создает UDP или TCP сокет
        :param broadcast: широковещателньный или нет
        :param timeout: тайм аут
        :return: сокет
        '''
        if type_socket == 'UDP':
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        elif type_socket == 'TCP':
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            return None
        # чтобы на одной машине можно было слушать тотже порт
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if broadcast:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(timeout)
        return sock

    def recv_json(self):
        '''
        Получает JSON из сокета
        :return: кортедж(dict, адрес)
        '''
        try:
            #  получить датаграмму и адрес из сокета
            data, addr = self.my_socket.recvfrom(self.BUFFER_SIZE)
            #  декодируем в юникод и загружаем из JSON
            temp = json.loads(data.decode('utf-8', errors='ignore'))
            print(temp)
            return temp, addr
        except socket.timeout:
            pass  #  ничего не пришло
        return None, None

    def recv_json_until(self, predicate, timeout):
        '''
        Несколько раз пытается получить JSON в течение timeout секунд, пока на полученных данных
        функция predicate не вернет True
        :param predicate: функция, чтобы проверять данные
        :param timeout: тайм аут
        :return:
        '''
        t0 = time.monotonic()
        while time.monotonic() < t0 + timeout:
            data, addr = self.recv_json()
            if predicate(data):
                return data, addr
        return None, None

    def bind(self, to=""):
        '''
        Привязаывается к порту, то есть начинает слушать с него сообщения
        :param to: интерфейс ("" - любой)
        '''
        print('bind to= ', to)
        self.my_socket.bind((to, self.port_no))

    def send_json(self, j, to):
        '''
        Отправляет JSON данные
        :param j: данные
        :param to: адрес кому отправить
        '''
        data = bytes(json.dumps(j), 'utf-8')
        return self.my_socket.sendto(data, (to, self.port_no))

    def send_json_broadcast(self, j):
        '''
        Оправляет JSON данные широковещательно
        :param j: данные
        '''
        return self.send_json(j, "<broadcast>")

    def __del__(self):
        print('closing socket')
        self.my_socket.close()

    def receive_data(self):
        '''
        Принимает данные по TCP пакетами по BUFFER_SIZE байт
        '''
        my_socket.bind((var.MY_ADDRESS, var.PORT_NO))
        my_socket.listen(True)

        print('Ожидание клиента...')
        conn, address = self.my_socket.accept()
        print(f'{address[0]}:{address[1]} подключен.')
        temp =b''
        while True:
            print('Получаем данные...')
            chunk = self.my_socket.recv(self.BUFFER_SIZE)
            if chunk:
                temp += chunk
            else:
                break

        print('Данные получены')
        self.__del__
        print('Соединение закрыто')
        return temp

    def send_data(self, data):
        '''
        Отправляет данные по TCP пакетами по BUFFER_SIZE байт
        '''
        print('Подключение к серверу.')
        while data:
            print('Передача данных...')
            read_bytes = data[:self.BUFFER_SIZE]
            data = data[self.BUFFER_SIZE:]
            self.my_socket.send(read_bytes)
        print('Отправлено.')
        print('Соединение закрыто.')


if __name__ == '__main__':
    network = Networking('TCP')
    network.send_data(b'asd')

