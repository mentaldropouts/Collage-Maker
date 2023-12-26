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

weights = False
cropBoundingBoxes = True

# Puts files in place
# GoogleDriver(dateFilter=dateFilter, contentFilter=contentFilter, layeredSearch=False)

# Removes these files background
# RemoveDriver(typeOfImage="person", useWeights=weights, crop=cropBoundingBoxes)

# Makes them into a collage
CollageDriver(height=2000, width=2000, numLayers=3, useWeights=weights, spacing=50)