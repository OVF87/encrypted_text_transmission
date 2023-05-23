# Инициализация класса графического интерфейса
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import variables as var



class Gui:
    '''
    Класс создает графический интерфейс
    '''
    def __init__(self, my_ip=None):
        self.title='Передача зашифрованного текста'
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

    def add_msg_in_list(self, text: str):
        self.msg_list.configure(state='normal')
        self.msg_list.insert(tk.END, '\n')
        self.msg_list.insert(tk.END, text)
        self.msg_list.configure(state='disabled')

    def call_gui(self):
        '''
        Вызов окна программы
        '''
        self.create_menu()
        self.draw_widgets()
        self.root.mainloop()

    def create_menu(self):
        '''
        Создание меню
        '''
        self.root.main_menu = tk.Menu()
        self.root.file_menu = tk.Menu(tearoff=0)
        self.root.file_menu.add_command(label='Очистить текстовые поля', command=self.new_text)
        self.root.file_menu.add_command(label='Сохранить в текстовый файл', command=self.save_file)
        self.root.file_menu.add_command(label='Открыть текстовый файл', command=self.open_file)
        self.root.file_menu.add_separator()
        self.root.file_menu.add_command(label='Выход', command=self.root.destroy)
        self.root.main_menu.add_cascade(label='Меню', menu=self.root.file_menu)
        self.root.main_menu.add_cascade(label='Помощь', command=self.get_help)
        self.root.config(menu=self.root.main_menu)

    def create_widget(self):
        '''
        Создает виджеты кнопок, информации, текстовые поля
        '''
        #  Конфигурация основного окна
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        #  Создание и конфигурация рамки для текстовых меток
        self.root.info_frame = tk.Frame(self.root, relief=tk.RAISED, bd=2)
        self.root.info_frame.rowconfigure([i for i in range(14)], minsize=20)
        self.root.info_frame.columnconfigure(0, minsize=30)

        #  Создание текстовых меток о своей информации
        self.lb_my_ip = tk.Label(self.root.info_frame, text=f'Мой IP:\n{self.my_ip}')
        self.lb_my_id = tk.Label(self.root.info_frame, text=f'Мой ID:\n{self.my_id}')
        self.lb_my_n = tk.Label(self.root.info_frame, text=f'Мой n:\n{self.my_n}')
        self.lb_my_public_key = tk.Label(self.root.info_frame, text=f'Мой Public key:\n{self.my_public_key}')
        self.lb_my_secret_key = tk.Label(self.root.info_frame, text=f'Мой Secret key:\n{self.my_secret_key}')

        #  Создание текстовых меток о чужой информации
        self.lb_out_ip = tk.Label(self.root.info_frame, text=f'Чужой IP:\n{self.out_ip}')
        self.lb_out_id = tk.Label(self.root.info_frame, text=f'Чужой ID:\n{self.out_id}')
        self.lb_out_n = tk.Label(self.root.info_frame, text=f'Чужой n:\n{self.out_n}')
        self.lb_out_public_key = tk.Label(self.root.info_frame, text=f'Чужой Public key:\n{self.out_public_key}')

        #  Создание текстовых полей
        self.root.text_frame = tk.Frame(self.root, relief=tk.RAISED, bd=2)
        self.root.text_frame.rowconfigure(0, weight=1)
        self.root.text_frame.columnconfigure(0, weight=1)
        self.root.text_frame.rowconfigure([0, 1, 2], minsize=20)
        self.root.text_frame.columnconfigure([0, 1], minsize=5)
        self.msg_list = tk.Text(self.root.text_frame, height=20, width=30, wrap="char", state='disabled')
        self.y_scrollbar_msg_list = tk.Scrollbar(self.root.text_frame, command=self.msg_list.yview)
        self.msg_list.configure(yscrollcommand=self.y_scrollbar_msg_list.set)
        self.scrollbar_text_edit = tk.Scrollbar(self.root.text_frame)
        self.txt_edit = tk.Text(self.root.text_frame, yscrollcommand=self.scrollbar_text_edit.set)

        #  Создание кнопоки
        self.btn_send = tk.Button(self.root.text_frame, text='Отправить данные')



    def draw_widgets(self):
        '''
        Размещает виджеты
        '''
        #  Рамка информации
        self.root.info_frame.grid(row=0, column=0, sticky='nsew')

        #  Текстовые метки своей информации
        self.lb_my_id.grid(row=1, column=0, sticky='ew', padx=5)
        self.lb_my_ip.grid(row=2, column=0, sticky='ew', padx=5)
        self.lb_my_n.grid(row=3, column=0, sticky='ew', padx=5)
        self.lb_my_public_key.grid(row=4, column=0, sticky='ew', padx=5)
        self.lb_my_secret_key.grid(row=5, column=0, sticky='ew', padx=5)

        #  Текстовые метки чужой информации
        self.lb_out_id.grid(row=7, column=0, sticky='ew', padx=5)
        self.lb_out_ip.grid(row=8, column=0, sticky='ew', padx=5)
        self.lb_out_n.grid(row=9, column=0, sticky='ew', padx=5)
        self.lb_out_public_key.grid(row=10, column=0, sticky='ew', padx=5)

        #  Виджеты кнопок
        self.btn_send.grid(row=2, column=0, sticky='nsew', padx=5)

        #  Виджеты тектовых полей
        self.root.text_frame.grid(row=0, column=1, sticky='nsew')
        self.y_scrollbar_msg_list.grid(row=0, column=1, sticky='ns')
        self.msg_list.grid(row=0, column=0, sticky='nsew')
        self.scrollbar_text_edit.grid(row=1, column=1, sticky='ns')
        self.txt_edit.grid(row=1, column=0, sticky='nsew')

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

    def get_text(self) -> str:
        text = self.txt_edit.get('1.0', tk.END)
        return text

    def new_text(self, all = 1):
        '''
        Очистка текстовых полей
        :param all: если True очистка поля ввода текста и истории сообщений,
        если False очистка только поля ввода
        '''
        self.txt_edit.delete('1.0', tk.END)
        if all:
            self.msg_list.configure(state='normal')
            self.msg_list.delete('1.0', tk.END)
            self.msg_list.configure(state='disabled')        

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
            text = self.msg_list.get('1.0', tk.END)
            output_file.write(text)
        self.root.title(self.title + f'\t - {filepath}')


if __name__ == '__main__':
    window = Gui()
    window.create_widget()
    window.call_gui()
