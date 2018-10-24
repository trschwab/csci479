from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import csv

app = QtGui.QApplication([])
mw = QtGui.QMainWindow()
mw.resize(800,800)
view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
mw.setCentralWidget(view)
mw.show()
mw.setWindowTitle('Visualize BEE PLOT')

w1 = view.addPlot()

f = open('locations.csv')

df = []
#if(=="last")
last_row = list(csv.reader(f))[-1]
for ind in range(1,len(last_row)):
    data = last_row[ind][1:-1].split(",")
    df.append([float(data[0]),float(data[1])])

s1 = pg.ScatterPlotItem(pos=df, size=10, pen=pg.mkPen(None), brush=pg.mkBrush(128, 255, 255, 120))
w1.addItem(s1)


## Make all plots clickable
lastClicked = []
def clicked(plot, points):
    global lastClicked
    for p in lastClicked:
        p.resetPen()
    print("clicked points", points)
    for p in points:
        p.setPen('b', width=2)
    lastClicked = points
s1.sigClicked.connect(clicked)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys


    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
