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
    def enc(data: str) -> str:
        '''
        Зашифровка сообщения
        :param data: текст сообщения
        '''
        enc_text = crp.get_encrypt(data, window.out_public_key, window.out_n)
        return enc_text


    def incoming_message(data):
        '''
        Вывод зашифрованого и расшифрованого 
        входящего сообщения в графический интерфейс
        :param data: текст сообщения
        '''        
        data = data.decode("utf-8")
        window.add_msg_in_list('Зашифровано <<<')
        window.add_msg_in_list(data)
        window.add_msg_in_list('Расшифровано <<<:')
        window.add_msg_in_list(crp.get_decrypt(data, window.my_secret_key, window.my_n))

    def run_reader_thread(callback):
        '''
        Запускает отдельный поток, чтобы получать данные из сокета
        :param callback: функция, которая вызывается, если получены данные
        '''
        def reader():
            temp =b''
            print('wait connect')
            try:
                conn, out_addr = network1.my_socket.accept()
                print('recv data ...')
                while True:
                    chunk = conn.recv(var.BUFFER_SIZE)
                    if b'EOF' == chunk:
                        callback(temp)
                        temp =b''
                    else:
                        temp += chunk
            except:
                pass
        # daemon=True, чтобы не зависал, если выйдет основной поток
        thread = threading.Thread(target=reader, daemon=True)
        thread.start()
        return thread

    def send_msg(self):
        '''
        Шифрование и отправка сообщения
        '''
        text = window.get_text()
        window.add_msg_in_list('Исходный текст:')
        window.add_msg_in_list(text)
        crp_text = crp.get_encrypt(text, window.out_public_key, window.out_n)
        window.add_msg_in_list('Зашифровано >>>')
        window.add_msg_in_list(crp_text)
        print('send->', crp_text)
        network2.tran_tcp(crp_text, window.out_ip)
        window.new_text(0)


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

    # Привязка кнопки к графическому интерфейсу
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

    # Закрытие сокетов
    network1.my_socket.close()
    network2.my_socket.close()

if __name__ == '__main__':
    main()
