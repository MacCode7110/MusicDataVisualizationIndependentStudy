import json
from dotenv import load_dotenv
import os
import base64
from requests import post

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
outcome = post(url, headers=headers, data=data)
json_outcome = json.loads(outcome.content)  # The deserialization of outcome.content produces a json object
access_token = json_outcome["access_token"]
authorization_header = {"Authorization": "Bearer " + access_token}

