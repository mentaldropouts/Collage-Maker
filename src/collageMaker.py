from PySide6 import QtCore, QtWidgets, QtGui
from mainUI import mainUIClass
from FilesUI import filesUIClass
import sys, os

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QtWidgets.QVBoxLayout()
        self.mainUI = mainUIClass()
        self.filesUI = filesUIClass()
        self.widgets = QtWidgets.QTabWidget()

        self.widgets.addTab(self.mainUI, "Home")
        self.widgets.addTab(self.filesUI, "Files")
        
        main_layout.addWidget(self.widgets)
        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()

    sys.exit(app.exec()) 