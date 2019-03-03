from PyQt5 import QtWidgets
import os
import shutil
from os.path import isfile, join


def startupCheck(self, jsondir):
    """
    Checks for existing session files and prompts the user on any action

    :param self: The QT session
    :param jsondir: The path to the images
    :return:
    """

    if not any(isfile(join(jsondir, i)) for i in os.listdir(jsondir)):
        return

    msg = "A session is already open / has not been closed. Do you want to " + \
          "DELETE these files? Selecting no will allow you to continue"
    reply = QtWidgets.QMessageBox.question(self, 'Message', msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

    if reply == QtWidgets.QMessageBox.Yes:
        msg = "ARE YOU SURE YOU WANT TO RESTART THE SESSION"
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                               msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            shutil.rmtree(jsondir)
