# -*- coding: utf-8 -*-
"""
Example demonstrating a variety of scatter plot features.
"""



## Add path to library (just for examples; you do not need this)
#import initExample

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import csv


f = open('coordsTest.csv')
csv_f = csv.reader(f)

points = []

for row in csv_f:
    for x in range(0, len(row)):
        points += [row[x]]

pointsA = list(map(float, points[2:]))

pointsForm = []

for evens in range(0, len(pointsA), 2):
    pointsForm += [[pointsA[evens], pointsA[evens + 1]]]


print(pointsForm)

app = QtGui.QApplication([])
mw = QtGui.QMainWindow()
mw.resize(800,800)
view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
mw.setCentralWidget(view)
mw.show()
mw.setWindowTitle('pyqtgraph example: ScatterPlot')

## create four areas to add plots
w1 = view.addPlot()
view.nextRow()

def formList(x):
    ''' returns form for a list of [x, y]
    '''
    return form(x[0], x[1])

def form(x, y):
    return [{'pos': [x, y], 'data': 1}]

print("Generating data, this takes a few seconds...")

## There are a few different ways we can draw scatter plots; each is optimized for different types of data:


## 1) All spots identical and transform-invariant (top-left plot).
## In this case we can get a huge performance boost by pre-rendering the spot
## image and just drawing that image repeatedly.

n = 300
df = [[1,2],[2,3]]
s1 = pg.ScatterPlotItem(pos=df,size=10, pen=pg.mkPen(None), brush=pg.mkBrush(128, 255, 255, 120))
pos = np.random.normal(size=(2,n), scale=1e-5)


#s1 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 120))
pos = np.random.normal(size=(2,n), scale=1e-5)
spots = [{'pos': pos[:,i], 'data': 1} for i in range(n)] + [{'pos': [0,0], 'data': 1}]
print(spots)
#spots = [{'pos': pos[:,i], 'data': 1} for i in range(n)] + [{'pos': [0,0], 'data': 1}]
#for evens in range(0, len(plotPoints), 2):
#    s1.addPoints(form(plotPoints[evens], plotPoints[evens + 1])
#    w1.addItem(s1)
#for many in range(0, len(pointsForm)):
#    s1.addPoints(form(pointsForm[many][0], pointsForm[many][1]))
#s1.addPoints(formList(array(plotPoints[0])))


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


