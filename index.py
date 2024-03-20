from video import  ffmbef_test as vi
from setup import wifitest, cam_config
from flask import Flask ,request
import subprocess
from connectionStatus import publicipfind , check_userpass
#from cloudservice import cloudcon
import  threading
from  alarm_event import alarm_test
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

#positive
#play the video according to the mac
@app.route('/video_feed/<mac_address>')
def video_feed(mac_address):
    return vi.video_feed(mac_address)

#positive
#stop the stream which is run in ffmpeg
@app.route('/stop_stream')
def stop_stream():
    return  vi.stop_stream()

#positive
# get the details of the user
@app.route('/details')
def det():
    return cam_config.details()

@app.route('/stream_check',methods=['POST'])
def stream_check():
    return vi.stream_check()

#positive
#submit the method
#can also use full for add new device from client
@app.route('/submit',methods=['POST'])
def submit():
    return cam_config.submit()

#positive
#return a nearby wifi name
@app.route('/display',methods=['GET'])
def display():
    return wifitest.display()
#positive
#create a wifi connection
@app.route('/testwifi',methods=['POST'])
def testwifi():
    return wifitest.testwifi()

#positive
#return network status
@app.route('/network_check')
def network_check():
    return wifitest.network_check() #it not need any data from the user are function only need from google
# to get a wifi password and store in it
#it uses /network_check , /testwifi
#positive
@app.route('/')
def index():
    return wifitest.index() #it only need data from user not a macfunction

@app.route('/cloud')
def cloud():
    pass

@app.route('/alarm')
def alarm():
    return  alarm_test.alarm()

@app.route('/activate_alarm', methods=['POST'])
def activate_motion_detection():
    return alarm_test.activate_motion_detection()

@app.route('/deactivate_alarm')
def deactivate_motion_detection():
    return alarm_test.deactivate_motion_detection()

#user can change the username and password

@app.route('/change_pass')
def chnge_pass():
    user = request.json.get('name')
    password = request.json.get('password')
    mac_address = request.json.get('mac_address')
    return check_userpass.changepass(user ,password ,mac_address)

#
@app.route('/delete_cam' ,methods=['POST'])
def deletecamera():
    mac_address=request.json.get('mac_address')
    return check_userpass.delete_camera(mac_address)
#for windows
def wifienable():
    return subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "enabled"])


if __name__=='__main__':
    #for linux # subprocess.run(["sudo", "ifconfig", "wlan0", "up"])
    t1=threading.Thread(target=wifienable)
    t1.start()
    #t2 = threading.Thread(target=publicipfind.publicip)
    #t2.start()
    #t3=threading.Thread(target=check_userpass.conn_check)
    #t3.start()
    app.run(host='0.0.0.0', port=9098,debug=True)

