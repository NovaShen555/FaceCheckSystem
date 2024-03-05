import base64

import cv2
from PyQt5.QtCore import QTimer, QStringListModel
from PyQt5.QtGui import QPixmap

from add_student import Ui_Dialog
from PyQt5.QtWidgets import QDialog
from cameraVideo import camera

class add_student_window(Ui_Dialog,QDialog):
    def __init__(self,funC,list,parent=None):
        super(add_student_window,self).__init__(parent)
        self.setupUi(self)
        self.funC = funC#要用到上级函数
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
        self.comboBox_2.currentIndexChanged.connect(self.fresh_window)#下拉框事件绑定
        self.pushButton_4.clicked.connect(self.del_student)
        self.base64_image = ""

        self.fresh_window()#刷新窗口

    def del_student(self):
        self.funC.del_student_by_name(self.comboBox_2.currentText(),self.listView.selectionModel().selectedIndexes()[0].data())
        self.fresh_window()

    def fresh_window(self):
        # 将listView添加部分数据
        self.classList = self.funC.get_student_by_class(self.comboBox_2.currentText())
        listModel = QStringListModel()
        listModel.setStringList(self.classList)
        self.listView.setModel(listModel)


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
        self.comboBox_2.clear()
        for i in self.list:
            self.comboBox.addItem(i)#将获取到的班级列表显示在下拉框中
            self.comboBox_2.addItem(i)
    #获取学生基本信息
    def get_student_data(self):
        self.class_id=self.comboBox.currentText()#获取班级
        self.student_id=self.lineEdit.text()#获取学号
        self.student_name=self.lineEdit_2.text()#获取姓名
        if self.class_id=="" or self.student_id=="" or self.student_name=="" or self.base64_image=="":
            print("信息不完整")
            return
        self.funC.add_student_by_name(self.base64_image,self.class_id,self.student_id,self.student_name)
        self.fresh_window()

    def close_window(self):
        # 关闭对话框
        self.close()
