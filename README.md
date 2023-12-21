Models are downloaded to : "Users/{username}/.u2net/" directory 
To review the rembg docs go to: https://github.com/danielgatis/rembg?tab=readme-ov-file

To use this project you need to seperate your files into folders within the folder that 
contains all your images. For my use case I am using testImages to hold my photos.

You need to name the folders within this folder specific things to use specific models:
"anime": uses 'isnet-anime' for finding the foreground
"person": uses 'u2net_human_seg' for finding the foreground
"other": uses 'isnet-general-use' for finding the foreground

