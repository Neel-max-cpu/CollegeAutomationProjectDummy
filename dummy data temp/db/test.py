import requests

# Define the base URL of your FastAPI application
base_url = "http://localhost:8000"

# Login endpoint URL
login_url = base_url + "/login"

# User credentials
user_credentials = {
    "email": "user@example.com",
    "password": "userpassword"
}

# Send POST request to login endpoint
response = requests.post(login_url, json=user_credentials)

# Check if the request was successful
if response.status_code == 200:
    # Extract the access token from the response JSON
    access_token = response.json()["access_token"]
    print("Login successful. Access Token:", access_token)
else:
    print("Login failed:", response.json()["detail"])
