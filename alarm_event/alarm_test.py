from flask import Flask, render_template, request
import requests
from requests.auth import HTTPDigestAuth
from datetime import datetime
import threading
import time
import cv2
from video import ffmbef_test
from cloudservice import cloudcon
app = Flask(__name__)

class MotionDetectionApp:
    def __init__(self):
        self.camera_available = False
        self.selected_date = None
        self.selected_start_time = None
        self.selected_end_time = None
        self.motion_detection_enabled = False
        self.motion_thread = None
        self.mac_address=None

    def start_motion_detection(self):

        while self.motion_detection_enabled:
            print("one")
            current_date = datetime.now().date()
            current_date_str = current_date.strftime("%Y-%m-%d")
            current_ti=datetime.now()
            current_time = current_ti.strftime("%H:%M")
            if (self.selected_date == current_date_str):
                print('date')
                if ( self.selected_start_time <= current_time <= self.selected_end_time):
                    print("time")
                    self.check_camera_availability()

                    if self.camera_available:
                        print("ttrue")
                        self.check_motion_detection()

            time.sleep(5)

    def check_motion_detection(self):
        ip_address=ffmbef_test.find_camera_ip(self.mac_address)
        if ip_address:
            userapass = ffmbef_test.find_uap(self.mac_address)
            if userapass != 'not found':
                username = userapass['user']
                password = userapass['password']
                cameratype = userapass['cameratype']
                print("username", int(cameratype))
            else:
                return ('Data reterived failed.')
            if ip_address:
                urls = [
                    # 0/28:18:fd:95:58:6c/admin/admin123       cpplus
                    f'http://{ip_address}/cgi-bin/configManager.cgi?action=getConfig&name=VideoStandard',
                    # 1/24:b1:05:72:7c:4e/admin/Squadcube12   hikvision
                    'rtsp://{username}:{password}@{ip_address}:554/cam/realmonitor?channel=1&subtype=0',
                    # 2/e0:50:8b:97:03:e1/admin/admin@123                     dahua
                    f'http://{ip_address}/cgi-bin/eventManager.cgi?action=getEventIndexes&code=VideoMotion'
                ]
            #endpoint = "http://192.168.29.210/cgi-bin/eventManager.cgi?action=getEventIndexes&code=VideoMotion"
                previous_response_content = "Error: No Events"
                try:
                    response = requests.get(urls[int(cameratype)], auth=HTTPDigestAuth(username, password))
                    current_response_content = response.text.strip()

                    if response.status_code == 401:
                        print("Alert: Authentication failure. Check username and password.")
                    elif previous_response_content == "Error: No Events" and current_response_content != "Error: No Events":
                        print(f"Alert: Motion detected! Response changed to: '{current_response_content}'")
                        cloudcon.send_pip(self.mac_address)
                    previous_response_content = current_response_content
                except Exception as e:
                    print(f"Error: {e}")
                    # Add proper error handling based on your requirements

    def check_camera_availability(self):
        ip_address = ffmbef_test.find_camera_ip(self.mac_address)
        print(ip_address)
        userapass = ffmbef_test.find_uap(self.mac_address)  # return the below data from user_data.json file
        if userapass != 'not found':
            username = userapass['user']
            password = userapass['password']
            cameratype = userapass['cameratype']

            print("username", username)
        else:
            return ('Data reterived failed.')
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
                self.camera_available = True
                cap.release()
            else:
                self.camera_available = False
    def check_motion_detection_status(self):
        ip_address = ffmbef_test.find_camera_ip(self.mac_address)
        print("check",self.mac_address)
        if ip_address:
            userapass = ffmbef_test.find_uap(self.mac_address)
            if userapass != 'not found':
                username = userapass['user']
                password = userapass['password']
                cameratype = userapass['cameratype']
                print("username", int(cameratype))
            else:
                return ('Data reterived failed.')
            if ip_address:
                urls = [
                    # 0/28:18:fd:95:58:6c/admin/admin123       cpplus
                    f'http://{ip_address}/cgi-bin/configManager.cgi?action=getConfig&name=VideoStandard',
                    # 1/24:b1:05:72:7c:4e/admin/Squadcube12   hikvision
                    'rtsp://{username}:{password}@{ip_address}:554/cam/realmonitor?channel=1&subtype=0',
                    # 2/e0:50:8b:97:03:e1/admin/admin@123                     dahua
                    f'http://{ip_address}/cgi-bin/configManager.cgi?action=getConfig&name=MotionDetect'
                ]
        #endpoint = "http://192.168.29.210/cgi-bin/configManager.cgi?action=getConfig&name=MotionDetect"
                try:
                    response = requests.get(urls[int(cameratype)], auth=HTTPDigestAuth(username, password))
                    return "table.MotionDetect[0].Enable=true" in response.text
                except Exception as e:
                    print(f"Error checking motion detection status: {e}")
                    return False

    def enable_motion_detection(self):
        ip_address = ffmbef_test.find_camera_ip(self.mac_address)
        print('enable motion',self.mac_address)
        if ip_address:
            userapass = ffmbef_test.find_uap(self.mac_address)
            if userapass != 'not found':
                username = userapass['user']
                password = userapass['password']
                cameratype = userapass['cameratype']
                print("username", int(cameratype))
            else:
                return ('Data reterived failed.')
            if ip_address:
                urls = [
                    # 0/28:18:fd:95:58:6c/admin/admin123       cpplus
                    f'http://{ip_address}/cgi-bin/configManager.cgi?action=getConfig&name=VideoStandard',
                    # 1/24:b1:05:72:7c:4e/admin/Squadcube12   hikvision
                    'rtsp://{username}:{password}@{ip_address}:554/cam/realmonitor?channel=1&subtype=0',
                    # 2/e0:50:8b:97:03:e1/admin/admin@123                     dahua
                    f'http://{ip_address}/cgi-bin/configManager.cgi?action=setConfig&MotionDetect[0].Enable=true'
                ]
                #endpoint = "http://192.168.29.210/cgi-bin/configManager.cgi?action=setConfig&MotionDetect[0].Enable=true"
                try:
                    response = requests.get(urls[int(cameratype)], auth=HTTPDigestAuth(username, password))
                    return response.status_code == 200
                except Exception as e:
                    print(f"Error enabling motion detection: {e}")
                    return False

    def disable_motion_detection(self):
        ip_address = ffmbef_test.find_camera_ip(self.mac_address)
        print(self.mac_address)
        if ip_address:
            userapass = ffmbef_test.find_uap(self.mac_address)
            if userapass != 'not found':
                username = userapass['user']
                password = userapass['password']
                cameratype = userapass['cameratype']
                print("username", int(cameratype))
            else:
                return ('Data reterived failed.')
            if ip_address:
                urls = [
                    # 0/28:18:fd:95:58:6c/admin/admin123       cpplus
                    f'http://{ip_address}/cgi-bin/configManager.cgi?action=getConfig&name=VideoStandard',
                    # 1/24:b1:05:72:7c:4e/admin/Squadcube12   hikvision
                    'rtsp://{username}:{password}@{ip_address}:554/cam/realmonitor?channel=1&subtype=0',
                    # 2/e0:50:8b:97:03:e1/admin/admin@123                     dahua
                    f'http://{ip_address}/cgi-bin/configManager.cgi?action=setConfig&MotionDetect[0].Enable=False'
                ]
                username = username
                password = password
                # endpoint = "http://192.168.29.210/cgi-bin/configManager.cgi?action=setConfig&MotionDetect[0].Enable=true"

                try:
                    response = requests.get(urls[int(cameratype)], auth=HTTPDigestAuth(username, password))
                    return response.status_code == 200
                except Exception as e:
                    print(f"Error enabling motion detection: {e}")
                    return False

motion_app = MotionDetectionApp()

@app.route('/')
def  alarm():
    return render_template('alarm.html', motion_detection_enabled=motion_app.motion_detection_enabled)

@app.route('/activate', methods=['POST'])
def activate_motion_detection():
    motion_app.selected_date = request.form['date']
    motion_app.selected_start_time = request.form['start_time']
    motion_app.selected_end_time = request.form['end_time']
    motion_app.mac_address = request.form['mac_address']
    print(motion_app.mac_address)
    motion_app.motion_detection_enabled = True


    if not motion_app.check_motion_detection_status():
        if motion_app.enable_motion_detection():
            print("Motion detection enabled.")
        else:
            return "Failed to enable motion detection."



    motion_app.motion_thread = threading.Thread(target=motion_app.start_motion_detection)
    motion_app.motion_thread.start()

    return "Motion detection activated!"

@app.route('/deactivate')
def deactivate_motion_detection():
    motion_app.motion_detection_enabled = False
    motion_app.disable_motion_detection()  # Disable motion detection when deactivating
    return "Motion detection deactivated!"

if __name__ == "__main__":
    app.run(debug=True, port=8030)
