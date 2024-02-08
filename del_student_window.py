import requests
from PyQt5.QtWidgets import QDialog, QMessageBox

from del_student import Ui_Dialog

class del_student_window(Ui_Dialog,QDialog):
    def __init__(self,list,token,parent=None):
        super(del_student_window,self).__init__(parent)
        self.setupUi(self)
        self.show_class(list)#在删除页面弹出时候，直接调用班级显示函数，进行班级列表在下拉框中的显示
        self.access_token = token#定义全局变量，接收来自主界面传递过来的token，访问令牌
        # self.pushButton_2.clicked.connect(self.close_window)#取消删除按钮事件绑定
        self.comboBox.activated.connect(self.choose_group_student)#对下拉框发生选择的时候进行事件绑定
        self.pushButton.clicked.connect(self.get_data)#对确定删除按钮进行事件绑定

    # 显示班级信息在下拉框
    def show_class(self, list):
        self.comboBox.clear() #清楚下拉框的内容，放一次下一次进入后重叠
        for i in list:
            self.comboBox.addItem(i)
    #取消删除
    def close_window(self):
        self.close()
    #学生列表展示
    def show_student_list(self,list):
        self.listWidget.clear()#清楚文本框的内容
        if list['result']['user_id_list'] == []:
            self.listWidget.addItem("该班级中暂无学生！")
        for l in list['result']['user_id_list']:
            self.listWidget.addItem(l)#将获取到的学生列表显示在文本框中

    # 获取学生列表
    def get_student_list(self,group):
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/getusers"

        params = {
            "group_id": group
        }
        access_token = self.access_token
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            return response.json()

    #获取选中班级中的学生的事件绑定
    def choose_group_student(self):
        class_name = self.comboBox.currentText()
        student_list=self.get_student_list(class_name)
        self.show_student_list(student_list)
    #获取数据
    def get_data(self):
        #在删除界面上的文本框中，获取我们选择的班级和学号进行后面的删除
        try:
            self.class_name=self.comboBox.currentText()#获取下拉框中的班级名称
            self.student_no = self.listWidget.currentItem().text()#获取学生列表中的学生
            if self.student_no=="该班级中暂无学生！":
                QMessageBox.about(self, "提示", "请确认班级和学生！")
                return
            #关闭对话框
            self.accept()
        except:
            QMessageBox.about(self,"提示","请确认班级和学生！")

