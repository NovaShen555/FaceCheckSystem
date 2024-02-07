from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from cameraVideo import camera
from mainWindow import Ui_MainWindow
class function_window(Ui_MainWindow,QMainWindow):
    '''
    初始化函数
    '''
    def __init__(self):
        super(function_window, self).__init__()
        self.setupUi(self)
        self.label.setScaledContents(True)#设置图像自适应label显示框
        self.pushButton.clicked.connect(self.open_Sign)#打开签到事件绑定
        self.pushButton_2.clicked.connect(self.close_Sign)#关闭签到事件绑定
        self.cameraStatus = False
    '''
        打开签到
    '''
    def open_Sign(self):
        if self.cameraStatus == True:
            return None
        self.cameraStatus = True
        #启动摄像头
        self.cameravideo = camera()
        # 启动定时器进行定时，每隔多长时间进行一次获取摄像头数据进行显示
        self.timeshow = QTimer(self)
        self.timeshow.start(10)
        # 每隔10毫秒产生一个信号timeout
        self.timeshow.timeout.connect(self.show_cameradata)
    '''
        摄像头数据显示
    '''
    def show_cameradata(self):
        #获取摄像头数据
        pic=self.cameravideo.camera_to_pic()
        #在lebel框中显示数据、显示画面
        self.label.setPixmap(pic)
    '''
        关闭签到
    '''
    def close_Sign(self):
        if self.cameraStatus == False:
            return None
        self.cameraStatus = False
        #关闭定时器，不再获取摄像头的数据
        self.timeshow.stop()
        self.timeshow.timeout.disconnect(self.show_cameradata)
        # 关闭摄像头
        self.cameravideo.colse_camera()
        #判断定时器是否关闭，关闭，则显示为自己设定的图像
        if self.timeshow.isActive() == False:
            self.label.setPixmap(QPixmap("./1.jpg"))
        else:
            QMessageBox.about(self,"警告","关闭失败，存在部分没有关闭成功！")
