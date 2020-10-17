# @光纤陀螺寻北仪测试软件
# @Author: gou
# @Time: 2020/9/20 20:20
# @version: 1.0
import sys
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer
from mainLay2 import Ui_From
from PyQt5.QtGui import QIcon
import pyqtgraph as pg
import struct
from dec2h import *
num_measure_list = []  # 寻北结果值数组
num_c_list = []        # 粗测数组
num_fog_list = []      # 陀螺采集数


class MainWindow(QtWidgets.QMainWindow, Ui_From):
    def __init__(self):
        super(MainWindow, self).__init__()
        pg.setConfigOption('background', '#f0f0f0')  # 设置背景为灰色
        pg.setConfigOption('foreground', 'b')  # 设置前景（包括坐标轴，线条，文本等等）为黑色
        pg.setConfigOption('antialias', True)  # 使曲线看起来更光滑，而不是锯齿状antialias
        self.setupUi(self)
        self.initUI()
        self.setWindowTitle("陀螺仪测试软件")
        self.ser = serial.Serial()
        self.port_check()
        # 设置图标
        self.setWindowIcon(QIcon("./images/com.png"))

        # 接收数据和发送数据数目置零
        self.data_num_received = 0  # 接收数据累加和
        self.lineEdit_9.setText(str(self.data_num_received))
        self.data_num_sended = 0  # 发送数据累加和
        self.lineEdit_10.setText(str(self.data_num_sended))

    def initUI(self):
        # 波特率
        list_bote_num = ['57600', '115200', '56000', '38400', '19200', '14400', '9600']
        self.comboBox_2.addItems(list_bote_num)    # 这里也可以使用addItem, 一项一项加

        # 命令区
        list_command_str = ['系统自检', '参数上传', '参数下传', '罗盘采集', '罗盘校准开始', '罗盘校准结束', '纬度装订', '陀螺采集开始',
                  '方位粗测', '方位精测位置A', '方位精测位置B', '方位采集', '连续采集', '方位角精测位置A数据', '方位角精测位置B数据']
        self.comboBox_3.addItem('请选择命令')
        self.comboBox_3.addItems(list_command_str)

        # 串口检测按钮
        self.pushButton.clicked.connect(self.port_check)

        # 串口信息显示
        self.comboBox.currentTextChanged.connect(self.port_imf)

        # 打开串口按钮
        self.pushButton_2.clicked.connect(self.port_open)

        # 关闭串口按钮
        self.pushButton_3.clicked.connect(self.port_close)

        # 发送数据按钮
        self.pushButton_4.clicked.connect(self.data_send)

        # 定时发送数据
        self.timer_send = QTimer()
        self.timer_send.timeout.connect(self.data_send)
        self.checkBox_4.stateChanged.connect(self.data_send_timer)

        # 定时器接收数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.data_receive)
        self.textEdit_2.setText("")

        # 清除接收窗口
        self.pushButton_5.clicked.connect(self.receive_data_clear)

        # 清除发送区
        self.pushButton_6.clicked.connect(self.send_data_clear)

    # 获取命令
    def have_command(self):
        # 计算纬度装订命令
        num_latitude_command_1 = int('0x07', 16)
        num_latitude_command_2 = int('0x04', 16)
        num_latitude_command_3 = int(self.lineEdit_2.text())
        num_latitude_command_4 = int(self.lineEdit_3.text())
        num_latitude_command_5 = int(self.lineEdit_4.text())
        num_latitude_command_6 = self.low_hex2(dec2hex(num_latitude_command_1 + num_latitude_command_2
                                     + num_latitude_command_3 + num_latitude_command_4 + num_latitude_command_5))
        str_latitude_command_3 = dec2hex1(int(self.lineEdit_2.text().strip()))
        str_latitude_command_4 = dec2hex1(int(self.lineEdit_3.text().strip()))
        str_latitude_command_5 = dec2hex1(int(self.lineEdit_4.text().strip()))

        # 计算粗测命令
        temp_L = self.dig_command(self.lineEdit_5)
        str_L_measure_3 = '0x'
        str_L_measure_4 = '0x'
        str_L_measure_3 += temp_L[4:6]
        str_L_measure_4 += temp_L[2:4]
        num_L_measure_1 = int('0x0A', 16)
        num_L_measure_2 = int('0x03', 16)
        num_L_measure_3 = int(str_L_measure_3, 16)
        num_L_measure_4 = int(str_L_measure_4, 16)
        str_L_measure_5 = self.low_hex2(dec2hex(num_L_measure_1 + num_L_measure_2 + num_L_measure_3 + num_L_measure_4))

        # 计算精测位置A
        temp_H_A = self.dig_command(self.lineEdit_6)
        str_H_A_measure_3 = '0x'
        str_H_A_measure_4 = '0x'
        str_H_A_measure_3 += temp_H_A[4:6]
        str_H_A_measure_4 += temp_H_A[2:4]
        num_H_A_measure_1 = int('0x0C', 16)
        num_H_A_measure_2 = int('0x03', 16)
        num_H_A_measure_3 = int(str_H_A_measure_3, 16)
        num_H_A_measure_4 = int(str_H_A_measure_4, 16)
        str_H_A_measure_5 = self.low_hex2(dec2hex(num_H_A_measure_1 + num_H_A_measure_2 + num_H_A_measure_3 + num_H_A_measure_4))

        # 计算精测位置B
        temp_H_B = self.dig_command(self.lineEdit_7)
        str_H_B_measure_3 = '0x'
        str_H_B_measure_4 = '0x'
        str_H_B_measure_3 += temp_H_B[4:6]
        str_H_B_measure_4 += temp_H_B[2:4]
        num_H_B_measure_1 = int('0x0E', 16)
        num_H_B_measure_2 = int('0x03', 16)
        num_H_B_measure_3 = int(str_H_B_measure_3, 16)
        num_H_B_measure_4 = int(str_H_B_measure_4, 16)
        str_H_B_measure_5 = self.low_hex2(dec2hex(num_H_B_measure_1 + num_H_B_measure_2
                                                  + num_H_B_measure_3 + num_H_B_measure_4))

        # 命令字典
        num_command = {
            '系统自检': ['0x01', '0x01', '0x02'],
            '参数上传': [],
            '参数下传': ['0x03', '0x01', '0x04'],
            '罗盘采集': ['0x04', '0x01', '0x05'],
            '罗盘校准开始': ['0x05', '0x01', '0x06'],
            '罗盘校准结束': ['0x06', '0x01', '0x07'],
            '纬度装订': ['0x07', '0x04', str_latitude_command_3, str_latitude_command_4,
                     str_latitude_command_5, num_latitude_command_6],
            '陀螺采集开始': ['0x08', '0x01', '0x09'],
            '方位粗测': ['0x0A', '0x03', str_L_measure_3, str_L_measure_4, str_L_measure_5],
            '方位精测位置A': ['0x0C', '0x03', str_H_A_measure_3, str_H_A_measure_4, str_H_A_measure_5],
            '方位精测位置B': ['0x0E', '0x03', str_H_B_measure_3, str_H_B_measure_4, str_H_B_measure_5],
            '方位采集': ['0x0F', '0x01', '0x10'],
            '连续采集': ['0x08', '0x01', '0x09'],
            '方位角精测位置A数据': ['0x0B', '0x05', '0x00', '0x00', '0xE1', '0x44', '0x35'],
            '方位角精测位置B数据': ['0x0D', '0x05', '0x00', '0x00', '0xE1', '0x44', '0x37']
        }
        # 选中的命令
        try:
            list_command = num_command[self.comboBox_3.currentText()]    # 获取命令字典的内容
        except:
            QMessageBox.critical(self, '命令选择错误', '请先选择命令')
            return None
        str_command = ''
        for x in list_command:
            if x.startswith('0x'):
                x = x[2:]
                str_command += x
                str_command += ' '
        print(str_command)
        return str_command

    # 串口检测
    def port_check(self):
        # 检测所有存在的串口，将信息存储在字典中
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        self.comboBox.clear()
        for port in port_list:
            self.Com_Dict["%s" % port[0]] = "%s" % port[1]
            self.comboBox.addItem(port[0])
        if len(self.Com_Dict) == 0:
            self.comboBox.setText("无串口")

    # 串口信息
    def port_imf(self):
        # 显示选定的串口的详细信息
        imf_s = self.comboBox.currentText()
        if imf_s != "":
            self.lineEdit_13.setText(self.Com_Dict[self.comboBox.currentText()])

    # 打开串口
    def port_open(self):
        self.ser.port = self.comboBox.currentText()
        self.ser.baudrate = int(self.comboBox_2.currentText())         # 将文本内的波特率字符串装换为整型
        self.ser.bytesize = 8                                          # 数据位
        self.ser.stopbits = 1                                          # 停止位
        self.ser.parity = serial.PARITY_NONE                           # 校验位为无
        try:
            self.ser.open()
        except:
            QMessageBox.critical(self, "Port Error", "此串口不能被打开！")
            return None

        # 打开串口接收定时器，周期为2ms
        self.timer.start(2)
        if self.ser.isOpen():
            self.pushButton_2.setEnabled(False)  # 打开串口按钮不可用
            self.pushButton_3.setEnabled(True)  # 关闭串口可用
            self.lineEdit.setEnabled(False)     # 采集周期不可用
            self.pushButton.setEnabled(False)   # 串口检测不可用
            self.comboBox.setEnabled(False)     # 串口选择不可用
            self.comboBox_2.setEnabled(False)   # 波特率不可用
            self.lineEdit_11.setText("串口打开成功")
            print("串口打开成功")
        # 显示串口信息
        if self.ser.isOpen():
            self.lineEdit_12.setText((self.get_port_info()))
        else:
            self.lineEdit_12.setText('None')

    # 关闭串口
    def port_close(self):
        self.timer.stop()
        self.timer_send.stop()
        try:
            self.ser.close()
        except:
            QMessageBox.critical(self, "Port Error", "串口关闭失败！")

        self.pushButton_2.setEnabled(True)      # 打开串口按钮可用
        self.pushButton_3.setEnabled(False)     # 关闭串口按钮不可用
        self.lineEdit.setEnabled(True)          # 采集周期不可用
        self.pushButton.setEnabled(True)       # 串口检测不可用
        self.comboBox.setEnabled(True)         # 串口选择不可用
        self.comboBox_2.setEnabled(True)       # 波特率不可用
        # 接收数据和发送数据数目置零
        self.data_num_received = 0
        self.lineEdit_9.setText(str(self.data_num_received))
        self.data_num_sended = 0
        self.lineEdit_10.setText(str(self.data_num_sended))
        self.lineEdit_11.setText("串口已关闭")
        self.lineEdit_12.setText('None')
        print("串口已关闭")

    # 发送数据
    def data_send(self):
        if self.ser.isOpen():
            if self.checkBox_3.isChecked():
                input_s = self.textEdit.toPlainText()  # 获得手动输入内容
            else:
                input_s = self.have_command()  # 获得内置命令
            if input_s != "":
                # 非空字符串
                if self.checkBox.isChecked():
                    # hex发送
                    input_s = input_s.strip()
                    send_list = []
                    while input_s != '':
                        try:
                            num = int(input_s[0:2], 16)
                        except ValueError:
                            QMessageBox.critical(self, 'wrong data', '请输入十六进制数据，以空格分开!')
                            return None
                        input_s = input_s[2:].strip()
                        send_list.append(num)
                    input_s = bytes(send_list)
                else:
                    # ascii发送
                    input_s = (input_s + '\r\n').encode('utf-8')
                    print("ascii发送")

                num = self.ser.write(input_s)
                self.data_num_sended += num
                self.lineEdit_10.setText(str(self.data_num_sended))
        else:
            pass

    # 接收数据
    def data_receive(self):
        try:
            num = self.ser.inWaiting()
        except:
            self.port_close()
            return None
        if num > 0:
            data = self.ser.read(num)            # 将采集到的数据放到data中
            num = len(data)
            # hex显示
            if self.checkBox_2.checkState():
                out_s = ''
                for i in range(0, len(data)):
                    out_s = out_s + '{:02X}'.format(data[i]) + ' '

                # self.textEdit_2.setText("")
                self.textEdit_2.insertPlainText(out_s)   # 这个是将数据发送到textEdit的命令
                # self.lineEdit_14.setText(out_s)
            else:
                # 串口接收到的字符串为b'xxx',要转化成iso-8859-1字符串才能输出到窗口中去
                self.textEdit_2.insertPlainText(data.decode('iso-8859-1'))
                # self.textEdit.insertPlainText(data.decode('unicode'))

            # 统计接收字符的数量
            self.data_num_received += num
            self.lineEdit_9.setText(str(self.data_num_received))

            # 获取到text光标
            textCursor = self.textEdit.textCursor()
            # 滚动到底部
            textCursor.movePosition(textCursor.End)
            # 设置光标到text中去
            self.textEdit.setTextCursor(textCursor)

            self.num_direction(out_s)      # 对接到的数据进行处理
        else:
            pass

    # 定时发送数据
    def data_send_timer(self):
        if self.checkBox_4.isChecked():
            self.timer_send.start(int(self.lineEdit.text()))  # 采样周期100ms
            self.lineEdit.setEnabled(False)
        else:
            self.timer_send.stop()
            self.lineEdit.setEnabled(True)

    # 清除显示
    def receive_data_clear(self):
        self.textEdit_2.setText("")

    # 清除显示
    def send_data_clear(self):
        self.textEdit.setText("")

    # 获得串口信息
    def get_port_info(self):
        str_info = ' '
        str_info += self.comboBox_2.currentText()
        print(self.comboBox_2.currentText())
        str_info += ','
        str_info += 'n'
        str_info += ','
        str_info += '8'
        str_info += ','
        str_info += '1'
        return str_info

    # 计算数据域命令
    def dig_command(self, buttonName):
        return num_len((int(buttonName.text().strip())) * 10)

    # 取十六进制的低两位
    def low_hex2(self, string_hex):
        str_new = '0x'
        str_new += string_hex[-2:]
        return str_new

    # 应答数据处理
    def num_direction(self, data4):
        num_data = str(data4)
        # print(num_data)                  # 打印出接收到的数据
        fog_data = self.textEdit_2.toPlainText()    # 获取textEdit当前文本
        print(fog_data)
        if num_data.startswith('81 03'):
            '''自检应答'''
            num_data_result = num_data[6:8]  # 该字节为自检结果
            num_data_temp = num_data[9:11]  # 温度自检结果
            if num_data_result == 'AA' and num_data_temp == 'AA':
                self.textEdit_2.insertPlainText('自检通过')
                print('自检通过！')
            else:
                QMessageBox.warning(self, "自检", "系统自检或温度自检没有通过！")
        elif num_data.startswith('84 0D'):
            '''读取磁罗盘'''
            # 4字节整型*3，共12字节磁罗盘数据
            pass
        elif num_data.startswith('85 01'):
            print('磁罗盘校准开始')
            self.textEdit_2.insertPlainText('磁罗盘校准开始')
        elif num_data.startswith('86 01'):
            print('磁罗盘校准结束')
            self.textEdit_2.insertPlainText('磁罗盘校准结束')
        elif num_data.startswith('87 02'):
            '''写入纬度应答'''
            if num_data[6:8] == 'AA':
                print('纬度写入成功！')
                self.textEdit_2.insertPlainText('纬度写入成功')
            else:
                print('纬度写入失败！')
                QMessageBox.warning(self, "纬度装订", "纬度写入失败！")
        elif num_data.startswith('8A 04'):
            '''粗测应答'''
            self.num_measure_c = self.extraction_data(num_data)
            num_c_list.append(float(self.num_measure_c))
            print('粗测结果：{}'.format(self.num_measure_c))
            self.lineEdit_8.setText(self.num_measure_c)
            self.drags2()
            # self.update_data2()
        elif num_data.startswith('8C 04'):
            '''精测A应答'''
            num_measure_h_A = self.extraction_data(num_data)
            print('精测A结果：{}'.format(num_measure_h_A))
            self.lineEdit_8.setText(self.num_measure_h_A)
        elif num_data.startswith('8E 04'):
            '''精测B应答'''
            num_measure_h_B = (self.extraction_data(num_data))
            print('精测B结果：{}'.format(num_measure_h_B))
            self.lineEdit_8.setText(self.num_measure_h_B)
        elif num_data.startswith('8F 04'):
            '''寻北结果应答'''
            self.num_measure_north = (self.extraction_data(num_data))
            num_measure_list.append(float(self.num_measure_north))
            print('寻北结果为：{}'.format(self.num_measure_north))
            self.lineEdit_8.setText(self.num_measure_north)
            print(num_measure_list)
            self.drags1()
            self.update_data1(num_measure_list)
        elif num_data.startswith('EB 90 C8 01'):
            print(self.str2list(num_data[102:123]))
            measure_list = self.str2list(num_data[12:23])
            measure_fog = measure_list[3]
            measure_fog += measure_list[2]
            measure_fog += measure_list[1]
            measure_fog += measure_list[0]
            measure_fog = (struct.unpack('!f', bytes.fromhex(measure_fog))[0]) / 14
            print(measure_fog)
            self.drags3()  # 得到一个数就重新画一次图
            num_fog_list.append(measure_fog)
            print(num_fog_list)
        elif num_data.startswith('55 01 56'):
            QMessageBox.warning(self, "指令异常", "寻北仪收到的命令校验和不通过，或者命令不规范！")
        else:

            pass

    # 寻北结果画图
    def drags1(self):
        self.graphicsLayoutWidget.clear()  # 清空里面的内容，否则会发生重复绘图的结果
        p1 = self.graphicsLayoutWidget.addPlot(title='寻北结果曲线', )
        p1.setLabel('left', '结果', 'mil')  # 设置坐标单位
        p1.setLabel('bottom', 'num', '1')
        self.curve = p1.plot(num_measure_list, pen=pg.mkPen(color='r', width=1.4))
        # p1.setXRange(1, 20)

    # 数据左移
    def update_data1(self, num_list):
        if len(num_list) != 0:
            num_list[:-1] = num_list[1:]
            self.curve.setData(num_list)
        else:
            pass

    # 粗测画图
    def drags2(self):
        self.graphicsLayoutWidget.clear()  # 清空里面的内容，否则会发生重复绘图的结果
        p2 = self.graphicsLayoutWidget.addPlot(title='粗测结果曲线', )
        p2.setLabel('left', '结果', 'mil')  # 设置坐标单位
        p2.setLabel('bottom', 'num', '1')
        self.curve2 = p2.plot(y=num_c_list, pen=pg.mkPen(color='r', width=1.4))
        # p2.setXRange(0, 10)

    # 陀螺画图
    def drags3(self):
        self.graphicsLayoutWidget.clear()  # 清空里面的内容，否则会发生重复绘图的结果
        p2 = self.graphicsLayoutWidget.addPlot(title='陀螺结果曲线', )
        p2.setLabel('left', '结果', '1')  # 设置坐标单位
        p2.setLabel('bottom', 'num', '1')
        self.curve2 = p2.plot(y=num_fog_list, pen=pg.mkPen(color='r', width=1.4))
        # p2.setXRange(0, 10)

    # 从数据包中取出测量的数据
    def extraction_data(self, num_data):
        if num_data[12:14] == '55':
            print('数据无效！')
            return str(0)
        else:
            # 数据有效
            print('数据有效！')
            str_num = self.str2list(num_data)
            measure = str_num[3]
            measure += str_num[2]
            num_measure = int(measure, 16)
            return str(num_measure / 10)

    # 将字符串转换成列表
    def str2list(self, num_data1):
        str_list = []
        data1 = num_data1
        while data1 != '':
            str_list.append(data1[0:2])
            data1 = data1[2:].strip()
        return str_list


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my = MainWindow()
    my.show()
    sys.exit(app.exec_())
