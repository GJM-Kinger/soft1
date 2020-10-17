# @todo
# @Author: gou
# @Time: 2020/9/24 20:33
# @version: 1.0
import sys
from pyqtgraph.Qt import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer
from pyqtgraph_pyqt import Ui_MainWindow
from PyQt5.QtGui import QIcon
import pyqtgraph as pg
import numpy as np
import time
# global p1, data5, ptr5, curves


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    进行初始化
    """
    def __init__(self):
        super(MainWindow, self).__init__()

        pg.setConfigOption('background', '#f0f0f0')  # 设置背景为灰色
        pg.setConfigOption('foreground', 'd')  # 设置前景（包括坐标轴，线条，文本等等）为黑色
        pg.setConfigOption('antialias', True)  # 使曲线看起来更光滑，而不是锯齿状antialias
        self.setupUi(self)
        self.setWindowTitle('动态折线图绘制')
        self.chunkSize = 100
        self.maxChunks = 10
        self.startTime = pg.ptime.time()  # 单位为秒
        # time.sleep(0.001)
        # endTime = pg.ptime.time()
        # print(endTime - startTime)
        # self.GraphicsLayoutWidget.clear()
        # p1 = self.pyqtgraph1.addPlot(title='寻北结果曲线', y=np.random.random(50) * 10, pen=pg.mkPen(color='b', width=2))
        p1 = self.pyqtgraph1.addPlot(title='寻北结果曲线', pen=pg.mkPen(color='b', width=2))
        self.data1 = np.random.normal(size=500)
        self.curve1 = p1.plot(self.data1)
        # 设定定时器
        self.timer = pg.QtCore.QTimer()
        # 定时器信号绑定 update_data 函数
        self.timer.timeout.connect(self.update_data)
        # 定时器间隔50ms，可以理解为 50ms 刷新一次数据
        self.timer.start(50)

    # 数据左移
    def update_data(self):
        self.data1[:-1] = self.data1[1:]
        self.data1[-1] = np.random.normal()
        # 数据填充到绘制曲线中
        self.curve1.setData(self.data1)



        # p1.setLabel('left', 'num', '°')  # 设置坐标单位
        # p1.setLabel('bottom', 'Time', 's')
        # print(time.sleep(1))
        # while time.sleep(1):
        #     # global data1, ptr1
        #     data1[:-1] = data1[1:]
        #     p1.plot(data1)
        #     curve1.setData(data1)
        #     time.sleep(1)
        #     # print(data1)

        # def update1():
        #     global data1, ptr1
        #     data1[:-1] = data1[1:]
        #     data1[-1] = np.random.normal()
        #     curve1.setData(data1)

        # timer = pg.QtCore.QTimer()
        # timer.timeout.connect(update1)
        # timer.start(50)

        # # p1.setXRange(1, 30)
        # self.curves = []  # 先定义一个空列表
        # # 输出一个chunkSize * 2 的浮点数组（里边是矩阵）
        # self.data5 = np.empty((self.chunkSize + 1, 2))  # 创建一个二维数组
        # self.ptr5 = 0
        # # x = np.random.random(50) * 10
        # # a = np.random.random(8)
        # # p1.plot(x)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my = MainWindow()
    my.show()
    sys.exit(app.exec_())
    # import sys
    #
    # if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    #     QtGui.QApplication.instance().exec_()
