# Модуль с основной логикой программы
import random
import threading
from cripto import Cripto
from gui import Gui
from network import Networking
from search import Search
import variables as var



port_no = var.PORT_NO
window = Gui()
crp = Cripto()


def main():
    def enc(*args):
        # Привязка функции расшифровки модуля cripto к графическому интерфейсу
        text = window.get_text()
        window.add_msg_in_list('I -> ' + text)
        enc_text = crp.get_encrypt(text, window.my_public_key, window.my_n)
        window.add_msg_in_list('I ENCRYPTED -> ' + enc_text)
        window.pull_text(enc_text)


    def decr(*args):
        # Привязка функции зашифровки модуля cripto к графическому интерфейсу
        text = window.get_text()
        decr_text = crp.get_decrypt(text, window.my_secret_key, window.my_n)
        window.pull_text(decr_text)


    def incoming_message(data):
        # Вывод входящего сообщения в графический интерфейс
        print('incoming <- ', data)
        window.add_msg_in_list('пришло <-' + data.decode("utf-8"))


    def send_msg(_, ):
        # Отправка сообщения
        text = window.get_text()
        print('send->', text)
        network2.tran_tcp(text, window.out_ip)


    def run_reader_thread(callback):
        '''
        Запускает отдельный поток, чтобы получать данные из сокета
        :param callback: функция, которая вызывается, если получены данные
        '''

        def reader():
            # функция чтения сообщения
            conn, out_addr = network1.my_socket.accept()
            while True:
                print('wait connect')
                try:
                    data = conn.recv(1024)
                    if data:
                        callback(data)
                    else:
                        break
                except :
                    pass
        # daemon=True, чтобы не зависал, если выйдет основной поток
        thread = threading.Thread(target=reader, daemon=True)
        thread.start()
        return thread


    my_id = random.getrandbits(64)
    window.my_id = my_id
    print('my ID: ', window.my_id)

    window.my_n, window.my_public_key, window.my_secret_key = crp.get_keys()
    print('my:', window.my_n, window.my_public_key, window.my_secret_key)
    window.create_widget()

    # Поиск в сети и обмен ключами с другим пользователем
    sr = Search(window.my_id, window.my_n, window.my_public_key).run()

    # Заполнение данных в графическом интерфейсе
    window.out_ip = sr[0][0]
    window.out_id, window.out_n, window.out_public_key = sr[1:]
    window.lb_out_ip.configure(text=f'Чужой IP:\n{window.out_ip}')
    window.lb_out_id.configure(text=f'Чужой ID:\n{window.out_id}')
    window.lb_out_n.configure(text=f'Чужой n:\n{window.out_n}')
    window.lb_out_public_key.configure(text=f'Чужой public_key:\n{window.out_public_key}')

    # Привязка кнопок к графическому интерфейсу
    window.btn_encrypt.bind('<ButtonPress-1>', enc)
    window.btn_decrypt.bind('<ButtonPress-1>', decr)
    window.btn_send.bind('<ButtonPress-1>', send_msg)

    # Распределение портов для передачи данных и прослушивания
    if window.my_id < window.out_id:
        port_no[0], port_no[1] = port_no[1], port_no[0]

    # Создание сокетов для входящих и исходящих подключений
    network1 = Networking('TCP', port_no=port_no[0])
    network2 = Networking('TCP', port_no=port_no[1])

    network1.bind(network1.my_address)
    network1.my_socket.listen()
    print(f"[*] Listening as {network1.my_address}:{network1.port_no}")

    network2.my_socket.connect((window.out_ip, network2.port_no))
    thread1 = run_reader_thread(incoming_message)

    # Вызов графического интерфейса
    window.call_gui()



if __name__ == '__main__':
    main()
