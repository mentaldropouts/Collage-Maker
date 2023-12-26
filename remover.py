from PIL import Image
from rembg import remove, new_session
from os import walk,makedirs
import os.path
import json

#####################################################################
# Purpose: Constructor for storing the images that are to be handled
# Input: folder path, extension to keep when processing
# Output: Object of Image class
#####################################################################
class Images:
    def __init__(self, folder = 'testImages', extensions = ['jpg','jpeg','png'], typeOfImage='person'):
        self.dir = folder
        self.extensions = extensions
        self.w = walk(self.dir)
        self.files = self.throughWalk()
        self.weights = {}
        self.model = 'isnet-general-use'
        self.output = 'out/'
        self.specFileName = ""
        # used to determine the model, set depending on the content filter
        self.typeOfImage = typeOfImage
        makedirs("result", exist_ok=True)
        makedirs(f'result/{self.typeOfImage}',  exist_ok=True)

        


#####################################################################
# Purpose: To go through all the images in specified image gallery
# Input: self.dir define in the initialization as folder
# Output: filling the self.files field with the names of image
# files with specified extensions that are defined in self.ext
#####################################################################
    def throughWalk(self):
        filePaths = []
        for dirNames, dirPaths, fileNames in self.w:
             for file in fileNames:  
                  filePath = str(dirNames+'/'+file)
                  extension = filePath.split('.')[1]
                  if extension in self.extensions:
                    filePaths.append(filePath)
        return filePaths

#####################################################################
# Purpose: Removing the background from Images in the folder
# Input: self.files which contains file names from the
# self.throughWalk function
# Output: A self.result array containing the images the specified 
# format.
#####################################################################
    def removeBack(self):
            numFile = 0 
            # Using the specified model to process the images
            for i in self.files:
                self.modelSelection(i)
                session = new_session(self.model)
                input = Image.open(i)
                
                if hasattr(self, 'amForeground'):
                    output = remove(input, 
                                    session=session, 
                                    alpha_matting=True, 
                                    alpha_matting_foreground_threshold=self.amForeground, 
                                    alpha_matting_background_threshold=self.amBackground,
                                    alpha_matting_erode_size=self.amErode,
                                    post_process_mask=True)
                else:
                     output = remove(input, session=session)
                # output.show() 
                file = i.split('/')[-1]
                name = file.split('.')[0] + ".png"
                # This is currently hard-coded for only using the person model
                path = f"result/{self.typeOfImage}/"+name
                output.save(path)
                #Getting the transparent weights for each image
                data = output.getdata()
                non_transparent_count = sum(1 for pixel in data if pixel[3 ] > 0)
                self.weights[path] = non_transparent_count

                
#####################################################################
# Purpose: Adding Alpha Matting Thresholds as members of Image Class
# Input: self and specific numbers you want threshold to be
# Output: Images instance has members amForeground, amBackground and
# amErode for alpha matting.
#####################################################################
    def alphaMatInitialize(self, amForeground = 270, amBackground = 20, amErode = 11):
         self.amForeground = amForeground
         self.amBackground = amBackground
         self.amErode = amErode

#####################################################################
# Purpose: Seperating files to use with different models
# Input: Image path to use to select the model
# Output: The correct model is slotted in self.model
#####################################################################
    def modelSelection(self, imagePath):
        if '/anime/' in imagePath:
              self.model = 'isnet-anime'
        elif '/person/' in imagePath:
             self.model = 'u2net_human_seg'
        else:
             self.model = 'isnet-general-use'

#####################################################################
# Purpose: Writing transparency weights to a file
# Input: Class object with the self.weights dictionary filled
# Output: file that can be loaded during runtime for faster usage
#####################################################################
    def writeWeights(self,file_path):
    # Write the dictionary to a file in JSON format
        assert len(self.weights) != 0
        with open(file_path, 'w') as json_file:
            json.dump(self.weights, json_file, separators=(',', ':'))

###################################################################
# MAIN DRIVER CODE STARTS HERE 
###################################################################
def RemoveDriver(typeOfImage):
    print("Entering RemoveDriver")
    I = Images(folder="out",typeOfImage=typeOfImage)
    I.throughWalk()
    I.alphaMatInitialize()

    if os.path.exists('result/{self.typeOfImage}'):
         print("pulling from existing results/{self.typeOfImage}")
    else: 
        print("Removing the back of images")
        I.removeBack()

    # Check for the file 
    if os.path.exists('weight.json'):
        print("pulling from existing weights.json")
    else:
        I.writeWeights('weights.json')


   
  