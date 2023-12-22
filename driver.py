import os
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.transport.requests import AuthorizedSession
from io import BytesIO
from PIL import Image
from IPython import display

# Define the API endpoint for mediaItems search
api_url = 'https://photoslibrary.googleapis.com/v1/mediaItems:search'

# Define the scopes
scopes = ['https://www.googleapis.com/auth/photoslibrary.readonly']

# Load or obtain credentials
creds = None

if os.path.exists('_secrets_/token.json'):
    creds = Credentials.from_authorized_user_file('_secrets_/token.json', scopes)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            '_secrets_/client_secrets.json', scopes)
        creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('_secrets_/token.json', 'w') as token:
            token.write(creds.to_json())

# Create an authorized session
authed_session = AuthorizedSession(creds)
nextPageToken = None
idx = 0
media_items = []

# Define the date range for the search
date_filter = {
    "startDate": {"year": 2023, "month": 8, "day": 1},
    "endDate": {"year": 2023, "month": 11, "day": 26}
}

contentFilter = {
     "includedContentCategories": [
        "PEOPLE"
      ]
}

while True:
    idx += 1
    print(idx)

    # Make the request to the API
    response = authed_session.post(
        api_url,
        headers={'content-type': 'application/json'},
        json={
            "pageSize": 100,
            "pageToken": nextPageToken,
            "filters": {"dateFilter": {"ranges": [date_filter]},
                        "contentFilter": contentFilter}
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
        media_items += media_items_response

        # Check if there is a next page token
        nextPageToken = response_json.get("nextPageToken")

        # Break the loop if there is no next page token
        if not nextPageToken:
            break

    except json.decoder.JSONDecodeError as e:
        print("Error decoding JSON:", e)

# Converting the data into a DataFrame
photos_df = pd.DataFrame(media_items)

# Ensure the directory exists
os.makedirs("out", exist_ok=True)

# Iterate through DataFrame rows and save images
for index, row in photos_df.iterrows():
    image_data_response = authed_session.get(row['baseUrl'] + "=w500-h250")
    image_content = image_data_response.content

    # Save image to the "out" directory
    image_filename = os.path.join("out", f"image_{index}.jpg")
    with open(image_filename, "wb") as img_file:
        img_file.write(image_content)

    # Display the image
    img = Image.open(BytesIO(image_content))
    display.display(img)

print("Images saved to 'out' directory.")
