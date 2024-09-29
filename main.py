import json
from dotenv import load_dotenv
import os
import base64
from requests import post, get

# initialize dotenv
load_dotenv()

# Retrieve environmental variables from .env file
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# API starting url
api_url = "https://api.spotify.com/v1/"

# Function to request token from Spotify's API
def get_token():
    #Use app's client id and client secret as auth token encoded into base64
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    # Define url and headers
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Post request that returns token in a json format
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

# Function that builds auth header with token
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# Function to search for artists on Spotify
def search_for_artist(token, artist_name):
    # build url and headers
    url = api_url + "search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query

    # Get request to retrieve artist and store as json object
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    # If statement to check if artist was found
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None

    # Return the artist object
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    # Build the url and headers
    url = api_url + f"artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)

    # Get request to retrieve tracks then store tracks as json object
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]

    # Return the track object
    return json_result

# Get a token for authorization
token = get_token()

# Search for the artist with the name "AC/DC" then store id of the artist
result = search_for_artist(token, "ACDC")
artist_id = result["id"]

# Gets the top songs of the artist
songs = get_songs_by_artist(token, artist_id)

# iterate through the tracks received and print them in a readable format
for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")