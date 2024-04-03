import json
import os , time
import threading
from video import ffmbef_test
import requests
import cv2
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
                # t1=threading.Thread(target=find_status,args=(mac_address, ),daemon=True)
                #t1.start() #
                #t1.join()
                #find the user and password change or not
                print("for", mac_address)
                t2=threading.Thread(target=check_up, args=(mac_address, ), daemon=True)
                t2.start()
                t2.join()

def find_status(mac_address):
    #print(mac_address)
    ip_check=ffmbef_test.find_camera_ip(mac_address)
    if ip_check :#it check the ip address of the is like or not
        cloudcon.send_conn(mac_address)
        print(ip_check,'pressent')
    else:
        cloudcon.send_conn(mac_address)
        print(ip_check,'not')

def check_up(mac_address):
    ip_address = ffmbef_test.find_camera_ip(mac_address)
    if ip_address:
        userapass = ffmbef_test.find_uap(mac_address)  # return the below data from user_data.json file
        if userapass != 'not found':
            username = userapass['user']
            password = userapass['password']
            cameratype = userapass['cameratype']
            print("username",int(cameratype))
        else:
            return('Data reterived failed.')
        if ip_address:
            rtsp_urls = [
                # 0/28:18:fd:95:58:6c/admin/admin123       cpplus
                f'rtsp://{username}:{password}@{ip_address}:554/Streaming/Channels/0',
                # 1/24:b1:05:72:7c:4e/admin/Squadcube12   hikvision
                f'rtsp://{username}:{password}@{ip_address}:554/cam/realmonitor?channel=1&subtype=0',
                # 2/e0:50:8b:97:03:e1/admin/admin@123                     dahua
                f'rtsp://{username}:{password}@{ip_address}/cam/realmonitor?channel=1&subtype=0'
            ]
            #rtsp_url = "rtsp://admin:admin@123@192.168.29.210/cam/realmonitor?channel=1&subtype=0"
            cap = cv2.VideoCapture(rtsp_urls[int(cameratype)])
            if cap.isOpened():
                cap.release()
            else:
                data = {
                    'macaddress': mac_address,
                    'Response': 'password not match'
                }
                json_data = json.dumps(data)
                cloudcon.send_pip(json_data)
    else:
        cloudcon.send_conn(mac_address)
        print('camera is offline or not in network')

#if user want to change username or password of
#this can be use for change that
def changepass(username ,password,mac_address):
    file_path = 'user_data.json'
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    for entry in data:
        if entry['macaddress'] == mac_address:
            if username and password:
                entry['user'] = username
                entry['password'] = password
                return 'updated'
            break
    with open('user_data.json', 'w') as file:
        json.dump(data, file, indent=4)

    print("MAC address not found")
    return 'check the mac_Address'

def delete_camera(mac_address):
    with open('user_data.json', 'r') as file:
        data = json.load(file)

    removed_entry = None
    updated_data = []
    for entry in data:
        if entry['macaddress'] != mac_address:
            updated_data.append(entry)
        else:
            removed_entry = entry
    if removed_entry:
        print(f"Entry removed: {removed_entry}")

    with open('user_data.json', 'w') as file:
        json.dump(updated_data, file, indent=4)

#conn_check()