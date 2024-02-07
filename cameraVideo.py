'''
创建类对象
open函数完成摄像头的配置打开
'''
import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap


class camera():
    '''
    类初始化，相当于构造函数
    '''
    def __init__(self):
        self.open_camera()
    '''
        以下函数通过opencv打开笔记本电脑默认摄像头
    '''
    def open_camera(self):
        # 0表示内置默认摄像头,self.capture为全局变量
        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # isopend()函数返回一个布尔值，来判断是否打开摄像头
        if self.capture.isOpened():
            print("摄像头打开成功")
        # 定义一个多维数组，用来存储获取的画面数据
        self.currentframe = np.array([])

    '''
        获取摄像头数据
    '''
    def read_camera(self):
        ret,pic_data=self.capture.read()
        if not ret:
            print("获取摄像头数据失败")
            return None
        return pic_data

    '''
        摄像头图像格式转换
    '''
    def camera_to_pic(self):
        pic=self.read_camera()
        #摄像头是BGR转换为RGB
        self.currentframe=cv2.cvtColor(pic,cv2.COLOR_BGR2RGB)
        #设置宽高
        #self.currentframe=cv2.cvtColor(self.currentframe,(521,411))
        height,width=self.currentframe.shape[:2]
        #转换格式（界面能够显示的格式）
        #先转换为QImage图片（画面）
        #QImage(data,width,height,format)创建：数据、快读、高度、格式
        qimg=QImage(self.currentframe,width,height,QImage.Format_RGB888)
        qpix=QPixmap.fromImage(qimg)
        return qpix
    '''
        关闭摄像头
    '''
    def colse_camera(self):
        #释放摄像头
        self.capture.release()
