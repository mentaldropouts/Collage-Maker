
from PySide6 import QtCore, QtWidgets, QtGui
import sys, os


class FilesUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Add widgets to the second UI
        label = QtWidgets.QLabel('Files', self)

        # Set layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(label)
