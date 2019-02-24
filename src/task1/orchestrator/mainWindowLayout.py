from PyQt5 import QtWidgets

def drawHome(window):
    # Quit Button
    btn = QtWidgets.QPushButton("Quit", window)
    btn.clicked.connect(window.exitProgram)
    btn.resize(200, 50)
    btn.move(730, 490)

    # Step 1 Label
    bl = QtWidgets.QLabel(window)
    bl.setText("Step 1 -  select the source image folders")
    bl.resize(600, 50)
    bl.move(25, 20)
    bl.setStyleSheet('color: darkblue')

    # Step 2 Label
    bl = QtWidgets.QLabel(window)
    bl.setText("Step 2 -  Run the modules. Keep in mind to run them in order if applicable")
    bl.resize(600, 50)
    bl.move(25, 200)
    bl.setStyleSheet('color: darkblue')

    # Select Directory Curr Directory
    window.dirLabel = QtWidgets.QLabel(window)
    window.dirLabel.setText(window.dir)
    window.dirLabel.resize(800, 50)
    window.dirLabel.move(230, 100)

    # Select Directory Button
    btn = QtWidgets.QPushButton("Browse For Photo Directory", window)
    btn.clicked.connect(window.getDirectory)
    btn.resize(200, 50)
    btn.move(25, 90)

def drawTask1(self):
    # Module 1 Button
    self.autofilterButton = QtWidgets.QPushButton("Module 1 - Auto Filter", self)
    self.autofilterButton.clicked.connect(self.launchAutoFilterModule)
    self.autofilterButton.move(25, 250)
    setModuleButtonProperties(self.autofilterButton)

    # Module 1 Label
    self.autofilterLabel = QtWidgets.QLabel(self)
    self.autofilterLabel.move(240, 250)
    setNotRunLabel(self.autofilterLabel)

    # ID Changes Button
    self.idSigChangesButton = QtWidgets.QPushButton("ID Signif Changes", self)
    self.idSigChangesButton.move(325, 250)
    setModuleButtonProperties(self.idSigChangesButton)

    # ID Changes Label
    self.idSigChangesLabel = QtWidgets.QLabel(self)
    setNotRunLabel(self.idSigChangesLabel)
    self.idSigChangesLabel.move(545, 250)

    # Module 2 Button
    self.manualfilterButton = QtWidgets.QPushButton("Module 2 - Human Filter", self)
    self.manualfilterButton.clicked.connect(self.launchManualFilterModule)
    self.manualfilterButton.move(25, 300)
    setModuleButtonProperties(self.manualfilterButton)

    # Module 2 Label
    self.manualFilterLabel = QtWidgets.QLabel(self)
    self.manualFilterLabel.move(240, 300)
    setNotRunLabel(self.manualFilterLabel)

    # Module 3 Button
    self.locateIRButton = QtWidgets.QPushButton("Module 3 - Locate IR Pts", self)
    self.locateIRButton.clicked.connect(self.launchLocateIRModule)
    self.locateIRButton.move(25, 350)
    setModuleButtonProperties(self.locateIRButton)

    # Module 3 Label
    self.locateIRLabel = QtWidgets.QLabel(self)
    self.locateIRLabel.move(240, 350)
    setNotRunLabel(self.locateIRLabel)

    # Module FlattenImages Button
    self.flattenImagesButton = QtWidgets.QPushButton("Flatten Images", self)
    self.flattenImagesButton.move(325, 350)
    setModuleButtonProperties(self.flattenImagesButton)

    # Module FlattenImages Label
    self.FlattenImagesLabel = QtWidgets.QLabel(self)
    self.FlattenImagesLabel.move(545, 350)
    setNotRunLabel(self.FlattenImagesLabel)

    # Module AreaPercent Button
    self.sortImagesButton = QtWidgets.QPushButton("Sort Images Top 3", self)
    self.sortImagesButton.move(625, 350)
    setModuleButtonProperties(self.sortImagesButton)

    # Module AreaPercent Label
    self.sortImagesLabel = QtWidgets.QLabel(self)
    self.sortImagesLabel.move(845, 350)
    setNotRunLabel(self.sortImagesLabel)

    # Module 4 Button
    self.plotButton = QtWidgets.QPushButton("Module 4 - Plot On Map", self)
    self.plotButton.move(25, 400)
    self.plotButton.clicked.connect(self.launchPlottingModule)
    setModuleButtonProperties(self.plotButton)

    # Module 4 Label
    self.plotLabel = QtWidgets.QLabel(self)
    self.plotLabel.move(240, 400)
    self.plotLabel.resize(400, 50)
    self.plotLabel.setStyleSheet('color: red')
    self.plotLabel.setText("Not Run (also requires ID Signif Changes to be completed)")


# Given a QWidgetLabel, sets the label to not run
def setNotRunLabel(l):
    l.setText("Not Run")
    l.resize(100, 50)
    l.setStyleSheet('color: red')


# Given a QWidgetButton, sets the properties of the button for the start of the program
def setModuleButtonProperties(b):
    b.resize(200, 50)
    b.setEnabled(False)
