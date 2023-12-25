from PIL import Image
import os
from random import shuffle
import math



class NewCollage:
    def __init__(self, height, width, folder, num_images):
        self.image = [Image.new("RGBA", (height,width)) for i in range(num_images)]
        print(len(self.image))
        self.collageSize = [height,width]
        print(self.collageSize)
        self.dir = folder
        self.images = []

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
        return filePaths
    
    def createCollage(self, collage_filename="collage.jpg", spacing=2):
        # Ensure the directory exists
        os.makedirs("out", exist_ok=True)
        # Get a list of image files in the folder
        image_files = [f for f in os.listdir(self.dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        # Check if there are any images in the folder
        if not image_files:
            print("No image files found in the folder.")
            return None
        # Open and paste each image into the collage
        current_x, current_y = 0, 0
        max_height = self.collageSize[1]
        max_width = self.collageSize[0]
        num_images = len(image_files)
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
        for imageFile in image_files:
            image_path = os.path.join(self.dir, imageFile)
            try:
                image = Image.open(image_path)
            except Exception as e:
                print(f"Error opening image {imageFile}: {e}")
                continue
            target_height = int((target_width / float(image.width)) * image.height)
            image = image.resize((target_width, target_height))
            self.images.append(image)

        shuffle(self.images)
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
    
def CollageDriver():
    print("Entering CollageDriver")
    collage = NewCollage(8000,8000,"result/person", 10)
    files = collage.walk()
    # print(files)
    collage.createCollage("collage.jpg")
    result = collage.addImagesTogether()
    result.save('test.png')

# LOCALIZED TESTING 
print("Entering CollageDriver")
collage = NewCollage(8000,8000,"result/person", 10)
files = collage.walk()
    # print(files)
collage.createCollage("collage.jpg")
result = collage.addImagesTogether()
result.save('test.png')