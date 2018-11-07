import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import bee_track_v1
from visualize_path_simple import visualize

class App(QWidget):

    beeNumber = 99999999

    def __init__(self):
        super().__init__()
<<<<<<< HEAD:button_pyqt5.py
        self.title = 'Insect Tracker App'
        self.left = 250
        self.top = 150
        self.width = 420
        self.height = 300
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #
        # MY CODE
        #



        #
        #
        #

        run_button = QPushButton('Run Trial', self)
        run_button.setToolTip('Click here to start image processing for a trial')
        run_button.move(150,210)
        run_button.clicked.connect(self.on_click)

        view_button = QPushButton('View Results', self)
        view_button.setToolTip('Click here to see past results of trials')
        view_button.move(150,120)
        view_button.clicked.connect(self.on_click)


        self.show()
=======
        self.ui = uic.loadUi('mainGUI.ui')
        self.ui.runTestButton.clicked.connect(self.runTest)
        self.ui.viewResultsButton.clicked.connect(self.viewResults)
        self.ui.show()
>>>>>>> a8c72a66ac2867ef5985b894529a83200c0b0322:button_pyqt5

    @pyqtSlot()
    def runTest(self):
        beeNumber = self.getInteger()
        if (beeNumber != None):
          bee_track_v1.runTest(beeNumber)

    def viewResults(self):
        self.window = SecondaryWindow(self)
        self.ui.close()


    def getInteger(self):
        i, okPressed = QInputDialog.getInt(self, "Trial ID","Enter Trial ID:", 28, 0, 100, 1)
        if okPressed:
            return i


class SecondaryWindow(QWidget):
    def __init__(self, parent=None):
      super().__init__()
      self.ui = uic.loadUi('visualizeGUI.ui')
      self.ui.testIDLineEdit.setValidator(QIntValidator())
      self.ui.runVisualizationButton.clicked.connect(self.openVisualzation)
      self.ui.plotTypeCombo.currentIndexChanged.connect(self.selectionChanged)
      self.ui.show()

    def selectionChanged(self):
      if(self.ui.plotTypeCombo.currentText() == 'index'):
        self.ui.testIDLineEdit.setReadOnly(False)
      elif (self.ui.plotTypeCombo.currentText() == 'all' or
              self.ui.plotTypeCombo.currentText() == 'latest'):
        self.ui.testIDLineEdit.setText('')
        self.ui.testIDLineEdit.setReadOnly(True)

    #opens the visualization
    def openVisualzation(self):
      if (self.ui.testIDLineEdit.text() == '' and self.ui.plotTypeCombo.currentText() == 'index'):
        return
      else:
        if(self.ui.plotTypeCombo.currentText() == 'index'):
          visualize("locations.csv", self.ui.plotTypeCombo.currentText(), self.ui.testIDLineEdit.text())
        else:
          visualize("locations.csv", self.ui.plotTypeCombo.currentText(), 0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
