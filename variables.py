# Глобальные переменные
import socket

host= socket.getaddrinfo(socket.gethostname(), None)

PORT_NO = [37020, 37021]
TIME_OUT = 20.0  # время таймаута при ожидании данных в сокет
BUFFER_SIZE = 1024  # размер буфера для примем сообщений
MY_ADDRESS = host[1][4][0]
