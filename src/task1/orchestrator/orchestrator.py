import sys
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
import os

# Constants
jsondir = "./tmp/json/"
autoFilterOutputPath = jsondir + "autofilter.json"
manualFilterOutputPath = jsondir + "manualfilter.json"
irLocateOutputPath = jsondir + "irlocate.json"
idSigChangesOutputPath = jsondir + "significantchanges.json"

# Main Window
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # Initialize Variables
        self.dir = ""
        self.exitRequested = False

        # Initialize Window
        super(MainWindow, self).__init__()
        self.setGeometry(50, 50, 950, 550)
        self.setWindowTitle("AeRo Task 1 Program")
        self.home()

    def home(self):
        # Quit Button
        btn = QtWidgets.QPushButton("Quit", self)
        btn.clicked.connect(self.exitProgram)
        btn.resize(200, 50)
        btn.move(730, 490)

        # Step 1 Label
        bl = QtWidgets.QLabel(self)
        bl.setText("Step 1 -  select the source image folders")
        bl.resize(600, 50)
        bl.move(25, 20)
        bl.setStyleSheet('color: darkblue')

        # Step 2 Label
        bl = QtWidgets.QLabel(self)
        bl.setText("Step 2 -  Run the modules. Keep in mind to run them in order if applicable")
        bl.resize(600, 50)
        bl.move(25, 200)
        bl.setStyleSheet('color: darkblue')

        # Select Directory Curr Directory
        self.dirLabel = QtWidgets.QLabel(self)
        self.dirLabel.setText(self.dir)
        self.dirLabel.resize(800, 50)
        self.dirLabel.move(230, 100)

        # Select Directory Button
        btn = QtWidgets.QPushButton("Browse For Photo Directory", self)
        btn.clicked.connect(self.getDirectory)
        btn.resize(200, 50)
        btn.move(25, 90)

        self.populateTask1()
        self.show()

    # ugggghhhhh
    def populateTask1(self):
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

    # fetches the director from the user and updates the program accordingly
    def getDirectory(self):
        self.dir = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Open a folder",
            os.getcwd(),
            QtWidgets.QFileDialog.ShowDirsOnly)

        # Update GUI and unlock certain buttons
        self.dirLabel.setText(self.dir)
        self.autofilterButton.setEnabled(True)  # Auto Filter Button unlock
        self.idSigChangesButton.setEnabled(True)  # ID Sig Changes Button unlock

        # Start the main loop
        self.mainBGloop()

    # The main loop that is in charge of periodically checking the status of the json files and updating the interface accordingly
    # I know its not safe to change these buttons from a thread but I don't want to dive into signals right now
    def mainBGloop(self):
        if os.path.isfile(autoFilterOutputPath) and not self.manualfilterButton.isEnabled():
            self.manualfilterButton.setEnabled(True)  # Manual Filter Button unlock
            updateTextCompletedGreen(self.autofilterLabel)

        if os.path.isfile(manualFilterOutputPath) and not self.locateIRButton.isEnabled():
            self.locateIRButton.setEnabled(True)  # Locate IR Button unlock
            updateTextCompletedGreen(self.manualFilterLabel)

        if os.path.isfile(irLocateOutputPath) and not self.flattenImagesButton.isEnabled():
            self.flattenImagesButton.setEnabled(True) # Flatten Image
            updateTextCompletedGreen(self.manualFilterLabel)

        if os.path.isfile(irLocateOutputPath) and os.path.isfile(idSigChangesOutputPath) and not self.plotButton.isEnabled():
            self.plotButton.setEnabled(True)  # Plot Button unlock
            updateTextCompletedGreen(self.manualFilterLabel)

        if True and not self.plotButton.isEnabled():  # DEBUG
            self.plotButton.setEnabled(True)
            updateTextCompletedGreen(self.manualFilterLabel)

        if not self.exitRequested:
            threading.Timer(0.5, self.mainBGloop).start()

    # Clean up before closing program
    def exitProgram(self):
        self.exitRequested = True
        sys.exit(0)

    # Launches the auto filter module and pipes the output into the current terminal
    def launchAutoFilterModule(self):
        runModule("Module 1 Auto Filtering",
                  "python3 ../filter-module/detect.py -i " + self.dir + " -f " + autoFilterOutputPath)

    # Launches the manual filter module and pipes the output into the current terminal
    def launchManualFilterModule(self):
        runModule("Module 2 Manual Filtering",
                  "python3 ../gui_broken_panel_filter/gui_sorter_working.py --from " + autoFilterOutputPath + " --to " + manualFilterOutputPath)

    # Launches the IR location module and pipes the output into the current terminal
    def launchLocateIRModule(self):
        runModule("Module 3 Locate IR",
                  "python3 ../mark-damaged-module/markergui.py -i " + manualFilterOutputPath + " -o " + irLocateOutputPath)

    # Launches the point plotting module
    def launchPlottingModule(self):
        runModule("Module 4 Plot points on map",
                  "python3 ../plot_pois/plot_pois.py -im ../map/map_coordinates.json -id " + irLocateOutputPath + " -pi ../plot_pois/pinpoint.png -ps 1")


# Runs a module and pipes the output to the current terminal
def runModule(title, cmd):
    runningDialog()
    print("\n\n\n\n\n\n=== " + title + " ===")
    os.system(cmd)
    print("=== Output End ===\n\n\n\n\n\n")

# Given a QWidgetLabel, sets the label to not run
def setNotRunLabel(l):
    l.setText("Not Run")
    l.resize(100, 50)
    l.setStyleSheet('color: red')

# Given a QWidgetButton, sets the properties of the button for the start of the program
def setModuleButtonProperties(b):
    b.resize(200, 50)
    b.setEnabled(False)

# Given a QWidgetLabel, this function will update it to Completed and change the colour to green
def updateTextCompletedGreen(label):
    label.setText("Completed")
    label.setStyleSheet('color: green')

# Pops up a new QMessageBox notifying the user of the running module
def runningDialog():
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)

    msg.setText("The module is running")
    msg.setInformativeText("Please check the terminal for module output")
    msg.setWindowTitle("Running")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    GUI = MainWindow()
    sys.exit(app.exec_())