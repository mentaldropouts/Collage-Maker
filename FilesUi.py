
from PySide6 import QtCore, QtWidgets, QtGui

import sys, os

class CheckBoxListItem(QtWidgets.QWidget):
    # checkedChange = QtCore.pyqtSignal(str)

    def __init__(self, text, checked, row, column):
        super().__init__()
        self.checkbox = QtWidgets.QCheckBox(text)
        self.row = row
        self.column = column
        self.checkbox.stateChanged.connect(lambda state: self.checkboxTester(self.checkbox, row, 0))
        print("State ", self.checkbox.isChecked())  

    def checkboxTester(self, checkbox, row, column):
        if checkbox.isChecked():
            print("Checkbox is checked.", row, column)
        else:
            print("Checkbox is unchecked.", row, column)


class filesUIClass(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.folder_path = "out"
        self.file_watcher = QtCore.QFileSystemWatcher(self)
        self.file_watcher.fileChanged.connect(self.update_table)
        self.initUI()

    

    def initUI(self):
        # Set layout
        layout2 = QtWidgets.QGridLayout(self)
        layout = QtWidgets.QHBoxLayout(self)
        self.files = QtWidgets.QListWidget()
        self.populate_table(self.folder_path)
        self.image_preview_label = QtWidgets.QLabel('Image Preview')
        self.image_preview_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.delete_button = QtWidgets.QPushButton('Delete Selected', self)
        self.delete_button.clicked.connect(self.delete_selected_images)
        layout.addWidget(self.files, 0.5)
        layout.addWidget(self.image_preview_label)
        layout2.addLayout(layout, 0, 0)
        layout2.addWidget(self.delete_button,1,0)
        # self.setLayout(layout2)

        # Slotting the table to watch which item is selected
        # self.files.itemClicked.connect(self.show_image_preview)
        
    

    def update_table(self, path):
        if path == self.folder_path:
            self.populate_table()
    
    def populate_table(self, folder_path):
        # Clear existing items in the table
        if os.path.exists(folder_path):
            # Get a list of files in the selected folder
            files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            # Populate the table with file names and paths
            row = 0
            self.checkBoxes = []
            for file_name in files:
                file_path = os.path.join(folder_path, file_name)
                # Create items for each cell
                listItem = QtWidgets.QListWidgetItem()
                checkBoxItem = CheckBoxListItem(file_path, False, row, 0)
            
                self.files.addItem(listItem)
                self.files.setItemWidget(listItem, checkBoxItem.checkbox)
                row += 1
        else:
            print(f"{folder_path} does not exist yet!")

    def toggle_checkbox(self, row, column):
        print("Starting to toggle checkbox")
        cell_widget = self.files.item(row)
        if cell_widget:
            checkbox = cell_widget.findChild(type(CheckBoxListItem))  # Find the checkbox
            checkbox.toggle()  # Toggle its state
            print("State = " , checkbox.checkbox.isChecked())
            # Optionally display the image associated with the row on check/uncheck 
            if checkbox.checkbox.isChecked():
                self.show_image_preview(row, column)
            else:
                self.image_preview_label.clear()

    def show_image_preview(self, row, column):  # Respond to clicks on any cell in a row
        print("Starting Image Preview")
        file_path_item = self.files.item(row, 0)
        print("showing ", self.files.item(row))
        if file_path_item:
            file_path = file_path_item.text()
    
        selected_items = self.files.selectedItems()
        print(selected_items[0])
        print()
        print()


        if selected_items:
            file_path = selected_items[0].text()  # Assuming the second column contains file paths

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

    def delete_selected_images(self):
        selected_rows = set()
        for row in range(self.files.rowCount()):
            checkbox_item = self.files.cellWidget(row, 0)
            if isinstance(checkbox_item.checkbox,QtWidgets.QCheckBox) and checkbox_item.checkState() == QtCore.Qt.Checked:
                selected_rows.add(row)
        print(selected_rows)
        if selected_rows:
            for row in sorted(selected_rows, reverse=True):
                file_path_item = self.files.item(row, 1)
                if file_path_item:
                    file_path = file_path_item.text()
                    os.remove(file_path)
                    self.files.removeRow(row)
