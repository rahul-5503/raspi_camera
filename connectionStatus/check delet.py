import requests
from requests.auth import HTTPDigestAuth
from video import ffmbef_test
# Replace these values with your actual credentials and URL
username = 'admin'
password = 'admin@12'
url = 'http://192.168.29.210/cgi-bin/configManager.cgi?action=getConfig&name=VideoStandard'

# Make a GET request with Digest Authentication
response = requests.get(url, auth=HTTPDigestAuth(username, password))

# Check if the request was successful
if response.status_code == 200:
    if "table.VideoStandard=PAL" in response.text:
        print("Request successful!")
        print("Response:", response.text)
    else:
        print("Request failed:")
        print("Response :",response.text)
else:
    print("Request failed:", response.status_code)


def check_up():
    ip_address = ffmbef_test.find_camera_ip(mac_address)
    # print(ip_address)
    userapass = find_uap(mac_address)  # return the below data from user_data.json file
    if userapass != 'not found':
        username = userapass['user']
        password = userapass['password']
        cameratype = userapass['cameratype']

        # print("username",username)
    else:
        return jsonify({'message': 'Data reterived failed.'})
    if ip_address:
        rtsp_urls = [
            # 0/28:18:fd:95:58:6c/admin/admin123       cpplus
            f'rtsp://{username}:{password}@{ip_address}:554/Streaming/Channels/0',
            # 1/24:b1:05:72:7c:4e/admin/Squadcube12   hikvision
            f'rtsp://{username}:{password}@{ip_address}:554/cam/realmonitor?channel=1&subtype=0',
            # 2/e0:50:8b:97:03:e1/admin/admin@123                     dahua
            f'rtsp://{username}:{password}@{ip_address}/cam/realmonitor?channel=1&subtype=0'
        ]