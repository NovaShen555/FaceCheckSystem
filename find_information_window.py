import xlwt
from PyQt5.QtWidgets import QDialog, QAbstractItemView, QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox

from find_information import Ui_Dialog


class find_information_window(Ui_Dialog, QDialog):
    def __init__(self, sign_data, parent=None):
        super(find_information_window, self).__init__(parent)
        self.setupUi(self)
        self.sign_data = sign_data  # 接收签到数据
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可更改
        # 设置表格为指定长度
        self.tableWidget.setColumnWidth(0, 110)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.tableWidget.setColumnWidth(1, 55)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.tableWidget.setColumnWidth(2, 45)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.tableWidget.setColumnWidth(3, 180)
        for i in self.sign_data.values():
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(i['user_id']))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(i['user_info']))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(i['group_id']))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(i['datetime']))
            self.tableWidget.resizeColumnToContents(4)
        self.pushButton.clicked.connect(self.export)  # 绑定按钮事件为导出为Excel

    # 表格数据导出
    def export(self):
        # 打开保存文件弹窗
        try:
            path, ret = QFileDialog.getSaveFileName(self, "选择导出文件路径", ".", "文件格式(*.xls)")
            row = self.tableWidget.rowCount()  # 获取行
            column = self.tableWidget.columnCount()  # 获取列
            # 创建一个workbook 设置编码
            workbook = xlwt.Workbook(encoding='utf-8')
            # 创建一个表的名称，不是文件名称
            worksheet = workbook.add_sheet('学生签到信息')
            for j in range(column):
                table = self.tableWidget.horizontalHeaderItem(j).text()  # 获取表头
                worksheet.write(0, j, table)  # 写入表头
            for i in range(row):
                for j in range(column):
                    data = self.tableWidget.item(i, j).text()  # 获取签到数据
                    # 写入excel 参数对应 行, 列, 值
                    worksheet.write(i + 1, j, data)  # 写入签到数据
            # 保存
            workbook.save(path)
            QMessageBox.about(self, "提示", "数据导出成功！")
            self.accept()
        except:
            QMessageBox.about(self, "提示", "数据导出异常！")
