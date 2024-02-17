from PIL import Image, ImageDraw
import os
from random import shuffle,randint
import math
import json

class NewCollage:
    def __init__(self, height, width, folder, num_images):
        self.image = [Image.new("RGBA", (height,width)) for i in range(num_images)]
        print(len(self.image))
        self.collageSize = [height,width]
        print(self.collageSize, "images", num_images)
        self.dir = folder
        self.images = []
        self.weights_path = 'weights.json'

        self.w = os.walk(self.dir)
        
    def walk(self):
        filePaths = []
        for dirNames, dirPaths, fileNames in self.w:
             for file in fileNames:  
                filePath = str(dirNames+'/'+file)
                filePaths.append(filePath)
    
        # Number of images that are to be included in each individual collage
        self.partition = len(filePaths) // len(self.image)
        print("partition: ", self.partition, "num files", len(filePaths), "num collages", len(self.image))

    def openImages(self):
        os.makedirs("out", exist_ok=True)
        # Get a list of image files in the folder
        self.image_files = [os.path.join(folder, f) for folder, _, files in os.walk(self.dir) for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

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

    
    def createCollage(self, spacing):
        self.spacing = spacing

        # Check if there are any images in the folder
        if not self.image_files:
            print("No image files found in the folder.")
            return None

        # Open and paste each image into the collage
        self.current_x, self.current_y = 0, 0
        self.max_height = self.collageSize[1]
        self.max_width = self.collageSize[0]
        self.num_rows = int(math.sqrt(self.partition)-1)

        self.curFileNum = 1
        self.curImagePos = 0

        for imageFile in self.image_files:
            try:
                image = Image.open(imageFile)
                # Calculate target dimensions based on aspect ratio
                aspect_ratio = image.width / image.height
                # print(aspect_ratio)
                if aspect_ratio > 1:  # Landscape image
                    self.target_width = int(self.max_width // self.num_rows)
                    self.target_height = int(self.target_width / aspect_ratio)
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
                
    def showImages(self):
        for i in self.image:
            i.show()
    
#####################################################################
# Purpose: Combining the multiple collages in self.images into a 
# single image
# Input: NewCollage object with self.images filled with images
# Output: The data for the final collage
#####################################################################
    def addImagesTogether(self):

        base = self.image[0]
        print("BASEH: ", base.height, "BASEW: ", base.width)
        for i in range(0, len(self.image)):
            if i == 0:
                base.paste(self.image[i],(0,0),mask = self.image[i])
            else:
                if i % 2 == 0: 
                    # randWidth = randint(100,150)
                    randWidth = randint(-50,50)
                    randHeight = randint(-50,50)
                elif i % 2 == 1:
                    randWidth = randint(-100,100)
                    randHeight = randint(-100,100)
                base.paste(self.image[i],(randWidth,randHeight),mask = self.image[i])
        return base
    


#####################################################################
# Purpose: Making the individual collages
# Input: The images in self.images
# Output: A collage image 
#####################################################################
    def addImages(self):
        shuffle(self.images)
        curImage = self.image[self.curImagePos]
        for image in self.images:
            print(f"Pasting {self.curFileNum:<3} position:  {self.current_x:<5}   {self.current_y:<5}  on file number  {self.curImagePos:<2}")
            if self.current_x < self.max_width and self.current_y < self.max_height:
                curImage.paste(image, (self.current_x, self.current_y))
                # curImage.putpixel((self.current_x, self.current_y), (255,255,255,255))
            else:
                print("Out of Range")
            self.current_x += self.target_width + self.spacing
            # If the number of imported files is greater than number of rows
            # if self.curFileNum % self.num_rows == 0:

            # if the next iteration would put self.current_x over
            if self.current_x + self.target_width > self.max_width:
                # Move the y value down appropriately
                self.current_y += self.target_height + self.spacing
                self.current_x = 0
                # print("curFileNum: ", curFileNum)
            portionValue = self.curFileNum % self.partition
            # print(portionValue, "-> ", self.curFileNum, "%", self.partition)
            if portionValue == 0:
                self.curImagePos += 1 
                if self.curImagePos >= len(self.image):
                    break
                curImage = self.image[self.curImagePos]
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

    collage.createCollage(spacing)
    result = collage.addImagesTogether()
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
# collage.createCollage(spacing=spacing)
# result = collage.addImagesTogether()
# result.save('test.png')
