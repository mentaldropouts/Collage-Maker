from Gdriver import GoogleDriver
from remover import RemoveDriver
from collage import CollageDriver

class mainDriver():
    def __init__(self) -> None:
        # Initial Specs
        self.height = 1000
        self.width = 1000
        self.numLayers = 3
        self.spacing = 10
        self.startDate = [2023, 10, 18]    
        self.endDate = [2023, 11, 18] 
        self.dateFilter = {
        "startDate": {"year": self.startDate[0], "month": self.startDate[1], "day": self.startDate[2]},
        "endDate": {"year": self.endDate[0], "month": self.endDate[1], "day": self.endDate[2]}
        }

        # Main States
        self.weights = False
        self.removing = False
        self.cropBoundingBoxes = True
        self.removeBackImages = True

        # State of buttons 
        self.searchGoogle = False
        self.searchPinterest = False

        # Linked to seachForImages and seacrchPinterest 
        self.searching = False

        self.credsLoaded = False
        self.credsFile = '_secrets_/client_secret.json'
    
        # Content Filter States
        self.startButton = False
        self.imageDir = 'out'
 
        self.contentFilter = {
            "includedContentCategories": [
                "SELFIES",
                "PETS",
                "LANDSCAPES",
                "PEOPLE"
            ],
            "excludedContentCategories": [
                "UTILITY"
            ]
        } 

    ####################################################
    # Purpose: To return the state of the machine
    # Input: States of the application
    # Output: Printing the state of the application
    ####################################################

    def report(self):
        report = f"""
        Current State of Collage Maker
        ------------------------------
        Height: {self.height} 
        Width: {self.width}
        Number of Layers: {self.numLayers}
        Spacing: {self.spacing}
        Start Date: {self.startDate}
        End Date: {self.endDate}
        Date Filter: {self.dateFilter}
        
        Search Google: {self.searchGoogle}
        Search Pinterest: {self.searchPinterest}

        Credentials Loaded: {self.credsLoaded}
        Credential File: {self.credsFile}

        Searching: {self.searching}
        Weights: {self.weights}
        Removing: {self.removing}
        Cropping Boundaries: {self.cropBoundingBoxes}
        """

        print(report)
