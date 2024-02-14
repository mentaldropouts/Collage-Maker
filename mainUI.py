import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from states import mainDriver

from Gdriver import GoogleDriver, delete_folders
from PDriver import PinterestDriver
from remover import RemoveDriver
from collage import CollageDriver
import os

class mainUIClass(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Initial States
        self.pinKey = "People"
        self.numImages = 50
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

        {

        # self.toggleGroup.addWidget(self.removeBackImages, 0,1)
        # self.toggleGroup.addWidget(self.weightsToggler, 1,0)
        # self.toggleGroup.addWidget(self.cropToggler, 1,1)

        # Configuring Content Group
        # self.contentGroup = QtWidgets.QGridLayout()
        # self.animalBox = QtWidgets.QCheckBox("ANIMALS")
        # self.artsBox = QtWidgets.QCheckBox("ARTS")
        # self.birthdayBox = QtWidgets.QCheckBox("BIRTHDAYS")
        # self.cityBox = QtWidgets.QCheckBox("CITYSCAPES")
        # self.craftsBox = QtWidgets.QCheckBox("CRAFTS")
        # self.docBox = QtWidgets.QCheckBox("DOCUMENTS")
        # self.fashionBox = QtWidgets.QCheckBox("FASHION")
        # self.flowersBox = QtWidgets.QCheckBox("FLOWERS")
        # self.foodBox = QtWidgets.QCheckBox("FOOD")
        # self.gardenBox = QtWidgets.QCheckBox("GARDENS")
        # self.holidaysBox = QtWidgets.QCheckBox("HOLIDAYS")
        # self.housesBox = QtWidgets.QCheckBox("HOUSES")
        # self.landBox = QtWidgets.QCheckBox("LANDSCAPES")
        # self.nightBox = QtWidgets.QCheckBox("NIGHT")
        # self.peopleBox = QtWidgets.QCheckBox("PEOPLE")
        # self.perfBox = QtWidgets.QCheckBox("PERFORMANCES")
        # self.petsBox = QtWidgets.QCheckBox("PETS")
        # self.recBox = QtWidgets.QCheckBox("RECEIPTS")
        # self.screenBox = QtWidgets.QCheckBox("SCREENSHOTS")
        # self.selBox = QtWidgets.QCheckBox("SELFIES")
        # self.sportBox = QtWidgets.QCheckBox("SPORTS")
        # self.travelBox = QtWidgets.QCheckBox("TRAVEL")
        # self.utilityBox = QtWidgets.QCheckBox("UTILITY")
        # self.weddingBox = QtWidgets.QCheckBox("WEDDINGS")
        # self.whiteBoards = QtWidgets.QCheckBox("WHITEBOARDS")

        # FUNCTIONALITY HAS NOT BEEN FINISHED FOR THESE FUNCTIONS 
        # self.contentGroup.addWidget(self.animalBox, 0,0)
        # self.contentGroup.addWidget(self.artsBox, 1,0)
        # self.contentGroup.addWidget(self.birthdayBox, 2,0)
        # self.contentGroup.addWidget(self.cityBox, 3,0)
        # self.contentGroup.addWidget(self.craftsBox, 4,0)
        # self.contentGroup.addWidget(self.docBox, 5,0)
        # self.contentGroup.addWidget(self.fashionBox, 6,0)
        # self.contentGroup.addWidget(self.flowersBox, 7,0)
        # self.contentGroup.addWidget(self.foodBox, 8, 0)
        # self.contentGroup.addWidget(self.gardenBox, 9, 0)
        # self.contentGroup.addWidget(self.holidaysBox, 10, 0)
        # self.contentGroup.addWidget(self.housesBox, 11, 0)
        # self.contentGroup.addWidget(self.landBox, 12, 0)
        # self.contentGroup.addWidget(self.nightBox, 13, 0)
        # self.contentGroup.addWidget(self.peopleBox, 0, 1)
        # self.contentGroup.addWidget(self.perfBox, 1, 1)
        # self.contentGroup.addWidget(self.petsBox, 2, 1)
        # self.contentGroup.addWidget(self.recBox, 3, 1)
        # self.contentGroup.addWidget(self.screenBox, 4, 1)
        # self.contentGroup.addWidget(self.selBox, 5, 1)
        # self.contentGroup.addWidget(self.sportBox, 6, 1)
        # self.contentGroup.addWidget(self.travelBox, 7, 1)
        # self.contentGroup.addWidget(self.utilityBox, 8, 1)
        # self.contentGroup.addWidget(self.weddingBox, 9, 1)
        # self.contentGroup.addWidget(self.whiteBoards, 10, 1)
        }

        # Configuring Footer
        self.footer = QtWidgets.QHBoxLayout()
        self.startButton = QtWidgets.QPushButton("Start")
        self.heightBox = QtWidgets.QLineEdit("1000")
        self.widthBox = QtWidgets.QLineEdit("1000") 
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
        # self.credButton.clicked.connect(self.showFiles)
        self.heightBox.textChanged.connect(self.handleChangeinHeight)
        self.widthBox.textChanged.connect(self.handleChangeinWidth)
        self.numLayersBox.textChanged.connect(self.handleChangeinNumLayers)
        self.spacingBox.textChanged.connect(self.handleChangeinSpacing)
        # self.weightsToggler.stateChanged.connect(self.toggleWeights)
        # self.cropToggler.stateChanged.connect(self.toggleCrop)
        self.searchGoogle.stateChanged.connect(self.toggleSearchGoogle)
        self.searchPinterest.stateChanged.connect(self.toggleSearchPinterest)
        
        # self.removeBackImages.stateChanged.connect(self.toggleRemoveBackImages)

        {
        # self.animalBox.stateChanged.connect(self.toggleAnimalBox)
        # self.artsBox.stateChanged.connect(self.toggleArtsBox)
        # self.birthdayBox.stateChanged.connect(self.toggleBirthdayBox)
        # self.cityBox.stateChanged.connect(self.toggleCityBox)
        # self.craftsBox.stateChanged.connect(self.toggleCraftsBox)
        # self.docBox.stateChanged.connect(self.toggleDocBox)
        # self.fashionBox.stateChanged.connect(self.toggleFashionBox)
        # self.flowersBox.stateChanged.connect(self.toggleFlowersBox)
        # self.foodBox.stateChanged.connect(self.toggleFoodBox)
        # self.gardenBox.stateChanged.connect(self.toggleGardenBox)
        # self.holidaysBox.stateChanged.connect(self.toggleHolidaysBox)
        # self.housesBox.stateChanged.connect(self.toggleHousesBox)
        # self.landBox.stateChanged.connect(self.toggleLandBox)
        # self.nightBox.stateChanged.connect(self.toggleNightBox)
        # self.perfBox.stateChanged.connect(self.togglePerfBox)
        # self.petsBox.stateChanged.connect(self.togglePetsBox)
        # self.recBox.stateChanged.connect(self.toggleRecBox)
        # self.screenBox.stateChanged.connect(self.toggleScreenBox)
        # self.selBox.stateChanged.connect(self.toggleSelBox)
        # self.sportBox.stateChanged.connect(self.toggleSportBox)
        # self.travelBox.stateChanged.connect(self.toggleTravelBox)
        # self.utilityBox.stateChanged.connect(self.toggleUtilityBox)
        # self.weddingBox.stateChanged.connect(self.toggleWeddingBox)
        # self.whiteBoards.stateChanged.connect(self.toggleWhiteBoards)
        }

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
        if self.driver.searchPinterest == True:
            PinterestDriver(out=self.driver.imageDir, key=self.pinKey, threads=10, images=self.numImages)


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
        # if os.path.exists(self.driver.imageDir) and not os.listdir(self.driver.imageDir):
            # os.rmdir(self.driver.imageDir)
        if os.path.exists('out') and self.driver.removing == False:
            self.loadedLabel.setText("Loaded")
            self.loadedLabel.setStyleSheet("background-color: orange;")
        elif self.driver.removing == True:
            print("Removing state")
            self.loadedLabel.setText("Removing")
            self.loadedLabel.setStyleSheet("background-color: yellow;")
        elif os.path.exists('result') and self.driver.removing == False:
            self.loadedLabel.setText("Done")
            self.loadedLabel.setStyleSheet("background-color: green;")
        else:
            self.loadedLabel.setText("Not Loaded")
            self.loadedLabel.setStyleSheet("background-color: red;")

    # Functionality that is called when the start button is clicked
    def start(self):
        print("starting")
        self.loadedIndicater()
        if self.driver.startButton:
            if self.driver.searchForImages:
                # print("Data Filter =", self.dateFilter)
                GoogleDriver(dateFilter=self.dateFilter, contentFilter=self.driver.contentFilter, layeredSearch=True)
                self.driver.removing = True
                self.loadedIndicater()
                RemoveDriver(dir=self.driver.imageDir,typeOfImages="person", useWeights=self.driver.weights, crop=self.driver.cropBoundingBoxes)
                self.driver.removing = False
            if self.driver.searchPinterest:
                PinterestDriver(out=self.driver.imageDir, key=self.pinKey, threads=10, images=self.numImages)
                self.driver.removing = True
                self.loadedIndicater()
                RemoveDriver(dir=self.driver.imageDir,typeOfImages="person", useWeights=self.driver.weights, crop=self.driver.cropBoundingBoxes)
                self.driver.removing = False
            # Creates the collage      
            self.loadedIndicater()
            CollageDriver(height=self.driver.height, width=self.driver.width, 
                          numLayers=self.driver.numLayers, spacing=self.driver.spacing,
                          useWeights=self.driver.weights)
            print("Finished Collage Driver!")

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
        self.driver.searchPinterest = self.searchPinterest.isChecked()
        print("toggledSearchPinterest: ", self.driver.searchPinterest)

    {

    # def toggleRemoveBackImages(self):
    #     self.driver.removeBackImages = self.removeBackImages.isChecked()
    #     print("toggledSearchForImages: ", self.driver.removeBackImages)

    # def toggleAnimalBox(self):
    #     self.driver.animals = self.animalBox.isChecked()

    # def toggleArtsBox(self):
    #     self.driver.arts = self.artsBox.isChecked()

    # def toggleBirthdayBox(self):
    #     self.driver.birthday = self.birthdayBox.isChecked()
    #     print("toggledBirthdayBox: ", self.driver.birthday)

    # def toggleCityBox(self):
    #     self.driver.city = self.cityBox.isChecked()

    # def toggleCraftsBox(self):
    #     self.driver.crafts = self.craftsBox.isChecked()

    # def toggleDocBox(self):
    #     self.driver.doc = self.docBox.isChecked()

    # def toggleFashionBox(self):
    #     self.driver.fashion = self.fashionBox.isChecked()

    # def toggleFlowersBox(self):
    #     self.driver.flowers = self.flowersBox.isChecked()

    # def toggleFoodBox(self):
    #     self.driver.food = self.foodBox.isChecked()

    # def toggleGardenBox(self):
    #     self.driver.garden = self.gardenBox.isChecked()

    # def toggleHolidaysBox(self):
    #     self.driver.holidays = self.holidaysBox.isChecked()

    # def toggleHousesBox(self):
    #     self.driver.houses = self.housesBox.isChecked()

    # def toggleLandBox(self):
    #     self.driver.landscapes = self.landBox.isChecked()

    # def toggleNightBox(self):
    #     self.driver.night = self.nightBox.isChecked()

    # def togglePeopleBox(self):
    #     self.driver.people = self.peopleBox.isChecked()
        
    # def togglePerfBox(self):
    #     self.driver.performances = self.perfBox.isChecked()

    # def togglePetsBox(self):
    #     self.driver.pets = self.petsBox.isChecked()

    # def toggleRecBox(self):
    #     self.driver.receipts = self.recBox.isChecked()

    # def toggleScreenBox(self):
    #     self.driver.screenshots = self.screenBox.isChecked()

    # def toggleSelBox(self):
    #     self.driver.selfies = self.selBox.isChecked()

    # def toggleSportBox(self):
    #     self.driver.sports = self.sportBox.isChecked()

    # def toggleTravelBox(self):
    #     self.driver.travel = self.travelBox.isChecked()

    # def toggleUtilityBox(self):
    #     self.driver.utility = self.utilityBox.isChecked()
        
    # def toggleWeddingBox(self):
    #     self.driver.weddings = self.weddingBox.isChecked()

    # def toggleWhiteBoards(self):
    #     self.driver.whiteBoards = self.whiteBoards.isChecked()
    }
    
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
