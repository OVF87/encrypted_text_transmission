# Инициализация класса графического интерфейса

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from search import Search
from network import Networking
import variables as var
import random  # !!!!!!!!!!!!!!


class Gui:
    '''
    Класс создает графический интерфейс
    '''
    def __init__(self, my_ip=None):
        self.title='Передача зашифрованных файлов'
        self.my_ip = random.getrandbits(64) # !!!!!!!!!! my_ip
        self.out_ip = 0

        self.root = tk.Tk()
        self.root.title(self.title)

        self.root.main_menu = tk.Menu()
        self.root.file_menu = tk.Menu(tearoff=0)
        self.root.file_menu.add_command(label='New', command=self.new_text)
        self.root.file_menu.add_command(label='Save', command=self.save_file)
        self.root.file_menu.add_command(label='Open', command=self.open_file)
        self.root.file_menu.add_separator()
        self.root.file_menu.add_command(label='Exit', command=self.root.destroy)
        self.root.main_menu.add_cascade(label='File', menu=self.root.file_menu)
        self.root.main_menu.add_cascade(label='Help', command=self.get_help)

        self.root.rowconfigure(0, minsize=100, weight=1)
        self.root.columnconfigure(1, minsize=100, weight=1)

        self.root.btn_frame = tk.Frame(self.root, relief=tk.RAISED, bd=2)
        self.root.btn_frame.rowconfigure([i for i in range(14)], minsize=5)
        self.root.btn_frame.columnconfigure([i for i in range(3)], minsize=30)

        self.lb_top = tk.Label(self.root.btn_frame, text='Для поиска в локальной сети нажми search')
        self.lb_my_ip = tk.Label(self.root.btn_frame, text=f'Мой IP:\n{self.my_ip}')
        self.lb_out_ip = tk.Label(self.root.btn_frame, text=f'Чужой IP:\n{self.out_ip}')
        self.lb_info = tk.Label(self.root.btn_frame, text='...')

        self.btn_search = tk.Button(self.root.btn_frame, text='Поиск в локальной сети', command=self.search)
        self.btn_plug = tk.Button(self.root.btn_frame, text='Принять данные',command=self.get_receiving)
        self.btn_send = tk.Button(self.root.btn_frame, text='Отправить данные',command=self.get_send)
        self.btn_encypt = tk.Button(self.root.btn_frame, text='Зашифровать',)
        self.btn_decrypt = tk.Button(self.root.btn_frame, text='Расшифровать',)

        self.root.text_frame = tk.Frame(self.root, relief=tk.RAISED, bd=2)
        self.root.text_frame.rowconfigure([0, 1], minsize=50)
        self.root.text_frame.columnconfigure(0, minsize=50, weight=1)
        self.txt_edit = tk.Text(self.root.text_frame)
        self.lb_out_text = tk.Label(self.root.text_frame, text='...Здесь будет принятый текст...', bg='yellow')

    def call_gui(self):
        '''
        Вызов окна программы
        '''
        self.root.config(menu=self.root.main_menu)
        self.draw_widgets()
        self.root.mainloop()

    def draw_widgets(self):
        '''
        Прорисовка виджетов
        '''
        self.root.btn_frame.grid(row=0, column=0, sticky='nsew')

        self.lb_top.grid(row=0, column=1,  sticky='ew', padx=5)
        self.btn_search.grid(row=1, column=1, sticky='ew', padx=5)
        self.lb_my_ip.grid(row=2, column=0, sticky='ew', padx=5)
        self.lb_out_ip.grid(row=2, column=2, sticky='ew', padx=5)
        self.lb_info.grid(row=2, column=1, sticky='ew', padx=5)

        self.btn_plug.grid(row=2, column=1, sticky='ew', padx=5)
        self.btn_send.grid(row=3, column=1, sticky='ew', padx=5)
        self.btn_encypt.grid(row=6, column=1, sticky='ew', padx=5)
        self.btn_decrypt.grid(row=7, column=1, sticky='ew', padx=5)

        self.root.text_frame.grid(row=0, column=1, sticky='nsew')
        self.txt_edit.grid(row=0, column=0, sticky='nsew')
        self.lb_out_text.grid(row=1, column=0, sticky='nsew')

    def open_file(self):
        '''
        Открываем текстовый файл
        '''
        filepath = askopenfilename(
            filetypes = [('Текстовые файлы', '*.txt'), ('Все файлы', '*.*')])
        if not filepath:
            return
        self.txt_edit.delete('1.0', tk.END)
        with open(filepath, 'r') as input_file:
            text = input_file.read()
            self.txt_edit.insert(tk.END, text)
        self.root.title(self.title + f'\t - {filepath}')

    def save_file(self):
        '''
        Сохраняем текущий текстовый файл
        '''
        filepath = asksaveasfilename(
            defaultextension = 'txt',
            filetypes = [('Текстовые файлы', '*.txt'), ('Все файлы', '*.*')],)
        if not filepath:
            return
        with open(filepath, 'w') as output_file:
            text = self.txt_edit.get('1.0', tk.END)
            output_file.write(text)
        self.root.title(self.title + f'\t - {filepath}')

    def get_help(self):
        '''
        Вызов окна справки
        '''
        help_window = tk.Tk()
        help_window.title('Help')
        help_window.rowconfigure(0, minsize=100, weight=10)
        help_window.columnconfigure(0, minsize=100, weight=10)
        lb_help = tk.Label(help_window, text='blablabla')
        lb_help.grid()

    def new_text(self):
        '''
        Очистка поля ввода текста
        '''
        self.txt_edit.delete('1.0', tk.END)

    def search(self):
        '''
        Поиск другого экземпляра программы
        '''
        print('search is running')
        self.lb_info.configure(text='Поиск начат...')
        sr = Search(pid=self.my_ip).run()
        self.lb_out_ip.configure(text=f'Чужой IP:\n{sr[1]}')
        self.out_ip = sr[1]
        print('out ip: ', self.out_ip)
        self.lb_info.configure(text='...')

    def get_receiving(self):
        '''
        Прием данных
        '''
        print('Прием данных...')
        self.lb_info.configure(text='Прием данных...')
        connect = Networking('TCP')

        data = connect.receive_data()
        self.txt_edit.insert('1.0', data)
        self.lb_info.configure(text='...')

    def get_send(self, ):
        '''
        Отправка данных
        '''
        print('data send')
        self.lb_info.configure(text='Передача данных...')
        temp = self.txt_edit.get('1.0', tk.END)
        print(temp)
        connect = Networking('TCP')
        connect.send_data(temp.encode())
        self.lb_info.configure(text='...')

    def get_encrypt(self):
        '''
        Шифрование данных
        '''
        pass

    def get_decrypt(self):
        '''
        Расшифровка данных
        '''
        pass






if __name__ == '__main__':
    window = Gui()
    window.call_gui()# Напишите здесь свой код :-)
