from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView

import classManage


class classManager(classManage.Ui_MainWindow, QMainWindow):
    def __init__(self,funC):
        super(classManager, self).__init__()
        self.setupUi(self)
        self.funC = funC
        # 将listView添加部分数据
        self.classList = self.funC.get_class()['result']['group_id_list']
        listModel = QStringListModel()
        listModel.setStringList(self.classList)
        self.listView.setModel(listModel)
        # 禁止编辑
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 点击list方法
        self.listView.clicked.connect(self.onClickedListView)
        self.nowSelect = ""
        # 绑定deleteclass方法
        self.pushButton_2.clicked.connect(self.deleteClass)
        # 绑定addclass方法
        self.pushButton.clicked.connect(self.addClass)

    def flashWindow(self):
        # 将listView添加部分数据
        self.classList = self.funC.get_class()['result']['group_id_list']
        listModel = QStringListModel()
        listModel.setStringList(self.classList)
        self.listView.setModel(listModel)

    def onClickedListView(self,item):
        print("Now choose "+self.classList[item.row()])
        self.nowSelect = self.classList[item.row()]

    def deleteClass(self):
        self.funC.delete_class_by_name(self.nowSelect)
        self.flashWindow()

    def addClass(self):
        print("Add class by name "+self.textEdit.toPlainText())
        self.funC.add_class_by_name(self.textEdit.toPlainText())
        self.flashWindow()
