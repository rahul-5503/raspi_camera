from flask import Flask,Response,request,json,jsonify,render_template,send_file
import os,cv2
import scapy.all as scapy
import requests
import threading
from cloudservice import cloudcon

#app = Flask(__name__)

def find_uap(mac):
    with open('user_data.json') as file:
        data = json.load(file)
        for obj in data:
            if obj.get('macaddress') == mac:
                return obj
    # If MAC address not found, return a message
    return 'not found'

#@app.route('/submit', methods=['POST'])
def submit():
    user = request.form.get('name')
    password = request.form.get('password')
    cameratype = request.form.get('cameratype')
    macaddress = request.form.get('macaddress')

    if not user or not password:
        return jsonify({'error': 'User and password are required.'}), 400
    # set a data in json formate
    data = {
        "user": user,
        "password": password,
        "cameratype": cameratype,
        "macaddress": macaddress
    }
    file_path = 'user_data.json'

    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            existing_data = json.load(json_file)

        existing_data.append(data)

        with open(file_path, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)
    else:
        with open(file_path, 'w') as json_file:
            json.dump([data], json_file, indent=4)

    data={
        'macaddress':macaddress
    }
    cloudcon.send_pip(data)
    return macaddress

#@app.route('/details')
def details():
    return render_template('index.html')


#if __name__ == '__main__':
 #   app.run(host='0.0.0.0', port=8100, debug=True)
    
