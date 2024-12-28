import requests

# Replace with your URL, username, and password
url = "https://recordings.exotel.com/exotelrecordings/guvi64/37c774e477eb9fdc31d981ac6e1418cn.mp3"
username = "0011108477047d82a455ec82081b0e67fb91322d6705b9bc"
password = "78bdfe0875b16f71fe5968bf7238b5bafe03f2a2f08d8826"

# Make the request with basic authentication
response = requests.get(url, auth=(username, password))

# Check the response
if response.status_code == 200:
    # Save the MP3 file locally
    with open("audio.mp3", "wb") as f:
        f.write(response.content)
    print("Success: The audio file has been downloaded and saved as 'audio.mp3'.")
else:
    print("Failed:", response.status_code, response.text)
