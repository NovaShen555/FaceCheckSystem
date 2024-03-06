import base64
import os
import pickle
import time

import cv2
import requests
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog, QAbstractItemView, QHeaderView, QTableWidgetItem
from cameraVideo import camera
from find_information_window import find_information_window
from main import Ui_MainWindow
from detect import detect_thread
from add_student_window import add_student_window
from del_student_window import del_student_window
from punchData import punchData


class function_window(Ui_MainWindow, QMainWindow):
    '''
    初始化函数
    '''

    def __init__(self):
        super(function_window, self).__init__()
        self.setupUi(self)
        self.label.setScaledContents(True)  # 设置图像自适应label显示框
        self.pushButton.clicked.connect(self.open_Sign)  # 打开签到事件绑定
        self.pushButton_2.clicked.connect(self.close_Sign)  # 关闭签到事件绑定
        # self.actionaddclass.triggered.connect(self.add_class)  # 添加班级按钮事件绑定
        # self.actionfindclass.triggered.connect(self.display_class)  # 查询班级按钮事件绑定
        # self.actiondelclass.triggered.connect(self.delete_calss)  # 删除班级按钮事件绑定
        # self.actionaddStu.triggered.connect(self.add_student)  # 增加学生人脸信息事件绑定
        # self.actiondelStu.triggered.connect(self.del_student)  # 删除学生人脸信息事件绑定
        # self.actionfindStu.triggered.connect(self.search_student)  # 学生信息查询事件绑定
        self.access_token = self.get_accessToken()  # 获取Access_token访问令牌，并复制为全局变量
        self.start_state = True

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可更改
        # 设置表格为指定长度
        self.tableWidget.setColumnWidth(0, 55)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.tableWidget.setColumnWidth(1, 25)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.tableWidget.setColumnWidth(2, 25)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.tableWidget.setColumnWidth(3, 90)
        # update: 2024-2-13
        # 新增表格列展示签到统计

        self.fresh_window()
        # update: 2024-2-13
        # 新增班级选择

    def show(self):
        self.fresh_window()
        super().show()


    '''
        刷新窗口，重新获取班级数据
    '''
    def fresh_window(self):
        list = self.get_class()['result']['group_id_list']
        self.comboBox.clear()
        for i in list:
            self.comboBox.addItem(i)  # 将获取到的班级列表显示在下拉框中

    '''
        打开签到
    '''

    def open_Sign(self):
        if self.start_state == True:
            # 启动摄像头
            self.cameravideo = camera()
            # 启动定时器进行定时，每隔多长时间进行一次获取摄像头数据进行显示
            self.timeshow = QTimer(self)
            self.timeshow.start(10)
            # 每隔10毫秒产生一个信号timeout
            self.timeshow.timeout.connect(self.show_cameradata)
            self.detect = detect_thread(self.access_token)  # 创建线程
            self.detect.start()  # 启动线程
            # 签到500毫秒获取一次,用来获取检测的画面
            self.faceshow = QTimer(self)
            self.faceshow.start(500)
            self.faceshow.timeout.connect(self.get_cameradata)
            # self.detect.transmit_data.connect(self.get_data)
            # update: 2024-2-13
            # 不再返回人脸的检测结果
            self.detect.transmit_data1.connect(self.get_seach_data)
            self.start_state = False
        else:
            QMessageBox.about(self, "提示", "正在检测，请先关闭！")

    '''
        关闭签到
    '''

    def close_Sign(self):
        if self.start_state == False:
            self.faceshow.stop()  # 计时器停止
            self.detect.ok = False  # 停止run函数运行
            self.detect.quit()  # 关闭线程
            # 关闭定时器，不再获取摄像头的数据
            self.timeshow.stop()
            self.timeshow.timeout.disconnect(self.show_cameradata)
            # 关闭摄像头
            self.cameravideo.colse_camera()
            self.start_state = True
            # 显示本次签到情况，弹出弹窗
            self.sign = find_information_window(self.detect.sign_data_list, self)  # 传递数据暂时为空
            self.sign.exec_()

            # 判断定时器是否关闭，关闭，则显示为自己设定的图像
            if self.timeshow.isActive() == False:
                self.label.setPixmap(QPixmap("1.jpg"))
            else:
                QMessageBox.about(self, "警告", "关闭失败，存在部分没有关闭成功！")

            # 将数据持久化
            objFromPickle:list[punchData] = []
            try:
                if os.path.getsize("pickle.pickle") > 0:
                    with open("pickle.pickle", "rb") as f:
                        unpickler = pickle.Unpickler(f)
                        objFromPickle = unpickler.load()
            finally:
                f = open("pickle.pickle", 'wb')
                for i in self.detect.store_data:
                    objFromPickle.append(i)
                print(objFromPickle)
                pickle.dump(objFromPickle, f)
                f.close()

        else:
            QMessageBox.about(self, "提示", "请先开始检测！")


    '''
        获取图像，并转换为base64格式
    '''

    def get_cameradata(self):
        camera_data1 = self.cameravideo.read_camera()
        # 把摄像头画面转化为一张图片，然后设置编码为base64编码
        _, enc = cv2.imencode('.jpg', camera_data1)
        base64_image = base64.b64encode(enc.tobytes())
        currentClass = self.comboBox.currentText()
        # 产生信号，传递数据
        self.detect.get_imgdata(base64_image,currentClass)

    '''
        摄像头数据显示
    '''

    def show_cameradata(self):
        # 获取摄像头数据
        pic = self.cameravideo.camera_to_pic()
        # 在lebel框中显示数据、显示画面
        self.label.setPixmap(pic)
        # 在label中显示当前时间
        # print(time.asctime())
        self.label_2.setText(time.asctime())

    '''
        获取Access_token访问令牌
    '''

    def get_accessToken(self):

        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        # host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=TKGXdKC7WPWeADGHmFBN8xAr&client_secret=lsr1tAuxv3tRGmOgZTGgNyri667dfKGg'
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=w6EtFT4ywGdPFjGq6THW2Ay3&client_secret=umaxaT4G52hc8bFwvIuLs0q1PkNpR08s'
        # 进行网络请求，使用get函数
        response = requests.get(host)
        if response:
            data = response.json()
            print(data)
            self.access_token = data['access_token']
            return self.access_token
        else:
            QMessageBox(self, "提示", "请检查网络连接！")

    def get_seach_data(self, data):
        self.plainTextEdit.setPlainText(data)
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        print(self.tableWidget.rowCount())
        for i in self.detect.sign_data_list.values():
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(i['user_id']))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(i['user_info']))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(i['group_id']))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(i['datetime']))
            self.tableWidget.resizeColumnToContents(4)
        # update: 2024-2-13
        # 新增表格列展示签到统计


    def add_class_by_name(self,name):
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/add"

        params = {
            "group_id": name
        }
        access_token = self.access_token
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            print(response.json())
            message = response.json()
            if message['error_code'] == 0:  # 根据规则，返回0则为班级添加成功
                QMessageBox.about(self, "班级创建结果", "班级创建成功")
            else:
                QMessageBox.about(self, "班级创建结果", "班级创建失败")

    # 添加班级
    def add_class(self):
        # 打开输入框，进行输入用户组
        group, ret = QInputDialog.getText(self, "添加班级", "请输入班级名称(由数字、字母、下划线组成)")
        if group == "":
            print("取消添加班级")
        else:
            self.add_class_by_name(group)

        self.fresh_window()

    # 班级查询
    def get_class(self):
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/getlist"
        params = {
            "start": 0,
            "length": 100
        }
        access_token = self.access_token
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            return response.json()

    # 学生查询
    def get_student_by_class(self,name):
        if name == "":
            return []
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/getusers"
        params = {
            "group_id": name
        }
        access_token = self.access_token
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            print(response.json())
            return response.json()["result"]["user_id_list"]
        else:
            return []

    # 将查询到的结果显示在MessageBOX框上面
    def display_class(self):
        list = self.get_class()
        str = ''
        for i in list['result']['group_id_list']:
            str = str + '\n' + i
        QMessageBox.about(self, "班级列表", str)

    # 删除班级调用
    def delete_class_by_name(self,name):
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/delete"

        params = {
            "group_id": name  # 要删除用户组的id
        }
        access_token = self.access_token
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            print(response.json())
            message = response.json()
            if message['error_code'] == 0:
                QMessageBox.about(self, "班级删除结果", "班级删除成功")
            else:
                QMessageBox.about(self, "班级删除结果", "班级删除失败")

    # 班级删除
    def delete_calss(self):
        # 打开输入框，进行输入用户组
        list = self.get_class()  # 首先获取用户组信息
        group, ret = QInputDialog.getText(self, "存在的班级", "班级信息" + str(list['result']['group_id_list']))
        if group == "":
            print("取消删除班级")
        else:
            self.delete_class_by_name(group)

        self.fresh_window()


    def add_student_by_name(self,base64_image,group,user_id,user_info):
        # 参数请求中，需要获取人脸编码，添加的组的id,添加的用户，新用户id信息
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add"

        params = {
            "image": base64_image,  # 人脸图片
            "image_type": "BASE64",  # 图片编码格式
            "group_id": group,  # 班级名称
            "user_id": user_id,  # 学生学号
            "user_info": user_info  # 学生姓名
        }
        access_token = self.access_token
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            data = response.json()
            if data['error_code'] == 0:
                QMessageBox.about(self, "增加结果", "学生增加成功！")
            else:
                QMessageBox.about(self, "增加结果", "学生增加失败！")

    # 增加学生信息
    def add_student(self):
        '''
        人脸注册
        '''
        list = self.get_class()  # 获取班级，将班级信息传递到我们新建的界面之中
        # 创建一个窗口，进行用户信息录入
        window = add_student_window(self,list['result']['group_id_list'], self)  # 将获取到的班级传递到新的界面，后续有用
        # 新创建窗口，通过exec()函数一直在执行，窗口不进行关闭
        window_status = window.exec_()
        # 判断
        if window_status != 1:
            return
        base64_image = window.base64_image


    def del_student_by_name(self,class_id,name):
        face_list = self.user_face_list(class_id, name)
        if face_list['error_msg'] == 'SUCCESS':
            for i in face_list['result']['face_list']:
                self.del_face_token(class_id, name, i['face_token'])
        else:
            return

    # 删除学生信息
    def del_student(self):
        list = self.get_class()  # 获取班级列表
        if list['error_msg'] == 'SUCCESS':
            window = del_student_window(list['result']['group_id_list'], self.access_token, self)
            # 新创建窗口，通过exec()函数一直在执行，窗口不进行关闭
            window_status = window.exec_()
            # 判断
            if window_status != 1:
                return
            class_name = window.class_name
            student_list = window.get_student_list(class_name)
            if student_list['error_msg'] == 'SUCCESS':
                student_no = window.student_no
                if student_no == "":
                    return
                for i in student_list['result']['user_id_list']:
                    if student_no == i:
                        self.del_student_by_name(class_name, student_no)
                    else:
                        return
            else:
                return
        else:
            return

    # 通过API访问规则，对学生人脸及有关信息进行删除
    def del_face_token(self, class_name, student_no, facetoken):
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/face/delete"
        params = {
            "user_id": student_no,
            "group_id": class_name,
            "face_token": facetoken
        }
        access_token = self.access_token
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            data = response.json()
            if data['error_code'] == 0:
                QMessageBox.about(self, "删除状态", "学生人脸及信息删除成功！")
            else:
                QMessageBox.about(self, "删除状态", "学生人脸及信息删除失败！")

    # 获取用户人脸列表
    def user_face_list(self, group, user):
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/face/getlist"
        params = {
            "user_id": user,
            "group_id": group
        }
        access_token = self.access_token
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            return response.json()

    # 学生有关信息查询
    def search_student(self):
        # 打开输入框，进行输入用户组
        student_no, ret = QInputDialog.getText(self, "学生学号", "请输入学生学号")
        if student_no == "":
            return
        else:
            request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/get"
            params = {
                "user_id": student_no,
                "group_id": "@ALL"
            }
            access_token = self.access_token
            request_url = request_url + "?access_token=" + access_token
            headers = {'content-type': 'application/json'}
            response = requests.post(request_url, data=params, headers=headers)
            if response:
                data = response.json()
                if data['error_code'] == 0:
                    QMessageBox.about(self, "查询结果", "学生姓名:" + data["result"]["user_list"][0]["user_info"] +
                                      "，班级：" + data["result"]["user_list"][0]["group_id"])
                else:
                    QMessageBox.about(self, "查询结果", "暂无该生！")
