from PyQt5 import QtWidgets

leftLabelPos = 240
leftButtonPos = 25

def drawHome(window):
    """
    Draws the home layout

    :param window: The QT session
    :return:
    """

    # Quit Button
    btn = QtWidgets.QPushButton("Quit", window)
    btn.clicked.connect(window.exitProgram)
    btn.resize(400, 50)
    btn.move(80, 750)

    # Step 1 Label
    bl = QtWidgets.QLabel(window)
    bl.setText("Step 1 -  select the source image folders")
    bl.resize(600, 50)
    bl.move(leftButtonPos, 20)
    bl.setStyleSheet('color: darkblue')

    # Step 2 Label
    bl = QtWidgets.QLabel(window)
    bl.setText("Step 2 -  Run the modules. Keep in mind to run them in order if applicable")
    bl.resize(600, 50)
    bl.move(leftButtonPos, 200)
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
    btn.move(leftButtonPos, 90)

def drawTask1(window):
    """
    Draws the home layout

    :param window: The QT session
    :return:
    """
    # Module 1 Button
    window.autofilterButton = QtWidgets.QPushButton("Auto Filter", window)
    window.autofilterButton.clicked.connect(window.launchAutoFilterModule)
    window.autofilterButton.move(leftButtonPos, 250)
    setModuleButtonProperties(window.autofilterButton)

    # Module 1 Label
    window.autofilterLabel = QtWidgets.QLabel(window)
    window.autofilterLabel.move(leftLabelPos, 250)
    setNotRunLabel(window.autofilterLabel)

    # ID Changes Button
    window.idSigChangesButton = QtWidgets.QPushButton("ID Signif Changes", window)
    window.idSigChangesButton.move(325, 300)
    setModuleButtonProperties(window.idSigChangesButton)

    # ID Changes Label
    window.idSigChangesLabel = QtWidgets.QLabel(window)
    setNotRunLabel(window.idSigChangesLabel)
    window.idSigChangesLabel.move(545, 300)

    # Module 2 Button
    window.manualfilterButton = QtWidgets.QPushButton("Human Filter", window)
    window.manualfilterButton.clicked.connect(window.launchManualFilterModule)
    window.manualfilterButton.move(leftButtonPos, 300)
    setModuleButtonProperties(window.manualfilterButton)

    # Module 2 Label
    window.manualFilterLabel = QtWidgets.QLabel(window)
    window.manualFilterLabel.move(leftLabelPos, 300)
    setNotRunLabel(window.manualFilterLabel)

    # Module 3 Button
    window.locateIRButton = QtWidgets.QPushButton("Locate IR Pts", window)
    window.locateIRButton.clicked.connect(window.launchLocateIRModule)
    window.locateIRButton.move(leftButtonPos, 350)
    setModuleButtonProperties(window.locateIRButton)

    # Module 3 Label
    window.locateIRLabel = QtWidgets.QLabel(window)
    window.locateIRLabel.move(leftLabelPos, 350)
    setNotRunLabel(window.locateIRLabel)

    # Module FlattenImages Button
    window.flattenImagesButton = QtWidgets.QPushButton("Flatten Images", window)
    window.flattenImagesButton.move(leftButtonPos, 400)
    setModuleButtonProperties(window.flattenImagesButton)

    # Module FlattenImages Label
    window.FlattenImagesLabel = QtWidgets.QLabel(window)
    window.FlattenImagesLabel.move(leftLabelPos, 400)
    setNotRunLabel(window.FlattenImagesLabel)

    # Remove Dup Img Butt
    window.removeDupButton = QtWidgets.QPushButton("Remove Duplicate Images", window)
    window.removeDupButton.move(leftButtonPos, 450)
    window.removeDupButton.clicked.connect(window.launchPlottingModule)
    setModuleButtonProperties(window.removeDupButton)

    # Remove Dup Img Label
    window.removeDupLabel = QtWidgets.QLabel(window)
    window.removeDupLabel.move(leftLabelPos, 450)
    setNotRunLabel(window.removeDupLabel)

    # Module AreaPercent Button
    window.sortImagesButton = QtWidgets.QPushButton("Sort Images", window)
    window.sortImagesButton.move(leftButtonPos, 500)
    setModuleButtonProperties(window.sortImagesButton)

    # Module AreaPercent Label
    window.sortImagesLabel = QtWidgets.QLabel(window)
    window.sortImagesLabel.move(leftLabelPos, 500)
    setNotRunLabel(window.sortImagesLabel)

    # Module 4 Button
    window.plotButton = QtWidgets.QPushButton("Plot On Map", window)
    window.plotButton.move(80, 600)
    window.plotButton.clicked.connect(window.launchPlottingModule)
    setModuleButtonProperties(window.plotButton)
    window.plotButton.resize(400, 50)


# Given a QWidgetLabel, sets the label to not run
def setNotRunLabel(l):
    l.setText("Not Run")
    l.resize(100, 50)
    l.setStyleSheet('color: red')


# Given a QWidgetButton, sets the properties of the button for the start of the program
def setModuleButtonProperties(b):
    b.resize(200, 50)
    b.setEnabled(False)
