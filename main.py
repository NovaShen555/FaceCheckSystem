import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from function_window import function_window

if __name__ == '__main__':
    app =QApplication(sys.argv)
    widgets =QMainWindow()
    ui = function_window()
    ui.show()
    app.exec_()
    sys.exit(0)
