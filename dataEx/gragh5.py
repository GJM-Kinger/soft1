# @todo
# @Author: gou
# @Time: 2020/9/28 16:24
# @version: 1.0

# import initExample  ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('折线图')
# 3) Plot in chunks, adding one new plot curve for every 100 samples
chunkSize = 100
# Remove chunks after we have 10
maxChunks = 10
startTime = pg.ptime.time()
win.nextRow()
p5 = win.addPlot(colspan=2, pen='r')
p5.setLabel('bottom', 'Time', 's')
p5.setXRange(-10, 0)
curves = []   # 先定义一个空列表
# 输出一个chunkSize * 2 的浮点数组（里边是矩阵）
data5 = np.empty((chunkSize + 1, 2))  # 创建一个二维数组
ptr5 = 0


def update3():
    global p5, data5, ptr5, curves
    now = pg.ptime.time()
    for c in curves:
        c.setPos(-(now - startTime), 0)

    i = ptr5 % chunkSize
    if i == 0:
        curve = p5.plot()
        curves.append(curve)
        last = data5[-1]
        data5 = np.empty((chunkSize + 1, 2))
        data5[0] = last
        while len(curves) > maxChunks:
            c = curves.pop(0)
            p5.removeItem(c)
    else:
        curve = curves[-1]
    data5[i + 1, 0] = now - startTime
    data5[i + 1, 1] = np.random.normal() * 10
    curve.setData(x=data5[:i + 2, 0], y=data5[:i + 2, 1])
    ptr5 += 1


# update all plots
def update():
    # update1()
    # update2()
    update3()


timer = pg.QtCore.QTimer()
timer.timeout.connect(update3)
timer.start(50)


# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
