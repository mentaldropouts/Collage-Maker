
from PySide6 import QtCore, QtWidgets, QtGui

import sys, os


class filesUIClass(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.folder_path = "out"
        self.file_watcher = QtCore.QFileSystemWatcher(self)
        self.file_watcher.fileChanged.connect(self.update_table)
        self.initUI()

    

    def initUI(self):
        # Set layout
        layout = QtWidgets.QHBoxLayout(self)
        self.table_widget = QtWidgets.QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(['File Name', 'File Path'])
        self.table_widget.setMinimumWidth(100)
        self.table_widget.setMaximumWidth(200)
        self.populate_table(self.folder_path)
        self.image_preview_label = QtWidgets.QLabel('Image Preview')
        self.image_preview_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.table_widget, 0.5)
        layout.addWidget(self.image_preview_label)
        self.setLayout(layout)

        # Slotting the table to watch which item is selected
        self.table_widget.itemSelectionChanged.connect(self.show_image_preview)

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

                # Set items in the table
                self.table_widget.setItem(row_position, 0, file_name_item)
                self.table_widget.setItem(row_position, 1, file_path_item)
        else:
            print(f"{folder_path} does not exist yet!")


    def show_image_preview(self):
        selected_items = self.table_widget.selectedItems()
        print(selected_items)
        
        if selected_items:
            file_path = selected_items[1].text()  # Assuming the second column contains file paths

            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
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
