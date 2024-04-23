# Automatic Collage Maker

![badmath](https://img.shields.io/github/languages/top/mentaldropouts/collageApp)

## Description
This application helps automate the process of creating collages, by assisting the user in collecting photos from their Google Photos account or from Pinterest,
Using Collage Maker these chosen photos can be used to create countless collages in seconds.

## Installation
You can install Collage Maker by running these commands
```
# Cloning repo
git clone https://github.com/mentaldropouts/Collage-Maker.git

# Making a virtual enviornment
pyenv virtualenv env
pyenv activate env

# Installing requiremnets
pip install -r requirements.txt

# Running the application
python src/main.py
```
## Usage
### Searching Google Photos
To use this program you first need to add your credentials.json file to a folder named \_secret_ in your cloned copy of the repo. For security reasons, this folder has been included in the .gitignore file so don't worry about accidentally commiting your google account information.
### Searching Pinterest
Just tick the checkbox and type in what ever you want to search for along with the number of images that you want and press the search button. It will buffer for a bit but if you inspect the terminal in which you started the app with it should show that it is removing the backgrounds of photos found. 
### Making a collage
Set the number of layers and size of the collage that you want to make then press the start button. If you have both "Search Google" and "Search Pinterest" boxes unticked then the process for making the collage should take only a second or two. 
### Tips for using
If you are getting alot of photos on the left side and not alot on the right, try reducing the number of layers and increasing the spacing value by 20 or so. This app allows you to manipulate alot of the parameters used in creating the collage but with that you have to perform some trial and error to get what you want. 


## Example 
![Example](Examples/Example.png)

![Example2](Examples/Example2.png)

![Example3](Examples/Example3.png)

![Example4](Examples/Example4.png)
