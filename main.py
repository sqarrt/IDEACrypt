import IDEACrypt
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


if __name__ == "__main__":
    window = Tk()
    window.geometry('370x150')
    window.title = "IDEA"
    lbl1 = Label(window, text = "Путь к исходному файлу")
    lbl2 = Label(window, text = "Путь к файлу ключа")
    entry1 = Entry(window, width = 50)
    entry2 = Entry(window, width = 50)
    var = IntVar(window, 0)
    chk = Checkbutton(window, text = "Расшифровка", variable = var)
    btn = Button(window, text = 'Запуск алгоритма')
    lbl1.grid(column = 0, row = 0)
    entry1.grid(column = 0, row = 1)
    lbl2.grid(column = 0, row = 2)
    entry2.grid(column = 0, row = 3)
    chk.grid(column = 0, row = 4)
    btn.grid(column = 0, row = 5)

    def entry1_clicked(event):
        entry1.insert(0, filedialog.askopenfilename() )

    def entry2_clicked(event):
        entry2.insert(0, filedialog.askopenfilename() )

    def chk_toggled(event):
        messagebox.showerror('TITLE', var.get())

    def btn_clicked(event):
        file = entry1.get()
        key = entry1.get()
        decode = var.get()
        if file != '' and key != '':
            keys = IDEACrypt.get_keys_from_file(key)
            blocks = IDEACrypt.get_blocks_from_file(file)
            keys = keys[0] if not decode else keys[1]
            cblocks = IDEACrypt.crypt_blocks(blocks, keys)
            IDEACrypt.write_file_from_blocks(cblocks, file+'_crypted')
        else:
            messagebox.showinfo("Ошибка!", "Введены не все данные")

    entry1.bind('<Button-1>', entry1_clicked)
    entry2.bind('<Button-1>', entry2_clicked)
    chk.bind('<Button-1>', chk_toggled)
    btn.bind('<Button-1>', btn_clicked)

    window.mainloop()
