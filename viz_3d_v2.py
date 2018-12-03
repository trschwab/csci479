from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import random
import time
import pandas as pd
import matplotlib.pyplot as plt

def visualize_3d():
	#app = QtGui.QApplication([])
	w = gl.GLViewWidget()
	w.show()
	g = gl.GLGridItem()
	w.addItem(g)

	df = pd.read_csv('positions_d.txt')
	df = df[df.columns[0:3]].values / 5


	cmap = plt.get_cmap('cool')
	colors = []
	for i in range(df.shape[0]):
		normal_num = i / df.shape[0]
		colors.append(cmap(normal_num))

	colors = np.array(colors)

	indexesFinal = np.array([[1,2]])
	sp2 = gl.GLScatterPlotItem(pos=df,size=0.1,pxMode=False ,color= colors)
	w.addItem(sp2)

	sp2 = gl.GLLinePlotItem(pos=df,width=0.5)
	w.addItem(sp2)


	## Start Qt event loop unless running in interactive mode.
	if __name__ == '__main__':
	    import sys
	    if (sys.flags.interactive != 1) or not hasattr(QtCore, PYQT_VERSION):
	        QtGui.QApplication.instance().exec_()

def call_it():
	visualize_3d()
