import requests

# The API endpoint
url = "http://localhost:5000/check_if_user_is_logged/anto"

# A GET request to the API
response = requests.get(url)

# Print the response
print(response.json())