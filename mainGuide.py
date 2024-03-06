import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from function_window import function_window
from guide import Ui_MainWindow
import classManage_window
from searchData_window import searchData_window


class mainGuide(Ui_MainWindow,QMainWindow):

    def __init__(self):
        super(mainGuide,self).__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.startFaceCheck)
        self.pushButton.clicked.connect(self.addStu)
        self.pushButton_2.clicked.connect(self.classManage)
        self.pushButton_4.clicked.connect(self.searchData)

    def searchData(self):
        print("searchData")
        sD.show()

    def classManage(self):
        print("classManage")
        clM.show()

    def addStu(self):
        print("addStu")
        funC.add_student()

    def startFaceCheck(self):
        print("startFaceCheck")
        funC.show()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        MainWindow.setWindowTitle("FaceCheckSystem")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widgets = QMainWindow()
    funC = function_window()
    clM = classManage_window.classManager(funC)
    sD = searchData_window()
    ui = mainGuide()
    ui.show()
    app.exec_()
    sys.exit(0)
