
from PySide6 import QtCore, QtWidgets, QtGui

import sys, os

class CheckBoxTableWidgetItem(QtWidgets.QTableWidgetItem):
    statechanged = QtCore.Signal("stateChanged")

    def __init__(self, checked=False):

        super(CheckBoxTableWidgetItem, self).__init__()
        self.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        self.setCheckState(QtCore.Qt.Checked if checked else QtCore.Qt.Unchecked)

        print(self.checkState())
        
    def check_item_state(self):
        state = self.checkState()
        if state == QtCore.Qt.Checked:
            print("The item is checked")
        elif state == QtCore.Qt.Unchecked:
            print("The item is unchecked")
        else:
            print("The item is in a partially checked state") 


class filesUIClass(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.folder_path = "result"
        self.file_watcher = QtCore.QFileSystemWatcher(self)
        self.file_watcher.addPath(self.folder_path)
        self.file_watcher.fileChanged.connect(self.update_table)
        self.initUI()

    def on_state_changed(state):
        if state == QtCore.Qt.Checked:
            print("Checkbox state changed: Checked")
        elif state == QtCore.Qt.Unchecked:
            print("Checkbox state changed: Unchecked")
        else:
            print("Checkbox state changed: Partially checked")

    def initUI(self):
        # Set layout
        layout2 = QtWidgets.QGridLayout(self)
        layout = QtWidgets.QHBoxLayout(self)
        self.table_widget = QtWidgets.QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(['', 'File Path'])
        self.table_widget.setColumnWidth(0, 20)
        self.table_widget.setMinimumWidth(100)
        self.table_widget.setMaximumWidth(500)

        self.populate_table(self.folder_path)
        self.table_widget.cellClicked.connect(lambda row, column: self.show_image_preview(row,column))

        self.image_preview_label = QtWidgets.QLabel('Image Preview')
        self.image_preview_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.delete_button = QtWidgets.QPushButton('Delete Selected', self)
        self.delete_button.clicked.connect(self.delete_selected_images)
        layout.addWidget(self.table_widget, 0.5)
        layout.addWidget(self.image_preview_label)
        layout2.addLayout(layout, 0, 0)
        layout2.addWidget(self.delete_button,1,0)
        self.setLayout(layout2)

        # Slotting the table to watch which item is selected
        # TODO Add lambda functionality to slot showing image preview with clicking file name
        # and toggle_checkbox with clicking the checkbox

    def update_table(self, path):
        if path == self.folder_path:
            self.populate_table()
    
    def populate_table(self, folder_path):
        # Clear existing items in the table
        self.table_widget.setRowCount(0)
        if os.path.exists(folder_path):
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


                # Create a checkbox item for each row
                checkbox_item = CheckBoxTableWidgetItem(checked=False)
                # checkbox_item.stateChanged.con÷nect(lambda state: checkbox_item.check_item_state())

                self.table_widget.setItem(row_position, 0, checkbox_item)

                # Set items in the table
                # self.table_widget.setItem(row_position, 1, file_name_item)
                self.table_widget.setItem(row_position, 1, file_path_item)
        else:
            print(f"{folder_path} does not exist yet!")

    def show_image_preview(self, row, column):
        file_path = self.table_widget.item(row, column).text()
        if file_path :
            print(file_path)
            if file_path.lower().endswith(('.webp','.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                pixmap = QtGui.QPixmap(file_path)
           # Get the current size of the pixmap
                current_width = pixmap.width()
                current_height = pixmap.height()
                # Get the target size (max_width, max_height)
                max_width = self.image_preview_label.width()
                max_height = self.image_preview_label.height()

                # Calculate the scaling factors for width and height
                width_scale_factor = max_width / current_width
                height_scale_factor = max_height / current_height

                # Use the minimum scale factor to maintain aspect ratio
                scale_factor = min(width_scale_factor, height_scale_factor)

                # Calculate the new size after scaling
                new_width = int(current_width * scale_factor)
                new_height = int(current_height * scale_factor)

                # Scale the pixmap
                pixmap = pixmap.scaled(new_width, new_height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

                self.image_preview_label.setPixmap(pixmap)
                self.image_preview_label.setScaledContents(True)
            else:
                self.image_preview_label.clear()

    def delete_selected_images(self):
        selected_rows = set()
        for row in range(self.table_widget.rowCount()):
            checkbox_item = self.table_widget.cellWidget(row, 0)
            if isinstance(checkbox_item, QtWidgets.QCheckBox) and checkbox_item.checkState() == QtCore.Qt.Checked:
                selected_rows.add(row)
        print(selected_rows)
        if selected_rows:
            for row in sorted(selected_rows, reverse=True):
                file_path_item = self.table_widget.item(row, 1)
                if file_path_item:
                    file_path = file_path_item.text()
                    os.remove(file_path)
                    self.table_widget.removeRow(row)
