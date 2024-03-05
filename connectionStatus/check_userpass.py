import json
import os , time
import threading
from video import ffmbef_test
import requests
from requests.auth import HTTPDigestAuth
from cloudservice import  cloudcon
#check camera presence
def conn_check():
    file_path = 'user_data.json'
    with open(file_path ,'r') as json_file:
        data =json.load(json_file)
        while True:
            print('10')
            time.sleep(10)
            for obj in data:
                mac_address=obj.get('macaddress')
                # it will return the pressence of the camera
                # and use the ffmbef_test files find_ip_Address function to find the ipaddress of the camera
                t1=threading.Thread(target=find_status,args=(mac_address, ),daemon=True)
                t1.start() #
                t1.join()
                #find the user and password change or not
                print("for", mac_address)
                t2=threading.Thread(target=check_up, args=(mac_address, ), daemon=True)
                t2.start()
                t2.join()

def find_status(mac_address):
    #print(mac_address)
    ip_check=ffmbef_test.find_camera_ip(mac_address)
    if ip_check :#it check the ip address of the is like or not
        print(ip_check,'pressent')
    else:
        print(ip_check,'not')
        return ip_check

def check_up(mac_address):
    ip_address = ffmbef_test.find_camera_ip(mac_address)
    # print(ip_address)
    userapass = ffmbef_test.find_uap(mac_address)  # return the below data from user_data.json file
    if userapass != 'not found':
        username = userapass['user']
        password = userapass['password']
        cameratype = userapass['cameratype']
        print("username",int(cameratype))
    else:
        return('Data reterived failed.')
    if ip_address:
        urls = [
            # 0/28:18:fd:95:58:6c/admin/admin123       cpplus
            f'http://{ip_address}/cgi-bin/configManager.cgi?action=getConfig&name=VideoStandard',
            # 1/24:b1:05:72:7c:4e/admin/Squadcube12   hikvision
            'rtsp://{username}:{password}@{ip_address}:554/cam/realmonitor?channel=1&subtype=0',
            # 2/e0:50:8b:97:03:e1/admin/admin@123                     dahua
            f'http://{ip_address}/cgi-bin/configManager.cgi?action=getConfig&name=VideoStandard'
        ]
        response = requests.get(urls[int(cameratype)], auth=HTTPDigestAuth(username, password))
        # Check if the request was successful
        if response.status_code == 200:
            if "table.VideoStandard=PAL" in response.text:
                print("Request successful!")
                print("Response:", response.text)
            else:
                data={
                    'macaddress': mac_address,
                    'Response': 'password not match'
                }
                json_data=json.dumps(data)
                cloudcon.send_pip(json_data)
                print("Request failed:")
                print("Response :", response.text)
        else:
            print("Request failed:", response.status_code)
    else:
        print('camera is offline or not in network')

#conn_check()