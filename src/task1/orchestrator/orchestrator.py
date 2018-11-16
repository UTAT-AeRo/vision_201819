import sys
import os
from PyQt4 import QtGui, QtCore


class Window(QtGui.QMainWindow):

    def __init__(self):
        # Initialize Variables
        self.dir = ""

        # Initialize Window
        super(Window, self).__init__()
        self.setGeometry(50, 50, 900, 550)
        self.setWindowTitle("AeRo Task 1 Program")
        # self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
        self.home()

    def home(self):
        # Quit Button
        btn = QtGui.QPushButton("Quit", self)
        btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        btn.resize(200, 50)
        btn.move(680, 490)

        # Select Directory Curr Directory
        self.dirLabel = QtGui.QLabel(self)
        self.dirLabel.setText(self.dir)
        self.dirLabel.resize(800, 50)
        self.dirLabel.move(230, 100)

        # Select Directory Button
        btn = QtGui.QPushButton("Browse For Photo Directory", self)
        btn.clicked.connect(self.getDirectory)
        btn.resize(200, 50)
        btn.move(25, 90)

        # Logo
        pic = QtGui.QLabel(self)
        # pic.move(25, 400)
        pic.setGeometry(30, 465, 400, 100)
        # use full ABSOLUTE path to the image, not relative
        pic.setPixmap(QtGui.QPixmap(os.getcwd() + "/logo.png"))

        self.populateTask1()
        self.show()

    def populateTask1(self):
        # Module 1 Button
        btn = QtGui.QPushButton("Module 1 - Auto Filter", self)
        # btn.clicked.connect(self.getDirectory)
        btn.resize(200, 50)
        btn.move(25, 250)

        # Module 1 Label
        self.m1s = QtGui.QLabel(self)
        self.m1s.setText("Not Run")
        self.m1s.resize(100, 50)
        self.m1s.move(240, 250)
        self.m1s.setStyleSheet('color: red')

        # Module 2 Button
        btn = QtGui.QPushButton("Module 2 - Human Filter", self)
        # btn.clicked.connect(self.getDirectory)
        btn.resize(200, 50)
        btn.move(25, 300)

        # Module 2 Label
        self.m2s = QtGui.QLabel(self)
        self.m2s.setText("Not Run")
        self.m2s.resize(100, 50)
        self.m2s.move(240, 300)
        self.m2s.setStyleSheet('color: red')

        # Module 3 Button
        btn = QtGui.QPushButton("Module 3 - Locate IR Pts", self)
        # btn.clicked.connect(self.getDirectory)
        btn.resize(200, 50)
        btn.move(25, 350)

        # Module 3 Label
        self.m3s = QtGui.QLabel(self)
        self.m3s.setText("Not Run")
        self.m3s.resize(100, 50)
        self.m3s.move(240, 350)
        self.m3s.setStyleSheet('color: red')

        # Module 4 Button
        btn = QtGui.QPushButton("Module 4 - Plot On Map", self)
        # btn.clicked.connect(self.getDirectory)
        btn.resize(200, 50)
        btn.move(25, 400)

        # Module 4 Label
        self.m4s = QtGui.QLabel(self)
        self.m4s.setText("Not Run")
        self.m4s.resize(100, 50)
        self.m4s.move(240, 400)
        self.m4s.setStyleSheet('color: red')

        # Module AreaPercent Button
        btn = QtGui.QPushButton("ID Degree of Damage", self)
        # btn.clicked.connect(self.getDirectory)
        btn.resize(200, 50)
        btn.move(450, 250)

        # Module AreaPercent Label
        self.mscs = QtGui.QLabel(self)
        self.mscs.setText("Not Run")
        self.mscs.resize(100, 50)
        self.mscs.move(670, 250)
        self.mscs.setStyleSheet('color: red')

        # Module 1 Button
        btn = QtGui.QPushButton("ID Signif Changes", self)
        # btn.clicked.connect(self.getDirectory)
        btn.resize(200, 50)
        btn.move(450, 400)

        # Module 1 Label
        self.mscs = QtGui.QLabel(self)
        self.mscs.setText("Not Run")
        self.mscs.resize(100, 50)
        self.mscs.move(670, 400)
        self.mscs.setStyleSheet('color: red')


    def getDirectory(self):
        self.dir = QtGui.QFileDialog.getExistingDirectory(
            self,
            "Open a folder",
            os.getcwd(),
            QtGui.QFileDialog.ShowDirsOnly)

        self.dirLabel.setText(self.dir)




def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())


run()