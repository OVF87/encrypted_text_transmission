import json
import socket
import time
import variables as var


host= socket.getaddrinfo(socket.gethostname(), None)
var.my_ip = host[1][4][0]


class Networking:
    '''
    Класс для создания сетевого подключения
    '''
    def __init__(self, type_socket, broadcast=False, port_no=None):
        self.buffer_size = var.BUFFER_SIZE # размер буфера для примем сообщений
        self.my_address = var.MY_ADDRESS
        self.port_no = port_no
        self.broadcast = broadcast
        self.timeout = var.TIME_OUT
        self.my_socket = self.get_socket(type_socket, broadcast=self.broadcast, timeout=self.timeout)

    @classmethod
    def get_socket(cls, type_socket, broadcast=False, timeout=0):
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
        print(type_socket, 'socked created')
        return sock

    def recv_json(self) -> tuple:
        '''
        Получает JSON из сокета
        :return: кортедж(dict, адрес)
        '''
        try:
            #  получить датаграмму и адрес из сокета
            data, addr = self.my_socket.recvfrom(self.buffer_size)

            #  декодируем в юникод и загружаем из JSON
            temp = json.loads(data.decode('utf-8', errors='ignore'))
            return temp, addr
        except socket.timeout:
            pass  #  ничего не пришло
        return None, None

    def recv_json_until(self, predicate, timeout: float) -> tuple:
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

    def bind(self, to=''):
        '''
        Привязаывается к порту, то есть начинает слушать с него сообщения
        :param to: интерфейс ('' - любой)
        '''
        self.my_socket.bind((to, self.port_no))

    def send_json(self, j: str, to):
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
        return self.send_json(j, '<broadcast>')

    def __del__(self):
        print('closing socket')
        self.my_socket.close()

    '''def recv_tcp(self):
        temp =b''
        print('recv data ...')
        chunk = self.my_socket.recv(self.buffer_size)
        print('chunk inner ', chunk)
        while chunk:

            if chunk:
                temp += chunk
                chunk = conn.recv(self.buffer_size)
            else:
                break
        print('recv tcp <-', chunk)
        return chunk'''

    def tran_tcp(self, data, addr):
        # Отправка файла блоками по buffer_size байта.
        print('Передача данных...')
        data = data.encode()
        while data:
            read_bytes = data[:self.buffer_size]
            data = data[self.buffer_size:]
            self.my_socket.send(read_bytes)
        print('Отправлено.')


if __name__ == '__main__':
    network = Networking('TCP')
    network.send_data(b'asd')

