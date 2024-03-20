from flask import Flask,Response,request,json,jsonify,render_template
import os ,subprocess,requests
from flask_cors import CORS
from cloudservice import cloudcon

app = Flask(__name__)
CORS(app)
final = []
#24:b1:05:72:7c:4e
# to get a data from form input
@app.route('/submit', methods=['POST'])
def submit():

    count_str = request.json.get('count')
    value=request.json.get('value')
    print(count_str)
    print(value)
    if count_str is None:
        return jsonify({'error': 'Count is missing in form data'}), 400

    try:
        count = int(count_str)
    except ValueError:
        return jsonify({'error': 'Count must be an integer'}), 400

    for i in range(count):
        user = value[i].get('username' )
        password = value[i].get('password' )
        cameratype = value[i].get('cameratype' )
        macaddress = value[i].get('mac_address' )

        data = {
            "user": user,
            "password": password,
            "cameratype": cameratype,
            "macaddress": macaddress
        }
        final.append(data)
    print(final)
    cloudcon.send_pip(final)
    # Return the list containing all the data
    return jsonify(final)

#@app.route('/wifi',methods=['GET'])
def wifi():
    try:
        # Run the command to fetch available networks
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'network', 'mode=Bssid'], universal_newlines=True)
        # Split the output by newline character
        lines = results.split('\n')
        # Extract SSIDs and print them
        ssids = [line.split(':')[1].strip() for line in lines if 'SSID' in line]
        file_path = 'user_data.json'
        return ssids
    except subprocess.CalledProcessError:
        print("Failed to fetch available networks.")

#@app.route('/detail')
def index():
    return render_template('alarm.html')

#@app.route('/')
def setup():
    return render_template('setup.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

