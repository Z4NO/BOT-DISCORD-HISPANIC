import requests
import discord


"""
Check if a user is logged in to Spotify.

Args:
    username (str): The username of the user to check.

Returns:
    bool: True if the user is logged in, False otherwise.
"""
async def check_if_user_is_logged_for_spotify(username: dis):
    url = f"http://localhost:5000/check_if_user_is_logged/{username}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json().get("is_logged", False)
    else:
        print(f"Error checking login status for {username}: {response.status_code}")
        return False