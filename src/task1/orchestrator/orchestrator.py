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

        # Step 1 Label
        bl = QtGui.QLabel(self)
        bl.setText("Step 1 -  select the source image folders")
        bl.resize(600, 50)
        bl.move(25, 20)
        bl.setStyleSheet('color: darkblue')

        # Step 2 Label
        bl = QtGui.QLabel(self)
        bl.setText("Step 2 -  Run the modules. Keep in mind to run them in order if applicable")
        bl.resize(600, 50)
        bl.move(25, 200)
        bl.setStyleSheet('color: darkblue')

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
        self.mb1 = QtGui.QPushButton("Module 1 - Auto Filter", self)
        # self.mb1.clicked.connect(self.getDirectory)
        self.mb1.resize(200, 50)
        self.mb1.move(25, 250)
        self.mb1.setEnabled(False)

        # Module 1 Label
        self.m1s = QtGui.QLabel(self)
        self.m1s.setText("Not Run")
        self.m1s.resize(100, 50)
        self.m1s.move(240, 250)
        self.m1s.setStyleSheet('color: red')

        # Module 2 Button
        self.mb2 = QtGui.QPushButton("Module 2 - Human Filter", self)
        # self.mb1.clicked.connect(self.getDirectory)
        self.mb2.resize(200, 50)
        self.mb2.move(25, 300)
        self.mb2.setEnabled(False)

        # Module 2 Label
        self.m2s = QtGui.QLabel(self)
        self.m2s.setText("Not Run")
        self.m2s.resize(100, 50)
        self.m2s.move(240, 300)
        self.m2s.setStyleSheet('color: red')

        # Module 3 Button
        self.mb3 = QtGui.QPushButton("Module 3 - Locate IR Pts", self)
        # self.mb1.clicked.connect(self.getDirectory)
        self.mb3.resize(200, 50)
        self.mb3.move(25, 350)
        self.mb3.setEnabled(False)

        # Module 3 Label
        self.m3s = QtGui.QLabel(self)
        self.m3s.setText("Not Run")
        self.m3s.resize(100, 50)
        self.m3s.move(240, 350)
        self.m3s.setStyleSheet('color: red')

        # Module 4 Button
        self.mb4 = QtGui.QPushButton("Module 4 - Plot On Map", self)
        # self.mb1.clicked.connect(self.getDirectory)
        self.mb4.resize(200, 50)
        self.mb4.move(25, 400)
        self.mb4.setEnabled(False)

        # Module 4 Label
        self.m4s = QtGui.QLabel(self)
        self.m4s.setText("Not Run")
        self.m4s.resize(100, 50)
        self.m4s.move(240, 400)
        self.m4s.setStyleSheet('color: red')

        # Module AreaPercent Button
        self.mb5 = QtGui.QPushButton("ID Degree of Damage", self)
        # self.mb1.clicked.connect(self.getDirectory)
        self.mb5.resize(200, 50)
        self.mb5.move(450, 250)
        self.mb5.setEnabled(False)

        # Module AreaPercent Label
        self.mscs = QtGui.QLabel(self)
        self.mscs.setText("Not Run")
        self.mscs.resize(100, 50)
        self.mscs.move(670, 250)
        self.mscs.setStyleSheet('color: red')

        # Module 1 Button
        self.mb6 = QtGui.QPushButton("ID Signif Changes", self)
        # self.mb1.clicked.connect(self.getDirectory)
        self.mb6.resize(200, 50)
        self.mb6.move(450, 400)
        self.mb6.setEnabled(False)

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

        # Update GUI and unlock certain buttons
        self.dirLabel.setText(self.dir)
        self.mb1.setEnabled(True)  # Auto Filter Button unlock
        self.mb6.setEnabled(True)  # ID Sig Changes Button unlock




def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())


run()