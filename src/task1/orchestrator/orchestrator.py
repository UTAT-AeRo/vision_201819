import json
import sys
import threading
from PyQt5 import QtWidgets
import os
import mainWindowLayout
import session

# Constants
jsondir = "./tmp/json/"
flattenedOutputFolder = "./tmp/flattened"
autoFilterOutputPath = jsondir + "autofilter.json"
manualFilterOutputPath = jsondir + "manualfilter.json"
irLocateOutputPath = jsondir + "irlocate.json"
idSigChangesOutputPath = jsondir + "significantchanges.json"
removeDupOutputPath = jsondir + "removeduplicates.json"
sortOutputPath = jsondir + "sortimages.json"
allPoisOutPutPath = jsondir + "pois.json"

# Main Window
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # Initialize Variables
        self.dir = ""
        self.exitRequested = False

        # Initialize Window
        super(MainWindow, self).__init__()
        self.setGeometry(50, 50, 625, 900)
        self.setWindowTitle("AeRo Task 1 Program")
        mainWindowLayout.drawHome(self)
        mainWindowLayout.drawTask1(self)
        self.show()
        session.startupCheck(self, jsondir)

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
        if os.path.isfile(
                autoFilterOutputPath) and not self.manualfilterButton.isEnabled():
            self.manualfilterButton.setEnabled(
                True)  # Manual Filter Button unlock
            updateTextCompletedGreen(self.autofilterLabel)

        if os.path.isfile(
                manualFilterOutputPath) and not self.locateIRButton.isEnabled():
            self.locateIRButton.setEnabled(True)  # Locate IR Button unlock
            updateTextCompletedGreen(self.manualFilterLabel)

        if os.path.isfile(
                irLocateOutputPath) and not self.removeDupButton.isEnabled():
            self.removeDupButton.setEnabled(True)  # Remove duplicate
            updateTextCompletedGreen(self.locateIRLabel)

        if os.path.isfile(
                removeDupOutputPath) and not self.flattenImagesButton.isEnabled():
            self.flattenImagesButton.setEnabled(True)  # Flatten Image
            updateTextCompletedGreen(self.removeDupLabel)

        if os.path.isfile(
                flattenedOutputFolder + "/result.json") and not self.sortImagesButton.isEnabled():
            self.sortImagesButton.setEnabled(True)  # Sort Images
            updateTextCompletedGreen(self.FlattenImagesLabel)

        if (os.path.isfile(sortOutputPath) or os.path.isfile(
                idSigChangesOutputPath)) and not self.plotButton.isEnabled():
            self.plotButton.setEnabled(True)  # Plot Button unlock
            updateTextCompletedGreen(self.sortImagesLabel)

        if not self.exitRequested:
            threading.Timer(0.5, self.mainBGloop).start()

    # Clean up before closing program
    def exitProgram(self):
        self.exitRequested = True
        sys.exit(0)

    # Launches the auto filter module and pipes the output into the current terminal
    def launchAutoFilterModule(self):
        runModule("Module 1 Auto Filtering",
                  "python3 ../filter_module/detect.py -i \"" + self.dir +
                  "\" -f " + autoFilterOutputPath + " -o \"" + jsondir + "\"")

    # Launches the manual filter module and pipes the output into the current terminal
    def launchManualFilterModule(self):
        runModule("Module 2 Manual Filtering",
                  "python3 ../gui_broken_panel_filter/gui_sorter_working.py --from " + autoFilterOutputPath + " --to " + manualFilterOutputPath)

    # Launches the IR location module and pipes the output into the current terminal
    def launchLocateIRModule(self):
        runModule("Module 3 Locate IR",
                  "python3 ../mark_damaged_module/markergui.py -i " + manualFilterOutputPath + " -f " + irLocateOutputPath)

    # Launches the remove duplicate module
    def launchRemoveDupModule(self):
        runModule("Module Remove Duplicates",
                  "python3 ../remove_duplicated_image/remove_duplicated.py " + irLocateOutputPath + " " + removeDupOutputPath + " 5120 5120 0.00001")

    # Launches the flattening module and pipes the output into the current terminal
    def launchFlattenModule(self):
        runModule("Module Flatten Images",
                  "python3 ../../task2/flattening_module/imageflattener.py --input " + removeDupOutputPath + " --output " + flattenedOutputFolder)

    # Launches the Sort damage module
    def launchSortModule(self):
        runModule("Module Degree Damage Images",
                  "python3 ../degree_damage_module/degree_dmg_gui.py -i " + flattenedOutputFolder + "/result.json" + " -f " + sortOutputPath)

    # Launches the point plotting module
    def launchPlottingModule(self):
        if os.path.exists(sortOutputPath) and os.path.exists(idSigChangesOutputPath):
            with open(sortOutputPath, 'r') as fp:
                sorted = json.load(fp)

            with open(idSigChangesOutputPath, 'r') as fp:
                sigChanges=json.load(fp)

            all_pois = {"damaged": sorted["damaged"] + sigChanges["damaged"]}

            with open(allPoisOutPutPath, 'w') as fp:
                json.dump(all_pois, fp)
            runModule("Module Plot points on map",
                      "python3 ../plot_pois/plot_pois.py -im ../map/map_coordinates.json -id " + allPoisOutPutPath + " -pi ../plot_pois/pinpoint.png -ps 0.1")
        elif os.path.exists(sortOutputPath):
            runModule("Module Plot points on map",
                      "python3 ../plot_pois/plot_pois.py -im ../map/map_coordinates.json -id " + sortOutputPath + " -pi ../plot_pois/pinpoint.png -ps 0.1")


    def lauchSigChange(self):
        runModule("Finding significant changes",
                  "python3 ../sig_changes_module/find_sig_changes_gui.py -d " + self.dir + " -f " + idSigChangesOutputPath)


# Runs a module and pipes the output to the current terminal
def runModule(title, cmd):
    print(cmd)
    runningDialog()
    print("\n\n\n\n\n\n=== " + title + " ===")
    os.system(cmd)
    print("=== Output End ===\n\n\n\n\n\n")


# Given a QWidgetLabel, this function will update it to Completed and change the colour to green
def updateTextCompletedGreen(label):
    label.setText("Completed")
    label.setStyleSheet('color: green')


# Pops up a new QMessageBox notifying the user of the running module
def runningDialog():
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)

    msg.setText("The module is about to run")
    msg.setInformativeText(
        "Please check the terminal for module output. The GUI will not respond until the module is "
        "complete. Press OK to start.")
    msg.setWindowTitle("About to start")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    GUI = MainWindow()
    sys.exit(app.exec_())
