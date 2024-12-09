import requests
import json

# Download a file
def download_file(peer_ip, filename):
    url = f"http://{peer_ip}:8000/files/{filename}"
    r = requests.get(url)
    if r.status_code == 200:
        with open('downloaded_' + filename, 'wb') as f:
            f.write(r.content)
        print("File downloaded successfully.")
    else:
        print("Error downloading file.")

# Upload a file
def upload_file(peer_ip, filename):
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8', errors='ignore')
    url = f"http://{peer_ip}:8000/files"
    data = {
        "filename": "uploaded_" + filename,
        "content": content
    }
    r = requests.post(url, data=json.dumps(data))
    if r.status_code == 201:
        print("File uploaded successfully.")
    else:
        print("Error uploading file.")