from PIL import Image, ImageDraw
import os
from random import shuffle,randint
import math
import json

class NewCollage:

    def __init__(self, height, width, folder, num_layers):
        self.collages = [Image.new("RGBA", (height,width)) for i in range(num_layers)]
        print(len(self.collages))
        self.collageSize = [height,width]
        print(self.collageSize, "images", num_layers)
        self.dir = folder
        self.images = []
        self.weights_path = 'weights.json'
        self.w = os.walk(self.dir)


    ##############################################################
    # Purpose: Finding how many images can be put in each collage
    # Input: self.w, self.collages
    # Output: self.partition
    ##############################################################
    def walk(self):
        filePaths = []
        for dirNames, dirPaths, fileNames in self.w:
             for file in fileNames:  
                filePath = str(dirNames+'/'+file)
                filePaths.append(filePath)
    
        # Number of images that are to be included in each individual collage
        self.partition = len(filePaths) // len(self.collages)
        print("partition: ", self.partition, "num files", len(filePaths), "num collages", len(self.collages))

    ##############################################################
    # Purpose: opening images and putting them in self.image_files
    # Input: self.dir
    # Output: self.image_files filled with files
    ##############################################################
    def openImages(self):
        os.makedirs("out", exist_ok=True)
        # Get a list of image files in the folder
        self.image_files = [os.path.join(folder, f) for folder, _, files in os.walk(self.dir) for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    ##############################################################
    # Purpose: Sorting images base on the amount of whitespace 
    # Input: self.weights_path
    # Output: self.image_files sorted based on weights
    ##############################################################
    def transparentWeightSorting(self):
        # Read the dictionary from the file
        with open(self.weights_path, 'r') as json_file:
            print("opening ", str(self.weights_path))
            loaded_dict = json.load(json_file) 
        # Sorting images in largest to smallest order
        tuple_array = [(key, value) for key, value in loaded_dict.items()]
        sorted_tuple_array = sorted(tuple_array, key=lambda x: x[1], reverse=True)
        imagePaths = [x[0] for x in sorted_tuple_array]
        
        self.image_files.clear()
        self.image_files = imagePaths

    ################################################################
    # Purpose: Finding the optimal size to make each image
    # Input: Self.collage_size, self.image_files, self.num_rows
    # Output: self.imags containing resized images
    ################################################################
    def resizeImages(self, spacing):
        self.spacing = spacing
        # Check if there are any images in the folder
        if not self.image_files:
            print("No image files found in the folder.")
            return None
        # Open and paste each image into the collage
        self.current_x, self.current_y = 0, 0
        self.max_height = self.collageSize[1]
        self.max_width = self.collageSize[0]
        self.num_rows = math.floor(math.sqrt(self.partition))
        self.curFileNum = 1
        self.curLayerPos = 0
        for imageFile in self.image_files:
            try:
                image = Image.open(imageFile)
                # Calculate target dimensions based on aspect ratio
                aspect_ratio = image.width / image.height
                # print(aspect_ratio)
                if aspect_ratio > 1:  # Landscape image
                    self.target_width = int(self.max_width // self.num_rows)
                    self.target_height = int(self.target_width / aspect_ratio)
                elif aspect_ratio == 1: # Square image
                    self.target_height = int(self.max_height // self.numrows)
                    self.target_width = self.target_height
                else:  # Portrait image
                    self.target_height = int(self.max_height // self.num_rows)
                    self.target_width = int(self.target_height * aspect_ratio)
                
            except Exception as e:
                print(f"Error opening image {imageFile}: {e}")
                continue

            print("target_height: ", self.target_height, "target_width: ", self.target_width)
            image = image.resize((self.target_width, self.target_height))
            self.images.append(image)

        print("adding images")
        self.addImages()

        # self.showImages()

    ################################################################
    # Purpose: Showing the resized images for debugging
    # Input: self.collages 
    # Output: Displaying each image in self.collages
    ################################################################        
    def showImages(self):
        for i in self.collages:
            i.show()
    
    #####################################################################
    # Purpose: Combining the multiple collages in self.images into a 
    # single image
    # Input: NewCollage object with self.images filled with images
    # Output: The data for the final collage
    #####################################################################
    def addLayersTogether(self):
        base = self.collages[0]
        print("BASEH: ", base.height, "BASEW: ", base.width)
        for i in range(0, len(self.collages)):
            if i == 0:
                base.paste(self.collages[i],(0,0),mask = self.collages[i])
            else:
                if i % 2 == 0: 
                    # randWidth = randint(100,150)
                    randWidth = randint(-50,50)
                    randHeight = randint(-50,50)
                elif i % 2 == 1:
                    randWidth = randint(-100,100)
                    randHeight = randint(-100,100)
                base.paste(self.collages[i],(randWidth,randHeight),mask = self.collages[i])
        return base

    #####################################################################
    # Purpose: Making the individual collages
    # Input: The images in self.images
    # Output: A collage image 
    #####################################################################
    def addImages(self):
        shuffle(self.images)
        curLayer = self.collages[self.curLayerPos]
        for image in self.images:
            print(f"Pasting {self.curFileNum:<3} position:  {self.current_x:<5}   {self.current_y:<5}  on file number  {self.curLayerPos:<2}")
            if self.current_x < self.max_width and self.current_y < self.max_height:
                curLayer.paste(image, (self.current_x, self.current_y))
                # curImage.putpixel((self.current_x, self.current_y), (255,255,255,255))
            else:
                print("Out of Range", image.width)
            self.current_x += self.target_width + self.spacing
            # If the number of imported files is greater than number of rows
            # if self.curFileNum % self.num_rows == 0:

            # if the next iteration would put self.current_x over
            if self.current_x + image.width > self.max_width:
                # Move the y value down appropriately
                self.current_y += image.height + self.spacing
                self.current_x = 0
                # print("curFileNum: ", curFileNum)
            imagesInCollage = self.curFileNum % self.partition
            # print(imagesInCollage, "-> ", self.curFileNum, "%", self.partition)
            if imagesInCollage == 0:
                self.curLayerPos += 1 
                if self.curLayerPos >= len(self.collages):
                    break
                curLayer = self.collages[self.curLayerPos]
                self.curFileNum = 0
                self.current_x = 0 
                self.current_y = 0
            self.curFileNum+=1
    
def CollageDriver(height, width, numLayers, useWeights, spacing):
    print("Entering CollageDriver")
    print(width, height)
    collage = NewCollage(height, width, "result/", numLayers)
    collage.walk()
    collage.openImages()
    if useWeights:
        collage.transparentWeightSorting()

    collage.resizeImages(spacing)
    result = collage.addLayersTogether()
    boundingBox = result.getbbox()
    # result = result.crop(boundingBox)
    result.save('test.png')
    result.show('test.png')

# LOCALIZED TESTING 
# print("Entering CollageDriver")
# collage = NewCollage(500,500,"result/", 24)
# collage.walk()
# collage.openImages()x
# spacing = 10
# collage.resizeImages(spacing=spacing)
# result = collage.addLayersTogether()
# result.save('test.png')
