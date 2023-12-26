### This Branch sorts the images by the amount of white space it has
#### Images with less white space will be placed at the front 

##### ISSUES: This seems to create good collages in each cell but as a whole the pictures contain more white space between each row. 


Models are downloaded to: "Users/{username}/.u2net/" directory
To review the rembg docs go to: https://github.com/danielgatis/rembg?tab=readme-ov-file

# Steps to run this program
1. Get your google credentials file from the Google Cloud Console and place it in a folder called:<br> \_secrets_/credientials.json
2. Edit the filters in the file "GDriver.py" file to your liking 
3. run the file "main.py" 

Then your collage will be saved as test.png



If you have all the photos that you want in your result folder then you can uncomment the code at the end of "collage.py" and just run that file to make the collage with your local photos.