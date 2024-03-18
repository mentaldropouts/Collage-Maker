import sys
import random
from time import sleep
from PySide6 import QtCore, QtWidgets, QtGui
from main import mainDriver


from Gdriver import GoogleDriver, delete_folders
from PDriver import PinterestDriver
from remover import RemoveDriver
from collage import CollageDriver
import os

class mainUIClass(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # If out and result are not made, make them
        if os.path.exists('out') == False:
            os.mkdir('out')
        if os.path.exists('result') == False:
            os.mkdir('result')

        # Initial States
        self.pinKey = "People"
        self.numImages = 20
        sampleStartDate = QtCore.QDate(2023, 10, 18)
        sampleEndDate = QtCore.QDate(2023, 11, 18)

        self.driver = mainDriver()
        self.layout = QtWidgets.QGridLayout(self)

        {
        # self.credButton = QtWidgets.QPushButton("Choose Google Credentials")
        # self.layout.addWidget(self.credButton, 0,0, 1,1)
        # Configuring Toggle Group 
        # self.toggleGroup = QtWidgets.QGridLayout()
        # self.weightsToggler = QtWidgets.QCheckBox("Use Weights")
        # self.cropToggler = QtWidgets.QCheckBox("Crop Bounding Boxes")
        }

        self.titleLayout = QtWidgets.QHBoxLayout()
        self.title = QtWidgets.QLabel("Collage Maker")
        self.loadedLabel = QtWidgets.QLabel("None")
        self.titleLayout.addWidget(self.title)
        self.titleLayout.addWidget(self.loadedLabel)

        self.googleLayout = QtWidgets.QGridLayout()
        self.googleLayout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.searchGoogle = QtWidgets.QCheckBox("Search Google Photos")
        credsLabel = QtWidgets.QLabel("*requires credentials")
        startDateText = QtWidgets.QLabel("Start Date:")
        endDateText = QtWidgets.QLabel("End Date:")
        self.endDateBox = QtWidgets.QDateEdit(sampleEndDate)
        self.startDateBox = QtWidgets.QDateEdit(sampleStartDate) 
        # Adding items to Google Layout
        self.googleLayout.addWidget(self.searchGoogle,0,0)
        self.googleLayout.addWidget(credsLabel,1,0)
        self.googleLayout.addWidget(startDateText,2,0)
        self.googleLayout.addWidget(self.startDateBox,2,1)
        self.googleLayout.addWidget(endDateText,3,0)
        self.googleLayout.addWidget(self.endDateBox,3,1)
        self.clearButton = QtWidgets.QPushButton("clear")
        self.pinterestLayout = QtWidgets.QGridLayout()
        self.searchPinterest = QtWidgets.QCheckBox("Search Pinterest")
        self.pinterestSearchButton = QtWidgets.QPushButton("Search")
        KeywordText = QtWidgets.QLabel("Keyword:")
        self.pinKeyword = QtWidgets.QLineEdit("People")
        numImagesText = QtWidgets.QLabel("Number of Images:")
        self.numImagesBox = QtWidgets.QComboBox(self)
        # Making combo box for number of images
        for i in range(10, 201, 10):
            self.numImagesBox.addItem(str(i))

        # Adding items to the Pinterest Layout
        self.pinterestLayout.addWidget(self.searchPinterest,0,0)
        self.pinterestLayout.addWidget(KeywordText,1,0)
        self.pinterestLayout.addWidget(self.pinKeyword)
        self.pinterestLayout.addWidget(numImagesText)
        self.pinterestLayout.addWidget(self.numImagesBox)
        self.pinterestLayout.addWidget(self.pinterestSearchButton)
    

        # self.removeBackImages = QtWidgets.QCheckBox("Remove Back Images")

        # Updates the indicator at start
        self.loadedIndicater()

        # Configuring Footer
        self.footer = QtWidgets.QHBoxLayout()
        self.chooseFiles = QtWidgets.QPushButton("Choose Files")
        self.startButton = QtWidgets.QPushButton("Start")
        self.heightBox = QtWidgets.QLineEdit("500")
        self.widthBox = QtWidgets.QLineEdit("500") 
        self.numLayersBox = QtWidgets.QLineEdit("20")
        self.spacingBox = QtWidgets.QLineEdit("10")
        heightText = QtWidgets.QLabel("Height:")
        widthText = QtWidgets.QLabel("Width:")
        numLayersText = QtWidgets.QLabel("Number of Layers:")
        spacingText = QtWidgets.QLabel("Spacing:")
        
        self.footer.addWidget(heightText)
        self.footer.addWidget(self.heightBox)
        self.footer.addWidget(widthText)
        self.footer.addWidget(self.widthBox)
        self.footer.addWidget(numLayersText)
        self.footer.addWidget(self.numLayersBox)
        self.footer.addWidget(spacingText)
        self.footer.addWidget(self.spacingBox)
        self.footer.addWidget(self.chooseFiles)
        self.footer.addWidget(self.startButton)

        # self.footer.addWidget(self.clearButton)

        # Configuring Preview
        self.imageDisplay = QtWidgets.QGraphicsView()
        self.imagePreview = QtWidgets.QLabel()
        self.imagePreview.setScaledContents(True)
        self.imagePreview.setAlignment(QtCore.Qt.AlignCenter)
        self.imagePreview.setPixmap(QtGui.QPixmap("test.jpg"))

        # Configuring Layouts
        self.layout.addLayout(self.titleLayout,0,0)
        self.BodyLayout = QtWidgets.QHBoxLayout()
        self.BodyLayout.addLayout(self.googleLayout)
        self.BodyLayout.addLayout(self.pinterestLayout)
        self.layout.addLayout(self.BodyLayout,1,0)
        self.layout.addLayout(self.footer, 4, 0, QtCore.Qt.AlignCenter)

        # Connecting buttons to function
        self.heightBox.textChanged.connect(self.handleChangeinHeight)
        self.widthBox.textChanged.connect(self.handleChangeinWidth)
        self.numLayersBox.textChanged.connect(self.handleChangeinNumLayers)
        self.spacingBox.textChanged.connect(self.handleChangeinSpacing)
        self.searchGoogle.stateChanged.connect(self.toggleSearchGoogle)
        self.searchPinterest.stateChanged.connect(self.toggleSearchPinterest)

        self.startButton.clicked.connect(self.toggleStartButton)
        self.startDateBox.dateChanged.connect(self.updateDate)
        self.endDateBox.dateChanged.connect(self.updateDate)
        self.pinKeyword.textChanged.connect(self.updateKey)
        self.searchGoogle.stateChanged.connect(self.showFiles)
        self.numImagesBox.currentIndexChanged.connect(self.updateNumImages)
        self.clearButton.clicked.connect(self.clearFolders)
        self.pinterestSearchButton.clicked.connect(self.searchP)
        # self.googleSearchButton.clicked.connect(GoogleDriver)

    # Function for the Search Pinterest Button
    def searchP(self):
        self.loadedIndicater()
        if self.driver.searchPinterest == True:
            PinterestDriver(out=self.driver.imageDir, key=self.pinKey, threads=10, images=self.numImages)
        if len(os.listdir('out')) != 0:
            RemoveDriver(dir=self.driver.imageDir,typeOfImages="person", useWeights=self.driver.weights, crop=self.driver.cropBoundingBoxes)
        self.loadedIndicater()
        
    # Functionality that is called when the choose credentials button is clicked
    def showFiles(self):
        if self.searchGoogle.isChecked() and self.driver.credsLoaded == False:
            fileDialog = QtWidgets.QFileDialog()
            fileDialog.setNameFilter("JSON files (*.json);;All files (*)")
            selected_file = None
            if fileDialog.exec():
                # Get the selected file name
                selected_file = fileDialog.selectedFiles() 
                print(f'Selected File: {selected_file}')
                if selected_file[0].split('.')[-1] == 'json':
                    print("Current Credentials are json files!")
                    self.driver.credsLoaded = True
                    # Checking the Check Box on the UI
                    self.driver.searchForImages = self.searchGoogle.isChecked()
                elif selected_file == None:
                    print("ERROR: Current Credentials are not json files!")
                    self.driver.credsLoaded = False
                    self.searchGoogle.setChecked(False)
                return
        
    # Functionality that handles date chages  
    def updateDate(self):
            self.startDate = [self.startDateBox.date().year(), self.startDateBox.date().month(), self.startDateBox.date().day()]
            self.endDate = [self.endDateBox.date().year(), self.endDateBox.date().month(), self.endDateBox.date().day()]
            self.dateFilter = {
                "startDate": {"year": self.startDate[0], "month": self.startDate[1], "day": self.startDate[2]},
                "endDate": {"year": self.endDate[0], "month": self.endDate[1], "day": self.endDate[2]}
            }

            # print("start:", self.startDate)
            # print("end:", self.endDate)

    def updateKey(self):
        self.pinKey = self.pinKeyword.text()
        # print("PinKey = ", self.pinKey)

    # Getting the number of images for pinterest to search
    def updateNumImages(self):
        self.numImages = int(self.numImagesBox.currentText())
        print("Looking for ", self.numImages, " on Pinterest")

    # Functionality updates the indicator for loaded pictures
    def loadedIndicater(self):
        print("Starting Load Indicator")
        sleep(0.5)
        if self.driver.searching:
            self.loadedLabel.setText("Searching")
            self.loadedLabel.setStyleSheet("background-color: Aquamarine;")
        elif self.driver.removing == True:
            print("Removing state")
            self.loadedLabel.setText("Removing")
            self.loadedLabel.setStyleSheet("background-color: indigo;")
        elif len(os.listdir('result')) != 0  and self.driver.removing == False and self.driver.searching == False:
            self.loadedLabel.setText("Loaded")
            self.loadedLabel.setStyleSheet("background-color: orange;")
        elif os.path.exists('test.png') and os.path.exists('out') == False and os.path.exists('result') and self.driver.removing == False:
            self.loadedLabel.setText("Done")
            self.loadedLabel.setStyleSheet("background-color: green;")
        elif len(os.listdir('out')) == 0 and len(os.listdir('result')) == 0:
            self.loadedLabel.setText("Not Loaded")
            self.loadedLabel.setStyleSheet("background-color: red;")

    # Functionality that is called when the start button is clicked
    def start(self):
        print("starting")
        if self.driver.searchForImages or self.driver.searchPinterest: 
            self.driver.searching == True
        self.loadedIndicater()
        if self.driver.startButton:
            if self.driver.searchForImages:
                # print("Data Filter =", self.dateFilter)
                GoogleDriver(dateFilter=self.dateFilter, contentFilter=self.driver.contentFilter, layeredSearch=True)
                # Changing States
                self.driver.searching == False
                self.loadedIndicater()
            if self.driver.searchPinterest:
                PinterestDriver(out=self.driver.imageDir, key=self.pinKey, threads=10, images=self.numImages)
                # Changing States
                self.driver.searching == False
                self.loadedIndicater()

            self.driver.removing = True
            RemoveDriver(dir=self.driver.imageDir,typeOfImages="person", useWeights=self.driver.weights, crop=self.driver.cropBoundingBoxes)
            self.driver.removing = False

            # Creates the collage
            self.loadedIndicater()
            CollageDriver(height=self.driver.height, width=self.driver.width, 
                          numLayers=self.driver.numLayers, spacing=self.driver.spacing,
                          useWeights=self.driver.weights)
            print("Finished Collage Driver!")
            self.loadedIndicater()

    def clearFolders(self):
        delete_folders('out/')
        delete_folders('result/')

    def toggleWeights(self):
        self.driver.weights = self.weightsToggler.isChecked()
        print("toggledWeights: ", self.driver.weights)
    def toggleCrop(self):
        self.driver.cropBoundingBoxes = self.cropToggler.isChecked()
        print("toggledCrop: ", self.driver.cropBoundingBoxes)

    def toggleSearchGoogle(self):
        self.driver.searchForImages = self.searchGoogle.isChecked()
        print("toggledSearchForImages: ", self.driver.searchForImages)

    def toggleSearchPinterest(self):
        print("Starting Pinterest Search")
        self.driver.searchPinterest = self.searchPinterest.isChecked()
        print("toggledSearchPinterest: ", self.driver.searchPinterest)

    def toggleStartButton(self):
        self.driver.startButton = True
        print("toggledStarButton: ", self.driver.startButton)
        self.start()
        self.driver.startButton = FalsestartButton = False
    
    def handleChangeinHeight(self):
        print("Height is now", self.driver.height)
        self.driver.height = int(self.heightBox.text())

    def handleChangeinWidth(self):
        self.driver.width = int(self.widthBox.text())

    def handleChangeinNumLayers(self):
        self.driver.numLayers = int(self.numLayersBox.text())

    def handleChangeinSpacing(self):
        self.driver.spacing = int(self.spacingBox.text())

# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     ui = MainWindow()
#     ui.show()

#     sys.exit(app.exec())
