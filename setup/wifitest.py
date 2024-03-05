from flask import Flask,Response,request,json,render_template,jsonify
import subprocess,time,requests
import os,requests,socket

#app= Flask(__name__)

#create a new connection by creating a xml file by wifi username
def createNewConnection(name, SSID, password):
    config = """<?xml version=\"1.0\"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>"""+name+"""</name>
    <SSIDConfig>
        <SSID>
            <name>"""+SSID+"""</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>"""+password+"""</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>"""
    command = "netsh wlan add profile filename=\""+name+".xml\""+" interface=Wi-Fi"
    with open(name+".xml", 'w') as file:
        file.write(config)
    os.system(command)
    
def connect(name, SSID):
    command = "netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\" interface=Wi-Fi"
    os.system(command)
    
#@app.route('/display',methods=['GET'])
def display():
    try:
        # Run the command to fetch available networks
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'network', 'mode=Bssid'], universal_newlines=True)
        # Split the output by newline character
        lines = results.split('\n')
        # Extract SSIDs and print them
        ssids = [line.split(':')[1].strip() for line in lines if 'SSID' in line]
        return ssids
        #for ssid in ssids:
          #  print(ssid)
    except subprocess.CalledProcessError:
        print("Failed to fetch available networks.")


#@app.route('/testwifi',methods=['POST'])
def testwifi():
    data=request.json
    name=data['wifiDropdown']
    password=data['passw']
    createNewConnection(name, name, password)
    connect(name, name)
    return jsonify({'message':200}),200

#@app.route('/network_check')
def network_check():
    url="https://google.co.in/"
    resp =requests.get(url)
    if resp.status_code == 200:
        return jsonify({'message':200}),200
    else:
        return jsonify({'message':400}),404

#@app.route('/wifi_setup')
def index():
      return render_template('setup.html')
    
#if __name__=='__main__':
 #  app.run(host='0.0.0.0',port=8060,debug=True)
