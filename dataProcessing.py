# @主要将寻北仪返回来的数据进行数据处理
# @Author: gou
# @Time: 2020/9/24 11:11
# @version: 1.0
import struct


# 应答数据处理
# from idlelib.idle_test.test_browser import f0


def num_direction(self):
    num_data = str(self)
    print(num_data)
    print(num_data)
    if num_data.startswith('81 03'):
        '''自检应答'''
        num_data_result = num_data[6:8]  # 该字节为自检结果
        num_data_temp = num_data[9:11]  # 温度自检结果
        if num_data_result == 'AA':
            # QMessageBox.information(self, '提示', '这是一个消息提示对话框!', QMessageBox.Ok | QMessageBox.Close, QMessageBox.Close)
            # QMessageBox.information(self, "自检", "自检通过！", QMessageBox.Yes | QMessageBox.No)
            QMessageBox.warning(self, "自检", "自检通过！")

            print('自检通过！')
        else:
            print('自检没有通过！')
        if num_data_temp == 'AA':
            print('温度自检通过！')
        else:
            print('温度自检没有通过！')
    elif num_data.startswith('84 0D'):
        '''读取磁罗盘'''
        # 4字节整型*3，共12字节磁罗盘数据
        pass
    elif num_data.startswith('85 01'):
        print('磁罗盘校准开始')
    elif num_data.startswith('86 01'):
        print('磁罗盘校准结束')
    elif num_data.startswith('87 02'):
        '''写入纬度应答'''
        if num_data[6:8] == 'AA':
            print('纬度写入成功！')
        else:
            print('纬度写入失败！')
    elif num_data.startswith('8A 04'):
        '''粗测应答'''
        num_measure_c = extraction_data(num_data)
        print('粗测结果：{}'.format(num_measure_c))
    elif num_data.startswith('8C 04'):
        '''精测A应答'''
        num_measure_h_A = extraction_data(num_data)
        print('精测A结果：{}'.format(num_measure_h_A))
    elif num_data.startswith('8E 04'):
        '''精测B应答'''
        num_measure_h_B = extraction_data(num_data)
        print('精测B结果：{}'.format(num_measure_h_B))
    elif num_data.startswith('8F 04'):
        '''寻北结果应答'''
        global num_measure_north
        num_measure_north = extraction_data(num_data)
        print('寻北结果为：{}'.format(num_measure_north))
    else:
        pass

    # 模拟画图


def drags(self):
    # self.graphicsLayoutWidget.clear()  # 清空里面的内容，否则会发生重复绘图的结果

    '''第一种绘图方式    normal表示正态'''
    # pg.setConfigOption('background', '#f0f0f0')  # 设置背景为灰色
    # pg.setConfigOption('foreground', 'd')  # 设置前景（包括坐标轴，线条，文本等等）为黑色
    # pg.setConfigOption('antialias', True)  # 使曲线看起来更光滑，而不是锯齿状antialias
    # self.graphicsLayoutWidget.addPlot(y=np.random.normal(size=100), pen=pg.mkPen(color='b', width=2))
    p1 = self.graphicsLayoutWidget.addPlot(title='寻北结果曲线', )
    p1.setLabel('left', '结果', 'mil')  # 设置坐标单位
    p1.setLabel('bottom', 'num', '1')
    self.data1 = np.random.normal(size=200)
    self.curve1 = p1.plot(self.data1, pen=pg.mkPen(color='r', width=1.4))
    # 设定定时器
    self.timer1 = pg.QtCore.QTimer()
    # 定时器信号绑定 update_data 函数
    self.timer1.timeout.connect(self.update_data)
    # 定时器间隔50ms，可以理解为 50ms 刷新一次数据
    self.timer1.start(100)

    # 数据左移


def update_data(self):
    self.data1[:-1] = self.data1[1:]
    self.data1[-1] = np.random.normal()
    # 数据填充到绘制曲线中
    self.curve1.setData(self.data1)


# 从数据包中取出测量的数据
def extraction_data(self):
    if self[12:14] == '55':
        print('数据无效！')
        return None
    else:
        # 数据有效
        str_num = str2list(self)
        measure = str_num[3]
        measure += str_num[2]
        num_measure = int(measure, 16)
        return num_measure


# 将字符串转换成列表
def str2list(self):
    str_list = []
    data1 = self
    while data1 != '':
        str_list.append(data1[0:2])
        data1 = data1[2:].strip()
    return str_list


# 创建一个动态数组
def dyna_list():
    # a = np.zeros((10, 2))
    # print(a)
    # a(0)
    a = []
    a.append([0, 0])
    a.append([1, 2])
    m = a[1]
    print(m[1])


if __name__ == '__main__':

    # struct.pack('<f', s)[0]
    # struct.unpack('!f', bytes.fromhex('CDCC2E42'))[0]
    a = struct.unpack('!f', bytes.fromhex('422eccdc'))[0]
    print(a)
