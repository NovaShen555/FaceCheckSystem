from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from cameraTestPy import Ui_Form

import cv2

class CameraPageWindow(QWidget,Ui_Form):
     returnSignal = pyqtSignal()
     def __init__(self,parent=None):
         print(1)
         super(CameraPageWindow, self).__init__(parent)
         print(2)
         self.timer_camera = QTimer() #初始化定时器
         self.cap = cv2.VideoCapture() #初始化摄像头
         self.CAM_NUM = 0
         self.setupUi(self)
         self.initUI()
         self.slot_init()
         print(3)
         self.openCamera()


     def initUI(self):
        self.setLayout(self.gridLayout)

     def slot_init(self):
         self.timer_camera.timeout.connect(self.show_camera)
         #信号和槽连接
         self.returnButton.clicked.connect(self.returnSignal)
         self.cameraButton.clicked.connect(self.slotCameraButton)

     def show_camera(self):
        flag,self.image = self.cap.read()
        show = cv2.resize(self.image,(480,320))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QImage(show.data, show.shape[1],show.shape[0],QImage.Format_RGB888)
        self.cameraLabel.setPixmap(QPixmap.fromImage(showImage))

     #打开摄像头
     def openCamera(self):
         flag = self.cap.open(self.CAM_NUM)
         if flag == False:
             msg = QMessageBox.Warning(self, u'Warning', u'请检测相机与电脑是否连接正确',
             buttons=QMessageBox.Ok,
             defaultButton=QMessageBox.Ok)
         else:
             self.timer_camera.start(30)

a=CameraPageWindow()
