# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/mq/Projects/IDEACrypt/design.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(535, 166)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(6)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.file_le = QtWidgets.QLineEdit(self.centralwidget)
        self.file_le.setGeometry(QtCore.QRect(12, 10, 331, 21))
        self.file_le.setReadOnly(True)
        self.file_le.setObjectName("file_le")
        self.file_load_button = QtWidgets.QPushButton(self.centralwidget)
        self.file_load_button.setGeometry(QtCore.QRect(360, 10, 161, 25))
        self.file_load_button.setObjectName("file_load_button")
        self.key_load_button = QtWidgets.QPushButton(self.centralwidget)
        self.key_load_button.setGeometry(QtCore.QRect(360, 50, 161, 25))
        self.key_load_button.setObjectName("key_loda_button")
        self.key_le = QtWidgets.QLineEdit(self.centralwidget)
        self.key_le.setGeometry(QtCore.QRect(12, 50, 331, 21))
        self.key_le.setReadOnly(True)
        self.key_le.setObjectName("key_le")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 60, 251, 61))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.encode_rb = QtWidgets.QRadioButton(self.groupBox)
        self.encode_rb.setGeometry(QtCore.QRect(10, 30, 101, 20))
        self.encode_rb.setObjectName("encode_rb")
        self.encode_rb.setChecked(True)
        self.decode_rb = QtWidgets.QRadioButton(self.groupBox)
        self.decode_rb.setGeometry(QtCore.QRect(120, 30, 121, 20))
        self.decode_rb.setObjectName("decode_rb")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(False)
        self.progressBar.setGeometry(QtCore.QRect(10, 130, 511, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName("progressBar")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(270, 90, 251, 25))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "IDEACrypt"))
        self.file_load_button.setText(_translate("MainWindow", "Choose file"))
        self.key_load_button.setText(_translate("MainWindow", "Choose key"))
        self.encode_rb.setText(_translate("MainWindow", "Encryption"))
        self.decode_rb.setText(_translate("MainWindow", "Decryption"))
        self.pushButton.setText(_translate("MainWindow", "Run"))

