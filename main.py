from Gdriver import GoogleDriver
from remover import RemoveDriver
from collage import CollageDriver
from tkinter import *


class mainDriver():
    def __init__(self) -> None:
        # Initial Specs
        self.height = 1000
        self.width = 1000
        self.numLayers = 3
        self.spacing = 10
        self.startDate = [2023, 10, 18]    
        self.endDate = [2023, 11, 18]   
        # Main States
        self.weights = False
        self.removing = False
        self.cropBoundingBoxes = True
        self.searchForImages = False
        self.searchPinterest = False
        self.removeBackImages = True
        
        # Content Filter States
        self.startButton = False
        self.imageDir = 'out'
 


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

     
        {
        # self.animals = False
        # self.arts = False
        # self.birthday = False
        # self.city = False
        # self.crafts = False
        # self.doc = False
        # self.fashion = False
        # self.flowers = False
        # self.food = False
        # self.garden = False
        # self.holidays = False
        # self.houses = False
        # self.landscapes = False
        # self.night = False
        # self.people = False
        # self.performances = False
        # self.pets = False
        # self.receipts = False
        # self.screenshots = False
        # self.selfies = False
        # self.sports = False
        # self.travel = False
        # self.utility = False
        # self.weddings = False
        # self.whiteBoards = False
        }