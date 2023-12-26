from PIL import Image
import os
from random import shuffle
import math
import json



class NewCollage:
    def __init__(self, height, width, folder, num_images):
        self.image = [Image.new("RGBA", (height,width)) for i in range(num_images)]
        print(len(self.image))
        self.collageSize = [height,width]
        print(self.collageSize)
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


    def transparentWeightSorting(self):

        os.makedirs("out", exist_ok=True)
        # Get a list of image files in the folder
        self.image_files = [f for f in os.listdir(self.dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
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

    
    def createCollage(self, collage_filename="collage.jpg", spacing=2):
        # Ensure the directory exists
        # Check if there are any images in the folder
        if not self.image_files:
            print("No image files found in the folder.")
            return None
        # Open and paste each image into the collage
        current_x, current_y = 0, 0
        max_height = self.collageSize[1]
        max_width = self.collageSize[0]
        num_images = len(self.image_files)
        # num_rows = max_height // (max_width // num_images + spacing)
        # num_rows = int(math.sqrt(num_images)) // len(self.image)
        num_rows = int(math.sqrt(self.partition))
        num_col = int(math.sqrt(self.partition))
        print("num_rows: ", num_rows, "num_images: ", num_images, "num_images_per_partition: ", self.partition)
        # Calculate the target width and height based on max_width and max_height
        target_width = max_width // (num_col)
        target_height = max_height // (num_rows)
        print("target_height: ", target_height, "target_width: ", target_width)
        curFileNum = 1
        curImagePos = 0
        curImage = self.image[curImagePos]

        for imageFile in self.image_files:
            try:
                image = Image.open(imageFile)
            except Exception as e:
                print(f"Error opening image {imageFile}: {e}")
                continue
            target_height = int((target_width / float(image.width)) * image.height)
            image = image.resize((target_width, target_height))
            self.images.append(image)

        print("adding images")
        self.addImages(curFileNum=curFileNum, 
                       current_x=current_x, 
                       current_y=current_y,
                       target_height=target_height,
                       target_width=target_width,
                       curImagePos=curImagePos,
                       spacing=spacing,
                       num_rows=num_rows)

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
        for i in range(0, len(self.image)):
            base.paste(self.image[i],(0,0),mask = self.image[i])
        return base
    
    def addImages(self, curFileNum, target_width, target_height, spacing, num_rows, curImagePos, current_x, current_y, ):
        curImage = self.image[curImagePos]
        for image in self.images:
            print("Pasting",curFileNum , "position: ", current_x, " ", current_y, " on file number ", curImagePos)
            curImage.paste(image, (current_x, current_y))
            current_x += target_width + spacing
            # If the number of imported files is greater than number of rows
            if curFileNum % num_rows == 0:
                # Move the y value down appropriately
                current_y += target_height + spacing
                current_x = 0
                # print("curFileNum: ", curFileNum)
            portionValue = curFileNum % self.partition
            print(portionValue, "-> ", curFileNum, "%", self.partition)
            if portionValue == 0:
                print()
                curImagePos += 1 
                if curImagePos >= len(self.image):
                    break
                curImage = self.image[curImagePos]
                curFileNum = 0
                current_x = 0 
                current_y = 0
            curFileNum+=1
    
def CollageDriver(numLayers):
    print("Entering CollageDriver")
    collage = NewCollage(8000,8000,"result/", numLayers)
    collage.walk()
    collage.transparentWeightSorting()
    collage.createCollage("collage.jpg")
    result = collage.addImagesTogether()
    result.save('test.png')

# LOCALIZED TESTING 
print("Entering CollageDriver")
collage = NewCollage(8000,8000,"result/person", 7)
collage.walk()
collage.transparentWeightSorting()
collage.createCollage("collage.jpg")
result = collage.addImagesTogether()
result.save('test.png')