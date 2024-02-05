
from PySide6 import QtCore, QtWidgets, QtGui
import sys, os


class filesUIClass(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Add widgets to the second UI
        label = QtWidgets.QLabel('Files', self)

        # Set layout
        layout = QtWidgets.QVBoxLayout(self)
        self.table_widget = QtWidgets.QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(['File Name', 'File Path'])
        self.populate_table('out')
        layout.addWidget(self.table_widget)
        layout.addWidget(label)
        self.setLayout(layout)
    
    def populate_table(self, folder_path):
        # Clear existing items in the table
        self.table_widget.setRowCount(0)

        # Get a list of files in the selected folder
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

        # Populate the table with file names and paths
        for file_name in files:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)

            file_path = os.path.join(folder_path, file_name)

            # Create items for each cell
            file_name_item = QtWidgets.QTableWidgetItem(file_name)
            file_path_item = QtWidgets.QTableWidgetItem(file_path)

            # Set items in the table
            self.table_widget.setItem(row_position, 0, file_name_item)
            self.table_widget.setItem(row_position, 1, file_path_item)
