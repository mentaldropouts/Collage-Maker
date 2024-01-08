from Gdriver import GoogleDriver
from remover import RemoveDriver
from collage import CollageDriver
from tkinter import *
from tkinter import ttk


class mainDriver():
    def __init__(self) -> None:
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

        # Main States
        self.weights = False
        self.cropBoundingBoxes = True
        self.searchForImages = False
        self.removeBackImages = False
        # Content Filter States
        self.animals = False
        self.arts = False
        self.birthday = False
        self.city = False
        self.crafts = False
        self.doc = False
        self.fashion = False
        self.flowers = False
        self.food = False
        self.garden = False
        self.holidays = False
        self.houses = False
        self.landscapes = False
        self.night = False
        self.people = False
        self.performances = False
        self.pets = False
        self.receipts = False
        self.screenshots = False
        self.selfies = False
        self.sports = False
        self.travel = False
        self.utility = False
        self.weddings = False
        self.whiteBoards = False
        self.startButton = False
        self.imageDir = 'out'

        if self.searchForImages:

            GoogleDriver(dateFilter=self.dateFilter, contentFilter=self.contentFilter, layeredSearch=True)

        if self.removeBackImages:
            # Removes these fil es background
            RemoveDriver(dir=self.imageDir,typeOfImages="person", useWeights=self.weights, crop=self.cropBoundingBoxes)
            RemoveDriver(dir=self.imageDir, typeOfImages="anime", useWeights=self.weights, crop=self.cropBoundingBoxes)

        # Makes them into a collage
        # CollageDriver(height=self.height, width=self.width, numLayers=self.numLayers, useWeights=self.weights, spacing=self.spacing)