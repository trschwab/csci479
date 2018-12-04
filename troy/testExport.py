import pyqtgraph as pg
import pyqtgraph.exporters


plt = pg.plot([1,5,2,4,3])

exporter = pg.exporters.ImageExporter(plt.plotItem)

exporter.parameters()['width'] = 100

exporter.export('fileName.png')
