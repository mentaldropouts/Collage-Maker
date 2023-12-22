from PIL import Image
import os
import math


class NewCollage:
    def __init__(self, height, width, folder):
        self.image = Image.new("RGBA", (height,width))
        self.collageSize = [height,width]
        print(self.collageSize)
        self.dir = folder
        self.w = os.walk(self.dir)

    def walk(self):
        filePaths = []
        for dirNames, dirPaths, fileNames in self.w:
             for file in fileNames:  
                filePath = str(dirNames+'/'+file)
                filePaths.append(filePath)
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
        num_rows = int(math.sqrt(num_images))
        num_images_per_row = num_rows

        print("num_rows: ", num_rows, "num_images: ", num_images, "num_images_per_row: ", num_images_per_row)

        # Calculate the target width and height based on max_width and max_height
        target_width = max_width // (num_images_per_row * spacing)
        target_height = max_height // (num_rows * spacing)

        print("target_height: ", target_height, "target_width: ", target_width)
        
        curFileNum = 0
        for imageFile in image_files:
            image_path = os.path.join(self.dir, imageFile)
            try:
                image = Image.open(image_path)
            except Exception as e:
                print(f"Error opening image {imageFile}: {e}")
                continue

            target_height = int((target_width / float(image.width)) * image.height)
            image = image.resize((target_width, target_height))

            # Resize the image to fit the collage
            assert self.collageSize[0] > 0
            assert self.collageSize[1] > 0

            print( target_width , int(self.collageSize[1] - spacing), image_path)
            self.image.paste(image, (current_x, current_y))

            current_x += target_width + spacing

            if curFileNum > num_images_per_row:
                current_x = 0
                current_y += target_height + spacing
                curFileNum = 0

            curFileNum+=1
        self.image.show()


collage = NewCollage(8000,4000,"result/person")
files = collage.walk()
# print(files)

collage.createCollage("collage.jpg")