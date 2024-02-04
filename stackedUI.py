from PySide6 import QtCore, QtWidgets, QtGui
from Firstui import FirstUI
import sys, os

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.MainUI = FirstUI()

        self.stackedWidget = QtWidgets.QStackedWidget(self)
        self.layout = QtWidgets.QBoxLayout()
        self.layout.addWidget(self.MainUI)
        self.stackedWidget.addWidget(self.MainUI)




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()

    sys.exit(app.exec())