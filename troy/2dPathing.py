#read in csv

import csv
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import random
import time
import pandas as pd
import pyqtgraph.examples

f = open('coordsTest.csv')
csv_f = csv.reader(f)

points = []

for row in csv_f:
    for x in range(0, len(row)):
        points += [row[x]]


#print(points)

points = [[5.0,0.0],[3.2,1.1],[2.2,3.3],[2.0,6.2],[2.3,7.3],[2.0,9.5]]

xVals = [5, 3, 2, 2, 2, 2]
yVals = [0, 1, 3, 6, 7, 10]


pyqtgraph.examples.run()


'''
x = np.random.normal(size=1000)
y = np.random.normal(size=1000)
pg.plot(x, y, pen=None, symbol="o")
pg.show()
'''

'''
x = np.arange(1000)
y = np.random.normal(size=(3, 1000))
plotWidget = pg.plot(title="3 plot curves")
for i in range(3):
    plotWidget.plot(x, y[i], pen=(i, 3))
'''


#pw = pg.plot(xVals, yVals, pen="r")
#pw.plot(xVals, yVals, pen="b")

#win = pg.GraphicsWindow()
#win.addPlot(pw)

#pg.show(imageData)


'''

app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()
g = gl.GLGridItem()
w.addItem(g)

indexesFinal = np.array([5, 0, 0])
sp2 = gl.GLScatterPlotItem(pos=[5, 0, 0], size=10.5, pxMode=False)

w.addItem(sp2)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, PYQT_VERSION):
        QtGui.QApplication.instance().exec_()

'''

