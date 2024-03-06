import pickle

from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem, QMainWindow

from punchData import punchData
from searchData import Ui_MainWindow

class searchData_window(Ui_MainWindow,QMainWindow):

    def show(self):
        super().show()
        # 读取持久化的数据
        f = open("pickle.pickle", 'rb')
        unpickler = pickle.Unpickler(f)
        self.sign_data = unpickler.load()
        f.close()
        print(self.sign_data)

        for i in self.sign_data:
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(i.user_id))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(i.user_info))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(i.group_id))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(i.datetime))
            self.tableWidget.resizeColumnToContents(4)

    def __init__(self):
        super(searchData_window,self).__init__()
        self.setupUi(self)
        self.sign_data:list[punchData] = []
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可更改
        # 设置表格为指定长度
        self.tableWidget.setColumnWidth(0, 130)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.tableWidget.setColumnWidth(1, 85)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.tableWidget.setColumnWidth(2, 85)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.tableWidget.setColumnWidth(3, 280)

        # 读取持久化的数据
        f = open("pickle.pickle", 'rb')
        unpickler = pickle.Unpickler(f)
        self.sign_data = unpickler.load()
        f.close()
        print(self.sign_data)

        for i in self.sign_data:
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(i.user_id))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(i.user_info))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(i.group_id))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(i.datetime))
            self.tableWidget.resizeColumnToContents(4)

        self.pushButton.clicked.connect(self.searchStu)

    def searchStu(self):
        print("searchStu")
        self.tableWidget.setRowCount(0)
        for i in self.sign_data:
            if i.user_id == self.textEdit.toPlainText():
                row = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row)
                self.tableWidget.setItem(row, 0, QTableWidgetItem(i.user_id))
                self.tableWidget.setItem(row, 1, QTableWidgetItem(i.user_info))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(i.group_id))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(i.datetime))
        self.textEdit.clear()
