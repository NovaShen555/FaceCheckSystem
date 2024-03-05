import time

import requests
from PyQt5.QtCore import QThread, pyqtSignal, QDateTime
from punchData import punchData

class detect_thread(QThread):
    # transmit_data = pyqtSignal(dict)#定义信号，用于子线程与主线程中的人脸检测数据交互
    # update: 2024-2-13
    # 不再返回人脸的检测结果
    transmit_data1 = pyqtSignal(str)  # 定义信号，用于子线程与主线程中的人脸识别数据交互
    # 字典用来存储签到数据
    sign_data_list = {}
    store_data:list[punchData] = []

    def __init__(self,access_token):
        super(detect_thread,self).__init__()
        self.currentClass = ""
        self.ok=True#循环控制变量
        self.condition = False#人脸检测控制变量，是否进行人脸检测
        self.access_token=access_token#主线程获取的access_token信息传递给子线程并设置为全局变量
    #run函数执行结束代表线程结束
    def run(self):
        while self.ok==True:
            if self.condition==True:
                self.detect_face(self.imageData)
                self.condition=False
    '''
        接收主线程传递过来的图像
    '''
    def get_imgdata(self,data,currentClass):
        #当窗口调用这个槽函数，就把传递的数据存放在线程的变量中
        self.imageData=data#将接收到图像数据赋值给全局变量
        self.condition=True#主线程有图像传递过来，改变condition的状态，run函数中运行人脸检测函数
        self.currentClass = currentClass  # 将接收到的班级数据赋值给全局变量
    '''
        人脸检测
    '''
    def detect_face(self,base64_image):
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
        # 请求参数是一个字典，在字典中存储了，要识别的内容
        params = {
            "image": base64_image,  # 图片信息字符串
            "image_type": "BASE64",  # 图片信息的格式
            "face_field": "gender,age,beauty,mask,emotion,expression,glasses,face_shape",  # 请求识别人脸的熟悉，各个熟悉在字符中用，用逗号隔开
            "max_face_num": 10#能够检测的最多人脸数
        }
        # 访问令牌
        access_token = self.access_token
        request_url = request_url + "?access_token=" + access_token
        # 设置请求的格式体
        headers = {'content-type': 'application/json'}
        # 发送post网络请求,请求百度AI进行人脸检测
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            # data = response.json()
            self.face_search()
            # self.transmit_data.emit(dict(data))#如果返回结果正确，则将返回信息传递给主线程
            # update: 2024-2-13
            # 不再返回人脸的检测结果

    # 人脸识别搜索检测，只识别一个人
    def face_search(self):
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"
        params = {
            "image": self.imageData,
            "image_type": "BASE64",
            "group_id_list": self.currentClass,
        }
        access_token = self.access_token
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            data = response.json()
            if data['error_msg'] == 'SUCCESS':
                score = int(data['result']['user_list'][0]['score']*100)/100
                if data['result']['user_list'][0]['score'] > 90:  # 大于90分，意味人脸识别成功
                    del [data['result']['user_list'][0]['score']]
                    datetime = QDateTime.currentDateTime()  # 获取人脸打开时间
                    datetime = datetime.toString()  # 将获取到的时间转为字符串
                    data['result']['user_list'][0]['datetime'] = datetime  # 将获取到的时间添加到返回的数据中
                    key = data['result']['user_list'][0]['group_id'] + data['result']['user_list'][0][
                        'user_id']  # 在变量中键入值，包括班级名称和学生学号
                    if key not in self.sign_data_list.keys():
                        self.sign_data_list[key] = data['result']['user_list'][0]

                        self.store_data.append(punchData(data['result']['user_list'][0]['user_id'],
                                                         data['result']['user_list'][0]['user_info'],
                                                         data['result']['user_list'][0]['group_id'],
                                                         time.asctime()))

                    list1 = [data['result']['user_list'][0]['user_id'],
                             data['result']['user_list'][0]['group_id']]  # 去除名字和班级
                    self.transmit_data1.emit(
                        "学生签到成功\n学生信息如下:\n" + "姓名:" + list1[0] + "\n" + "班级:" + list1[1]+"\n匹配度："+str(score)+"%")  # 将信号发送给主线程
