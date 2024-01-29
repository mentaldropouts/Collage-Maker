from pinscrape import pinscrape
import os

class PhotoSearch:
#####################################################################
# Purpose: Scrape Images from Pinterst to use in collages
# Input: Nothing
# Output: A folder that contains the images 
#####################################################################
    def makeSearch(self, outputFolder, keyword, maxThreads, maxImages):
        self.details = pinscrape.scraper.scrape(keyword, outputFolder, {}, maxThreads, maxImages)

    def printResult(self):
        if self.details["isDownloaded"]:
            print("\nDownloading completed !!")
            print(f"\nTotal urls found: {len(self.details['extracted_urls'])}")
            print(f"\nTotal images downloaded (including duplicate images): {len(self.details['url_list'])}")
            print(self.details)
        else:
            print("Nothing to download")

def PinterestDriver(out, key, threads, images):
    obj = PhotoSearch()
    obj.makeSearch(out, key, threads, images)


# Local Testing 
# obj = PhotoSearch()
# obj.PinterestDriver("out", "Transformers", 10, 15)
        
