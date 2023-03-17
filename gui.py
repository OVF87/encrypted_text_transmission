# Инициализация класса графического интерфейса

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename


class Gui:
    '''Класс создает графический интерфейс'''
    def __init__(self, title='Передача зашифрованных файлов', my_ip=None):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.main_menu = tk.Menu()
        self.root.file_menu = tk.Menu(tearoff=0)
        self.root.file_menu.add_command(label="New", command=self.new_text)
        self.root.file_menu.add_command(label="Save", command=self.save_file)
        self.root.file_menu.add_command(label="Open", command=self.open_file)
        self.root.file_menu.add_separator()
        self.root.file_menu.add_command(label="Exit")

        self.root.main_menu.add_cascade(label="File", menu=self.root.file_menu)
        self.root.main_menu.add_cascade(label="Help")




        self.my_ip = my_ip
        self.out_ip = 0

        self.root.rowconfigure(0, minsize=100, weight=10)
        self.root.columnconfigure([0, 1], minsize=100, weight=10)

        self.root.btn_frame = tk.Frame(self.root, relief=tk.RAISED, bd=2)
        self.root.btn_frame.rowconfigure([i for i in range(14)], minsize=5, weight=10)
        self.root.btn_frame.columnconfigure([i for i in range(3)], minsize=50, weight=10)

        self.lb_top = tk.Label(self.root.btn_frame, text='Для поиска в локальной сети нажми search')
        self.lb_my_ip = tk.Label(self.root.btn_frame, text=f'Мой IP:\n{self.my_ip}')
        self.lb_out_ip = tk.Label(self.root.btn_frame, text=f'out IP:\n{self.out_ip}')
        self.lb_info = tk.Label(self.root.btn_frame, text='')

        self.btn_search = tk.Button(self.root.btn_frame, text='Поиск в локальной сети', command=self.search)
        self.btn_plug = tk.Button(self.root.btn_frame, text='Принять данные',)
        self.btn_send = tk.Button(self.root.btn_frame, text='Отправить данные',)
        self.btn_encypt = tk.Button(self.root.btn_frame, text='Зашифровать',)
        self.btn_decrypt = tk.Button(self.root.btn_frame, text='Расшифровать',)

        self.txt_edit = tk.Text(self.root)
        self.lb_out_text = tk.Label(self.root, text=None, bg='yellow')

    def call_gui(self):
        '''Вызов окна программы'''
        self.root.config(menu=self.root.main_menu)
        self.draw_widgets()
        self.root.mainloop()

    def draw_widgets(self):
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

        self.txt_edit.grid(row=0, column=1, sticky='ew')
        self.lb_out_text.grid(row=1, column=1,sticky='n')

    def open_file(self):
        '''Открываем файл для редактирования'''
        filepath = askopenfilename(
            filetypes = [('Текстовые файлы', '*.txt'), ('Все файлы', '*.*')])
        if not filepath:
            return
        self.txt_edit.delete('1.0', tk.END)
        with open(filepath, 'r') as input_file:
            text = input_file.read()
            self.txt_edit.insert(tk.END, text)
        self.root.title(f'file - {filepath}')

    def save_file(self):
        '''Сохраняем текущий файл как новый файл'''
        filepath = asksaveasfilename(
            defaultextension = 'txt',
            filetypes = [('Текстовые файлы', '*.txt'), ('Все файлы', '*.*')],)
        if not filepath:
            return
        with open(filepath, 'w') as output_file:
            text = self.txt_edit.get('1.0', tk.END)
            output_file.write(text)
        self.root.title(f'текстовый редактор - {filepath}')

    def new_text(self):
        self.txt_edit.delete('1.0', tk.END)

    def search(self):
        pass

    def plug(self):
        pass

    def send(self, ):
        pass

    def encrypt(self):
        pass

    def decrypt(self):
        pass






if __name__ == '__main__':
    window = Gui()
    window.call_gui()# Напишите здесь свой код :-)
