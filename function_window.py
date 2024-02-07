import base64

from datetime import datetime

import cv2
import requests
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from cameraVideo import camera
from mainWindow import Ui_MainWindow
from detect import detect_thread
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
        self.access_token=self.get_accessToken()#获取Access_token访问令牌，并复制为全局变量
        self.start_state=True
    '''
        打开签到
    '''
    def open_Sign(self):
        if self.start_state==True:
            # 启动摄像头
            self.cameravideo = camera()
            # 启动定时器进行定时，每隔多长时间进行一次获取摄像头数据进行显示
            self.timeshow = QTimer(self)
            self.timeshow.start(30)
            # 每隔10毫秒产生一个信号timeout
            self.timeshow.timeout.connect(self.show_cameradata)
            self.detect = detect_thread(self.access_token)  # 创建线程
            self.detect.start()  # 启动线程
            # 签到1000毫秒获取一次,用来获取检测的画面
            self.faceshow = QTimer(self)
            self.faceshow.start(2000)
            self.faceshow.timeout.connect(self.get_cameradata)
            self.detect.transmit_data.connect(self.get_data)
            self.start_state=False
        else:
            QMessageBox.about(self, "提示", "正在检测，请先关闭！")

    '''
        关闭签到
    '''
    def close_Sign(self):
        if self.start_state==False:
            self.faceshow.stop()  # 计时器停止
            self.detect.ok = False  # 停止run函数运行
            self.detect.quit()  # 关闭线程
            # 关闭定时器，不再获取摄像头的数据
            self.timeshow.stop()
            self.timeshow.timeout.disconnect(self.show_cameradata)
            # 关闭摄像头
            self.cameravideo.colse_camera()
            self.start_state=True
            # 判断定时器是否关闭，关闭，则显示为自己设定的图像
            if self.timeshow.isActive() == False:
                self.label.setPixmap(QPixmap("image/1.jpg"))
                self.plainTextEdit_2.clear()
            else:
                QMessageBox.about(self, "警告", "关闭失败，存在部分没有关闭成功！")
        else:
            QMessageBox.about(self, "提示", "请先开始检测！")
    #获取人脸检测数据并显示到文本框中
    def get_data(self,data):
        if data['error_code']!=0:
            self.plainTextEdit_2.setPlainText(data['error_msg'])
            return
        elif data['error_msg'] == 'SUCCESS':
            self.plainTextEdit_2.clear()
            # 在data字典中键为result对应的值才是返回的检测结果
            face_num = data['result']['face_num']
            # print(face_num)
            if face_num == 0:
                self.plainTextEdit_2.setPlainText("当前没有人或人脸出现！")
                return
            else:
                self.plainTextEdit_2.clear()
                self.plainTextEdit_2.appendPlainText("检测到人脸！")
                self.plainTextEdit_2.appendPlainText("——————————————")
            # 人脸信息获取['result']['face_list']是列表，每个数据就是一个人脸信息，需要取出每个列表信息（0-i）
            for i in range(face_num):
                age = data['result']['face_list'][i]['age']  # 年龄
                # print(age)
                beauty = data['result']['face_list'][i]['beauty']  # 美观度
                gender = data['result']['face_list'][i]['gender']['type']  # 性别
                expression = data['result']['face_list'][i]['expression']['type']
                face_shape = data['result']['face_list'][i]['face_shape']['type']  # 脸型
                glasses = data['result']['face_list'][i]['glasses']['type']  # 是否戴眼镜
                emotion = data['result']['face_list'][i]['emotion']['type']  # 情绪
                mask = data['result']['face_list'][i]['mask']['type']  # 是否戴口罩
                # 往窗口中添加文本，参数就是需要的文本信息
                # print(age,gender,expression,beauty,face_shape,emotion,glasses,mask)
                self.plainTextEdit_2.appendPlainText("第" + str(i + 1) + "个学生人脸信息:")
                self.plainTextEdit_2.appendPlainText("——————————————")
                self.plainTextEdit_2.appendPlainText("年龄:" + str(age))
                if gender == 'male':
                    gender = "男"
                else:
                    gender = "女"
                self.plainTextEdit_2.appendPlainText("性别:" + str(gender))
                self.plainTextEdit_2.appendPlainText("表情:" + str(expression))
                self.plainTextEdit_2.appendPlainText("颜值分数:" + str(beauty))
                self.plainTextEdit_2.appendPlainText("脸型:" + str(face_shape))
                self.plainTextEdit_2.appendPlainText("情绪:" + str(emotion))
                if glasses == "none":
                    glasses="否"
                elif glasses == "common":
                    glasses="是:普通眼镜"
                else:
                    glasses="是:太阳镜"
                self.plainTextEdit_2.appendPlainText("是否佩戴眼镜:" + str(glasses))
                if mask == 0:
                    mask = "否"
                else:
                    mask = "是"
                self.plainTextEdit_2.appendPlainText("是否佩戴口罩:" + str(mask))
                self.plainTextEdit_2.appendPlainText("——————————————")
        else:
            print("人脸获取失败！")

    '''
        获取图像，并转换为base64格式
    '''
    def get_cameradata(self):
        # 输出当前时间，精确到毫秒
        print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        camera_data1 = self.cameravideo.read_camera()
        # 把摄像头画面转化为一张图片，然后设置编码为base64编码
        _, enc = cv2.imencode('.jpg', camera_data1)
        base64_image = base64.b64encode(enc.tobytes())
        #产生信号，传递数据
        self.detect.get_imgdata(base64_image)
    '''
        摄像头数据显示
    '''
    def show_cameradata(self):
        #获取摄像头数据
        pic=self.cameravideo.camera_to_pic()
        #在lebel框中显示数据、显示画面
        self.label.setPixmap(pic)

    '''
        获取Access_token访问令牌
    '''
    def get_accessToken(self):

        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=TKGXdKC7WPWeADGHmFBN8xAr&client_secret=lsr1tAuxv3tRGmOgZTGgNyri667dfKGg'
        # 进行网络请求，使用get函数
        response = requests.get(host)
        if response:
            data = response.json()
            self.access_token = data['access_token']
            print(self.access_token)
            return self.access_token
        else:
            QMessageBox(self,"提示","请检查网络连接！")
