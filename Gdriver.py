import os
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.transport.requests import AuthorizedSession
from io import BytesIO
from PIL import Image
import json
from IPython import display


class PhotoSearch:

#####################################################################
# Purpose: Initializing the Google Photos API and utilizing it to 
# search for specific photographs given filters
# Input: Your Google Credentials.json in a folder called "_secrets_"
# Output: A class object of PhotoSearch that can hold the results
#####################################################################
    def setup(self):
        # Define the API endpoint for mediaItems search
        self.api_url = 'https://photoslibrary.googleapis.com/v1/mediaItems:search'

        # Define the scopes
        self.scopes = ['https://www.googleapis.com/auth/photoslibrary.readonly']

        # Load or obtain credentials
        creds = None

        if os.path.exists('_secrets_/token.json'):
            creds = Credentials.from_authorized_user_file('_secrets_/token.json', self.scopes)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '_secrets_/client_secrets.json', self.scopes)
                creds = flow.run_local_server()
                # Save the credentials for the next run
                with open('_secrets_/token.json', 'w') as token:
                    token.write(creds.to_json())

        # Create an authorized session
        self.authed_session = AuthorizedSession(creds)
        self.nextPageToken = None
        self.idx = 0
        self.media_items = []

#####################################################################
# Purpose: Initializing the filters that you want to use in the 
# search
# Input: Specific filters with parameters in Json format
# Output: Class object should have new fields related to the filters
#####################################################################

        
        # Define the date range for the search
        date_filter = {
            "startDate": {"year": 2023, "month": 5, "day": 1},
            "endDate": {"year": 2023, "month": 6, "day": 15}
        }

        contentFilter = {
            "includedContentCategories": [
                "PEOPLE", 
                "SELFIES",
                "PETS",
                "SCREENSHOTS"
            ],
            "excludedContentCategories": [
                "UTILITY"
            ]
        }

#####################################################################
# Purpose: Make the actual request to the Google Servers to pull the 
# images from the account
# Input: The filters added in addFilters()
# Output: The response stored in self.media_items
#####################################################################
        while True:
            self.idx += 1
            print("index: ",self.idx)

            # Make the request to the API
            response = self.authed_session.post(
                self.api_url,
                headers={'content-type': 'application/json'},
                json={
                    "pageSize": 100,
                    "pageToken": self.nextPageToken,
                    "filters": {
                        "dateFilter": {"ranges": [date_filter]},
                        "contentFilter": contentFilter
                    }
                }
            )

            try:
                # Check the response status code
                print("Response Status Code:", response.status_code)

                # Decode JSON response
                response_json = response.json()

                # Check if there are media items in the response
                media_items_response = response_json.get("mediaItems", [])
                print("Media items count:", len(media_items_response))
    
                # Append media items to the list
                self.media_items += media_items_response

                # Check if there is a next page token
                self.nextPageToken = response_json.get("nextPageToken")

                # Break the loop if there is no next page token
                if not self.nextPageToken:
                    break
    
            except json.decoder.JSONDecodeError as e:
                print("Error decoding JSON:", e)

######################################################################
# Purpose: Converting media_items into a pandas dataframe and saving 
# them to the output directory for use in Collage.py 
# Input: self.media_items and specified output folder
# Output: Images saved into the output folder and them being displayed
######################################################################
                
        # Converting the data into a DataFrame
        photos_df = pd.DataFrame(self.media_items)

        # Ensure the directory exists
        os.makedirs("out", exist_ok=True)

        # Iterate through DataFrame rows and save images
        for index, row in photos_df.iterrows():
            image_data_response = self.authed_session.get(row['baseUrl'] + "=w500-h250")
            image_content = image_data_response.content

            # Save image to the "out" directory
            image_filename = os.path.join("out", f"image_{index}.jpg")
            with open(image_filename, "wb") as img_file:
                img_file.write(image_content)

            # Display the image
            img = Image.open(BytesIO(image_content))
            display.display(img)

        print("Images saved to 'out' directory.")

def GoogleDriver():
    print("Entering GoogleDriver")
    instance = PhotoSearch()
    instance.setup()
    
