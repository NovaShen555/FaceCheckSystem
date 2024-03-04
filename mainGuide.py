import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from function_window import function_window
from guide import Ui_MainWindow

class mainGuide(Ui_MainWindow,QMainWindow):

    def __init__(self):
        super(mainGuide,self).__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.startFaceCheck)
        self.pushButton_3.setText("开始11111打卡")

    def startFaceCheck(self):
        print("startFaceCheck")
        self.hide()
        funC.show()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        MainWindow.setWindowTitle("FaceCheckSystem")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widgets = QMainWindow()
    funC = function_window()
    ui = mainGuide()
    ui.show()
    app.exec_()
    sys.exit(0)
