import sys
import IDEACrypt
import design
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication


class IDEACryptApp(QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.file = ""
        self.key = ""
        self.mode = True

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setWindowTitle("Успешно!")
        self.msg.result()

        self.error = QMessageBox()
        self.error.setIcon(QMessageBox.Critical)
        self.error.setWindowTitle("Ошибка!")

        #listeners
        self.file_load_button.clicked.connect(self.file_load_button_clicked)
        self.key_load_button.clicked.connect(self.key_load_button_clicked)
        self.pushButton.clicked.connect(self.run)
        self.progressBar.valueChanged.connect(self.pb_changed)
        self.encode_rb.toggled.connect(self.mode_toggled)
        self.msg.buttonClicked.connect(lambda: self.progressBar.setValue(0))
        self.error.buttonClicked.connect(lambda: self.progressBar.setValue(0))

    def file_load_button_clicked(self):
        #file dialog
        self.file_le.clear()
        self.file = QFileDialog.getOpenFileName(self.window(), "Выберите файл")[0]
        self.file_le.setText(self.file)

    def key_load_button_clicked(self):
        #file dialog
        self.key_le.clear()
        self.key = QFileDialog.getOpenFileName(self.window(), "Выберите файл ключа")[0]
        self.key_le.setText(self.key)

    def run(self):
        try:
            blocks = IDEACrypt.get_blocks_from_file(self.file)
            self.progressBar.setValue(0)
            keys = IDEACrypt.get_keys_from_file(self.key)
            self.progressBar.setValue(20)
            if self.mode:
                enblocks = IDEACrypt.crypt_blocks(blocks, keys[0])
                self.progressBar.setValue(40)
                deblocks = IDEACrypt.crypt_blocks(enblocks, keys[1])
                self.progressBar.setValue(60)

                if len(IDEACrypt.compare_colls(blocks, deblocks)) == 0:
                    newfile = self.file.replace('.', '.idea')
                    self.progressBar.setValue(80)
                    IDEACrypt.write_file_from_blocks(enblocks, newfile)
                    self.progressBar.setValue(100)
                    self.msg.setText("Файл зашифрован и сохранён как " + newfile)
                    self.msg.show()
                else:
                    self.error.setText('В процессе шифрования появились битые блоки. Используйте другой ключ!')
                    self.error.show()
            else:
                deblocks = IDEACrypt.crypt_blocks(blocks, keys[1])
                self.progressBar.setValue(49)
                IDEACrypt.write_file_from_blocks(deblocks, self.file)
                self.progressBar.setValue(60)
                newfile = self.file.replace('.idea', '.')
                self.progressBar.setValue(80)
                IDEACrypt.write_file_from_blocks(deblocks, newfile)
                self.progressBar.setValue(100)
                self.msg.setText("Файл расшифрован и сохранён как " + newfile)
                self.msg.show()
        except FileNotFoundError:
            self.error.setText('Файл не найден или не выбран!')
            self.error.show()

    def pb_changed(self):
        if self.progressBar.value() > 0:
            self.progressBar.setEnabled(True)
        else:
            self.progressBar.setEnabled(False)

    def mode_toggled(self):
        self.mode = True if self.encode_rb.isChecked() else False


#app execution
def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('res/icon.png'))
    window = IDEACryptApp()
    window.show()
    app.exec_()


#check for target of execution
if __name__ == "__main__":
    main()
