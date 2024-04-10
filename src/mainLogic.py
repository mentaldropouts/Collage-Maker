import sys
import random
from time import sleep
from PySide6 import QtCore, QtWidgets, QtGui
from mainStates import mainDriver

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
        self.credsSearchText = QtWidgets.QLabel("Credentials Not Loaded")
        self.credsSearchButton = QtWidgets.QPushButton(text="Browse")
        # credsLabel = QtWidgets.QLabel("*requires credentials")
        startDateText = QtWidgets.QLabel("Start Date:")
        endDateText = QtWidgets.QLabel("End Date:")
        self.endDateBox = QtWidgets.QDateEdit(sampleEndDate)
        self.startDateBox = QtWidgets.QDateEdit(sampleStartDate) 

        # Adding items to Google Layout
        self.googleLayout.addWidget(self.searchGoogle,0,0)
        self.googleLayout.addWidget(self.credsSearchText, 1, 0)
        self.googleLayout.addWidget(self.credsSearchButton, 1, 1)
        # self.googleLayout.addWidget(credsLabel,1,0)
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
    
        # Configuring Footer
        self.footer = QtWidgets.QHBoxLayout()
        self.chooseFiles = QtWidgets.QPushButton("Choose Files")
        self.startButton = QtWidgets.QPushButton("Start")
        self.heightBox = QtWidgets.QLineEdit(str(self.driver.height))
        self.widthBox = QtWidgets.QLineEdit(str(self.driver.weights)) 
        self.numLayersBox = QtWidgets.QLineEdit(str(self.driver.numLayers))
        self.spacingBox = QtWidgets.QLineEdit(str(self.driver.spacing))
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

        # Configuring Preview
        self.imageDisplay = QtWidgets.QGraphicsView()
        self.imagePreview = QtWidgets.QLabel()
        self.imagePreview.setScaledContents(True)
        self.imagePreview.setAlignment(QtCore.Qt.AlignCenter)
        self.imagePreview.setPixmap(QtGui.QPixmap("test.jpg"))

        # Configuring Layouts
        self.layout.addLayout(self.titleLayout,0,0)
        self.BodyLayout = QtWidgets.QHBoxLayout()
        self.BodyLayout.addLayout(self.pinterestLayout)
        self.BodyLayout.addLayout(self.googleLayout)
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
        self.credsSearchButton.clicked.connect(self.getFiles)
        # self.searchGoogle.stateChanged.connect()
        self.numImagesBox.currentIndexChanged.connect(self.updateNumImages)
        self.clearButton.clicked.connect(self.clearFolders)
        self.pinterestSearchButton.clicked.connect(self.searchP)
        # self.googleSearchButton.clicked.connect(GoogleDriver)

    # Function for the Search Pinterest Button
    def searchP(self):
        # If the box for searching Pinterest is ticked
        if self.driver.searchPinterest == True:
            # Changing state 
            self.run_Pinterest_Driver()
            self.changeLabelSearching()
            
        # Removing Backgrounds of found images
        if len(os.listdir('out')) != 0:

            # Changing state
            self.run_Remove_Driver()
            self.changeLabelRemoving()

        # Changing State    
        self.changeLabelLoaded()

        # TODO: Make it where the Search Pinterest Button is unclicked when searching is done
            
    # Functionality that is called when the choose credentials button is clicked
    def getFiles(self):
        if self.searchGoogle.isChecked() and self.driver.credsLoaded == False:
            fileDialog = QtWidgets.QFileDialog()
            fileDialog.setNameFilter("JSON files (*.json);;All files (*)")
            selected_file = None
            if fileDialog.exec():
                # Get the selected file name
                selected_file = fileDialog.selectedFiles() 
                if selected_file[0].split('.')[-1] == 'json':
                    print("Current Credentials are json files!")
                    self.driver.credsLoaded = True
                    self.driver.credsFile = selected_file[0]
                    self.credsSearchText.setText("Credentials Loaded!")
                    print(self.driver.credsFile, end="\n")
                    # Checking the Check Box on the UI
                    self.driver.searchGoogle = self.searchGoogle.isChecked()

                    # Copying the contents of the file to __secrets__
                    self.copyCredsToSecret(self.driver.credsFile)

                elif selected_file == None:
                    print("ERROR: Current Credentials are not json files!")
                    self.driver.credsLoaded = False
                    self.searchGoogle.setChecked(False)
                return
    #####################################################
    # Purpose: Copies file that user selects into the 
    # _secrets_ folder
    #####################################################
    def copyCredsToSecret(self,file_name, destination_folder="../_secrets_/"):
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"File '{file_name}' not found.")

        os.makedirs(destination_folder, exist_ok=True)
        base_name = os.path.basename(file_name)
        destination_path = os.path.join(destination_folder, 'client_secret.json')
        try:
            # Open both files in binary mode ('rb' for reading, 'wb' for writing)
            with open(file_name, 'rb') as source_file, open(destination_path, 'wb') as destination_file:
                # Read data from the source file in chunks
                chunk = source_file.read(1024)  # Adjust chunk size as needed
                while chunk:
                    destination_file.write(chunk)
                    chunk = source_file.read(1024)
            print(f"File '{file_name}' copied to '{destination_path}'")
        except OSError as e:
            raise OSError(f"Error copying file: {e}")
        
    # Functionality that handles date chages  
    def updateDate(self):
            self.driver.startDate = [self.startDateBox.date().year(), self.startDateBox.date().month(), self.startDateBox.date().day()]
            self.driver.endDate = [self.endDateBox.date().year(), self.endDateBox.date().month(), self.endDateBox.date().day()]
            self.driver.dateFilter = {
                "startDate": {"year": self.driver.startDate[0], "month": self.driver.startDate[1], "day": self.driver.startDate[2]},
                "endDate": {"year": self.driver.endDate[0], "month": self.driver.endDate[1], "day": self.driver.endDate[2]}
            }

    def updateKey(self):
        self.pinKey = self.pinKeyword.text()

    # Getting the number of images for pinterest to search
    def updateNumImages(self):
        self.numImages = int(self.numImagesBox.currentText())
        print("Looking for ", self.numImages, " on Pinterest")

    # Functionality updates the indicator for loaded pictures
    # def loadedIndicater(self):
    #     if self.driver.searching:
    #         self.loadedLabel.setText("Searching")
    #         self.loadedLabel.setStyleSheet("background-color: Aquamarine;")
    #     elif self.driver.removing == True:
    #         print("Removing state")
    #         self.loadedLabel.setText("Removing")
    #         self.loadedLabel.setStyleSheet("background-color: indigo;")
    #     elif len(os.listdir('result')) != 0  and self.driver.removing == False and self.driver.searching == False:
    #         self.loadedLabel.setText("Loaded")
    #         self.loadedLabel.setStyleSheet("background-color: orange;")
    #     elif os.path.exists('test.png') and os.path.exists('out') == False and os.path.exists('result') and self.driver.removing == False:
    #         self.loadedLabel.setText("Done")
    #         self.loadedLabel.setStyleSheet("background-color: green;")
    #     elif len(os.listdir('out')) == 0 and len(os.listdir('result')) == 0:
    #         self.loadedLabel.setText("Not Loaded")
    #         self.loadedLabel.setStyleSheet("background-color: red;")

    # Functionality that is called when the start button is clicked
    def start(self):

        # DEBUGGING FUNCTIONS
        self.driver.report()

        # Starting a search for images
        if self.driver.startButton:
            
            if self.driver.searchGoogle:
                self.changeLabelSearching()
                self.run_Google_Driver()

            if self.driver.searchPinterest:
                # Changing States
                self.changeLabelSearching()
                self.run_Pinterest_Driver()
            
            # Changing state
            self.changeLabelRemoving()
            
            # Removing Backgrounds
            self.run_Remove_Driver()

            # Changing state
            self.changeLabelLoaded()            

            # Creates the collage
            CollageDriver(height=self.driver.height, width=self.driver.width, 
                          numLayers=self.driver.numLayers, spacing=self.driver.spacing,
                          useWeights=self.driver.weights)
            
            #Changing State
            self.loadedLabel.setText("Finished")
            self.loadedLabel.setStyleSheet("background-color: green;")            
            print("Finished Collage Driver!")

    def clearFolders(self):
        delete_folders('out/')
        delete_folders('result/')

    # Toggling States
    def toggleWeights(self):
        self.driver.weights = self.weightsToggler.isChecked()
        print("toggledWeights: ", self.driver.weights)

    def toggleCrop(self):
        self.driver.cropBoundingBoxes = self.cropToggler.isChecked()
        print("toggledCrop: ", self.driver.cropBoundingBoxes)

    def toggleSearchGoogle(self):
        self.driver.searchGoogle = self.searchGoogle.isChecked()
        print("toggledSearchForImages: ", self.driver.searchGoogle)

    def toggleSearchPinterest(self):
        print("Starting Pinterest Search")
        self.driver.searchPinterest = self.searchPinterest.isChecked()
        print("toggledSearchPinterest: ", self.driver.searchPinterest) 

    def toggleStartButton(self):
        self.driver.startButton = True
        print("toggledStarButton: ", self.driver.startButton)
        self.start()
        self.driver.startButton = FalsestartButton = False
    
    # Handling parameters of the collage
    def handleChangeinHeight(self):
        print("Height is now", self.driver.height)
        self.driver.height = int(self.heightBox.text())

    def handleChangeinWidth(self):
        self.driver.width = int(self.widthBox.text())

    def handleChangeinNumLayers(self):
        self.driver.numLayers = int(self.numLayersBox.text())

    def handleChangeinSpacing(self):
        self.driver.spacing = int(self.spacingBox.text())

    # Changes the loadedLabel to "Searching"
    def changeLabelSearching(self):
        print("Entering changeLabelSearching")
        self.loadedLabel.setText("Searching")
        self.loadedLabel.setStyleSheet("background-color: blue;")
        print("Leaving changeLabelSearching")
        
    # Change the loadedLabel to "Removing"
    def changeLabelRemoving(self):
        self.loadedLabel.setText("Removing")
        self.loadedLabel.setStyleSheet("background-color: maroon;")

    # Change the loadedLabel to "Loaded"
    def changeLabelLoaded(self):
        self.loadedLabel.setText("Loaded")
        self.loadedLabel.setStyleSheet("background-color: orange;")

    # Change the loadedLabel to "Finished"
    def changeLabelFinished(self):
        self.loadedLabel.setText("Finished")
        self.loadedLabel.setStyleSheet("background-color: green;")
        
    # Helper function that run externally-defined functions
    def run_Pinterest_Driver(self):
        print("Running Pinterest Driver")
        PinterestDriver(out=self.driver.imageDir,
                        key=self.pinKey, 
                        threads=10, 
                        images=self.numImages)
        
    def run_Google_Driver(self):
        print("Running Google Driver")
        GoogleDriver(dateFilter=self.driver.dateFilter, 
                     contentFilter=self.driver.contentFilter, 
                     layeredSearch=True)
    
    def run_Remove_Driver(self):
        print("Running Remove Driver")
        RemoveDriver(dir=self.driver.imageDir,typeOfImages="person", 
                    useWeights=self.driver.weights, 
                    crop=self.driver.cropBoundingBoxes)
                          
