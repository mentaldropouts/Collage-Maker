from Gdriver import GoogleDriver
from remover import RemoveDriver
from collage import CollageDriver

dateFilter = {
    "startDate": {"year": 2023, "month": 1, "day": 1},
    "endDate": {"year": 2023, "month": 3, "day": 22}
}

contentFilter = {
    "includedContentCategories": [
        "SELFIES"
    ],
    "excludedContentCategories": [
        "UTILITY"
    ]
} 

# STATES
weights = False
cropBoundingBoxes = True
searchForImages = False
removeBackImages = True

imageDir = 'testImages'

if searchForImages:
    GoogleDriver(dateFilter=dateFilter, contentFilter=contentFilter, layeredSearch=True)

if removeBackImages:
    # Removes these fil es background
    RemoveDriver(dir=imageDir,typeOfImages="person", useWeights=weights, crop=cropBoundingBoxes)
    RemoveDriver(dir=imageDir, typeOfImages="anime", useWeights=weights, crop=cropBoundingBoxes)

# Makes them into a collage
CollageDriver(height=2000, width=2000, numLayers=6, useWeights=weights, spacing=50)
