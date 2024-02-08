import base64

import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap

from add_student import Ui_Dialog
from PyQt5.QtWidgets import QDialog
from cameraVideo import camera

class add_student_window(Ui_Dialog,QDialog):
    def __init__(self,list,parent=None):
        super(add_student_window,self).__init__(parent)
        self.setupUi(self)
        self.list=list#收取主界面传递过来的班级列表
        self.show_class()#将班级列表显示在下拉框中
        self.label.setScaledContents(True)#使得图像自适应
        self.label.setPixmap(QPixmap("./image/my.jpg"))
        self.cameravideo = camera()#导入相机函数
        self.time = QTimer()#启用定时器，实时显示人脸视频
        self.time.timeout.connect(self.show_camera)#计时器绑定画面显示函数
        self.time.start(50)#每隔50ms获取一次画面
        self.pushButton.clicked.connect(self.get_cameradata)#获取画面按钮事件绑定
        self.pushButton_2.clicked.connect(self.get_student_data)#点击确定，获取对应信息
        self.pushButton_3.clicked.connect(self.close_window)#点击关闭，窗口关闭
    def show_camera(self):
        # 获取摄像头数据
        pic = self.cameravideo.camera_to_pic()#获取一帧图像
        # 显示数据、显示画面
        self.label.setPixmap(pic)

    def get_cameradata(self):
        camera_data1 = self.cameravideo.read_camera()
        # 把摄像头画面转化为一张图片，然后设置编码为base64编码
        _, enc = cv2.imencode('.jpg', camera_data1)
        base64_image = base64.b64encode(enc.tobytes())
        self.base64_image=base64_image#全局变量，用于保存画面base64格式画面
        self.time.stop()#计时器停止
        self.cameravideo.colse_camera()#摄像机关闭
    def show_class(self):
        self.comboBox.clear()
        for i in self.list:
            self.comboBox.addItem(i)#将获取到的班级列表显示在下拉框中
    #获取学生基本信息
    def get_student_data(self):
        self.class_id=self.comboBox.currentText()#获取班级
        self.student_id=self.lineEdit.text()#获取学号
        self.student_name=self.lineEdit_2.text()#获取姓名
        self.accept()#点击确认后关闭对话框
    #关闭窗口
    def close_window(self):
        # 关闭对话框
        self.close()
