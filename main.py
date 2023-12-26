from Gdriver import GoogleDriver
from remover import RemoveDriver
from collage import CollageDriver


date_Filter = {
    "startDate": {"year": 2023, "month": 8, "day": 1},
    "endDate": {"year": 2023, "month": 12, "day": 22}
}

content_Filter = {
    "includedContentCategories": [
    "SELFIES"
    ],
    "excludedContentCategories": [
    "UTILITY"
    ]
} 

# Puts files in place
GoogleDriver(date_Filter, content_Filter)
# Removes these files background
RemoveDriver()
# Makes them into a collage
CollageDriver()
