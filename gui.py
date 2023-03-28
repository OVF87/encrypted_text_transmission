# Инициализация класса графического интерфейса
import random  # !!!!!!!!!!!!!!
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import variables as var



class Gui:
    '''
    Класс создает графический интерфейс
    '''
    def __init__(self, my_ip=None):
        self.title='Передача зашифрованных файлов'
        self.my_id = None
        self.my_ip = var.MY_ADDRESS
        self.out_id = None
        self.out_ip = None
        self.my_n = None
        self.my_public_key = None
        self.my_secret_key = None
        self.out_n = None
        self.out_public_key = None
        self.root = tk.Tk()
        self.root.title(self.title)

    def create_menu(self):
        '''
        Создание меню
        '''
        self.root.main_menu = tk.Menu()
        self.root.file_menu = tk.Menu(tearoff=0)
        self.root.file_menu.add_command(label='New', command=self.new_text)
        self.root.file_menu.add_command(label='Save', command=self.save_file)
        self.root.file_menu.add_command(label='Open', command=self.open_file)
        self.root.file_menu.add_separator()
        self.root.file_menu.add_command(label='Exit', command=self.root.destroy)
        self.root.main_menu.add_cascade(label='File', menu=self.root.file_menu)
        self.root.main_menu.add_cascade(label='Help', command=self.get_help)
        self.root.config(menu=self.root.main_menu)

    def create_widget(self):
        '''
        Создает виджеты кнопок, информации, текстовые поля
        '''
        #  Создание и конфигурация рамки для виджетов кнопок и текстовых меток
        self.root.btn_frame = tk.Frame(self.root, relief=tk.RAISED, bd=2)
        self.root.btn_frame.rowconfigure([i for i in range(14)], minsize=5)
        self.root.btn_frame.columnconfigure([i for i in range(3)], minsize=30)

        #  Создание текстовых меток о своей информации
        self.lb_my_ip = tk.Label(self.root.btn_frame, text=f'Мой IP:\n{self.my_ip}')
        self.lb_my_id = tk.Label(self.root.btn_frame, text=f'Мой ID:\n{self.my_id}')
        self.lb_my_n = tk.Label(self.root.btn_frame, text=f'Мой n:\n{self.my_n}')
        self.lb_my_public_key = tk.Label(self.root.btn_frame, text=f'Мой public_key:\n{self.my_public_key}')
        self.lb_my_secret_key = tk.Label(self.root.btn_frame, text=f'Мой secret_key:\n{self.my_secret_key}')

        #  Создание текстовых меток о чужой информации
        self.lb_out_ip = tk.Label(self.root.btn_frame, text=f'Чужой IP:\n{self.out_ip}')
        self.lb_out_id = tk.Label(self.root.btn_frame, text=f'Чужой ID:\n{self.out_id}')
        self.lb_out_n = tk.Label(self.root.btn_frame, text=f'Чужой n:\n{self.out_n}')
        self.lb_out_public_key = tk.Label(self.root.btn_frame, text=f'Чужой public_key:\n{self.out_public_key}')

        #  Создание кнопок
        self.btn_send = tk.Button(self.root.btn_frame, text='Отправить данные')#, command=self.get_send)
        self.btn_encrypt = tk.Button(self.root.btn_frame, text='Зашифровать')
        self.btn_decrypt = tk.Button(self.root.btn_frame, text='Расшифровать')

        #  Создание текстовых полей
        self.root.text_frame = tk.Frame(self.root, relief=tk.RAISED, bd=2)
        self.root.text_frame.rowconfigure([0, 1, 2], minsize=20)
        self.root.text_frame.columnconfigure(0, minsize=20, weight=1)
        self.msg_list = tk.Listbox(self.root.text_frame, height=20, width=30)
        self.y_scrollbar_msg_list = tk.Scrollbar(self.root.text_frame, command=self.msg_list.yview)
        self.x_scrollbar_msg_list = tk.Scrollbar(self.root.text_frame, orient="horizontal", command=self.msg_list.xview)
        self.msg_list.configure(xscrollcommand=self.x_scrollbar_msg_list.set,  yscrollcommand=self.y_scrollbar_msg_list.set)
        self.scrollbar_text_edit = tk.Scrollbar(self.root.text_frame)
        self.txt_edit = tk.Text(self.root.text_frame, yscrollcommand=self.scrollbar_text_edit.set)
        self.lb_out_text = tk.Label(self.root.text_frame, text='...Здесь будет принятый текст...', bg='yellow')

    def call_gui(self):
        '''
        Вызов окна программы
        '''

        self.create_menu()
        #self.create_widget()
        self.draw_widgets()
        self.root.mainloop()

    def draw_widgets(self):
        '''
        Размещает виджеты
        '''
        #  Рамка кнопок
        self.root.btn_frame.grid(row=0, column=0, sticky='nsew')

        #  Текстовые метки своей информации
        self.lb_my_id.grid(row=1, column=0, sticky='ew', padx=5)
        self.lb_my_ip.grid(row=2, column=0, sticky='ew', padx=5)
        self.lb_my_n.grid(row=3, column=0, sticky='ew', padx=5)
        self.lb_my_public_key.grid(row=4, column=0, sticky='ew', padx=5)
        self.lb_my_secret_key.grid(row=5, column=0, sticky='ew', padx=5)

        #  Текстовые метки чужой информации
        self.lb_out_id.grid(row=1, column=2, sticky='ew', padx=5)
        self.lb_out_ip.grid(row=2, column=2, sticky='ew', padx=5)
        self.lb_out_n.grid(row=3, column=2, sticky='ew', padx=5)
        self.lb_out_public_key.grid(row=4, column=2, sticky='ew', padx=5)

        #  Виджеты кнопок
        self.btn_send.grid(row=3, column=1, sticky='ew', padx=5)
        self.btn_encrypt.grid(row=6, column=1, sticky='ew', padx=5)
        self.btn_decrypt.grid(row=7, column=1, sticky='ew', padx=5)

        #  Виджеты тектовых полей
        self.root.text_frame.grid(row=0, column=1, sticky='nsew')
        self.y_scrollbar_msg_list.grid(row=0, column=2, sticky='ns')
        self.x_scrollbar_msg_list.grid(row=1, column=0, sticky='sew')
        self.msg_list.grid(row=0, column=0, sticky='nsew')
        self.scrollbar_text_edit.grid(row=2, column=2, sticky='ns')
        self.txt_edit.grid(row=3, column=0, sticky='nsew')
        self.lb_out_text.grid(row=2, column=0, sticky='nsew')

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

    def get_out_data(self):
        pass

    def get_receiving(self):
        '''
        Прием данных
        '''
        print('Прием данных...')
        self.lb_info.configure(text='Прием данных...')
        connect = Networking('TCP')

        data = connect.receive_data()
        self.lb_out_text.configure(text=data)
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
    """
    def get_encrypt(self):
        '''
        Шифрование данных
        '''
        self.lb_info.configure(text='Шифрование данных...')
        print('encrypt is running')
        text = self.txt_edit.get('1.0', tk.END)
        text = self.crp.get_encrypt(text, self.my_secret_key, self.my_n)
        self.txt_edit.delete('1.0', tk.END)
        self.txt_edit.insert(tk.END, text)
        print(text)
        self.lb_info.configure(text='...')

    def get_decrypt(self):
        '''
        Расшифровка данных
        '''
        print('decrypt is running')
        self.lb_info.configure(text='Дешифровка данных...')
        text = self.lb_out_text.cget('text')
        text = self.crp.get_decrypt(text, self.out_public_key, self.out_n)
        self.lb_out_text.configure(text=text)
        print(text)
        self.lb_info.configure(text='...')
    """
    def get_text(self) -> str:
        text = self.txt_edit.get('1.0', tk.END)
        return text

    def pull_text(self, text: str):
        self.txt_edit.delete('1.0', tk.END)
        self.txt_edit.insert(tk.END, text)

    def add_msg_in_list(self, text: str):
        self.msg_list.insert(tk.END, text)


if __name__ == '__main__':
    window = Gui()
    window.create_widget()
    window.call_gui()
