from PIL import Image
from rembg import remove, new_session
from os import walk

#####################################################################
# Purpose: Constructor for storing the images that are to be handled
# Input: folder path, extension to keep when processing
# Output: Object of Image class
#####################################################################
class Images:
    def __init__(self, folder = 'testImages', extensions = ['jpg','jpeg','gif','png']):
        self.dir = folder
        self.extensions = extensions
        self.w = walk(self.dir)
        self.files = self.throughWalk()
        self.model = 'isnet-general-use'
        self.output = 'out/'
        self.specFileName = ""

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
                print(i)
                output.show()
                file = i.split('/')[-1]
                name = file.split('.')[0] + ".png"
                path = "result/person/"+name
                output.save(path)
                

               

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
       
###################################################################
# MAIN DRIVER CODE STARTS HERE 
#####################################################################
I = Images("out")
I.throughWalk()
I.alphaMatInitialize()
I.removeBack()