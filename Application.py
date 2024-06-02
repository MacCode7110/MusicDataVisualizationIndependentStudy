import json
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import pandas as pd
import altair as alt

# Load selected csv data into a pandas dataframe

needed_columns = ["spotify_id"]

dataframe = pd.read_csv(
    "music_preference_questionnaire_responses.csv",
    usecols=needed_columns,
    na_filter=False,
    nrows=20
)

# Enable access to the Spotify Web API

load_dotenv()  # Parse the .env file and load all the stored environment variables.

client_id = os.getenv("CLIENT_ID")  # Get the CLIENT_ID environment variable
client_secret = os.getenv("CLIENT_SECRET")  # Get the CLIENT_SECRET environment variable

authorization_info = client_id + ":" + client_secret  # information that is needed to get the API access token.
authorization_info_to_bytes = authorization_info.encode("utf-8")
authorization_info_to_base64 = str(base64.b64encode(authorization_info_to_bytes), "utf-8")

url = "https://accounts.spotify.com/api/token"
headers = {
    "Authorization": "Basic " + authorization_info_to_base64,
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {"grant_type": "client_credentials"}
result = post(url, headers=headers, data=data)
json_result = json.loads(result.content)  # The deserialization of outcome.content produces a json object
access_token = json_result["access_token"]
authorization_header = {"Authorization": "Bearer " + access_token}


#  Access a selection of audio features for all tracks

def get_audio_features(track_ids):
    coordinates_dict = {}
    for track_id in track_ids:
        query_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
        query_result = get(query_url, headers=authorization_header)
        json_conversion = json.loads(query_result.content)
        coordinates_dict[track_id] = {"X": json_conversion["energy"], "Y": json_conversion["danceability"]}
    return coordinates_dict


coordinates_by_track_id = get_audio_features(dataframe["spotify_id"].tolist())

