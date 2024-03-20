import subprocess
from flask import Flask, Response,send_file, render_template, jsonify,json,request
import scapy.all as scapy

#app = Flask(__name__)

def find_camera_ip(mac_address):
    # Scan local network for all devices                                                                          have to set static jio
    devices = scapy.srp(scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst="192.168.29.1/24"), timeout=2, verbose=0)[0]
    for _, device in devices:
        if device.haslayer(scapy.ARP):
            if device[scapy.ARP].hwsrc == mac_address:
                #print(device[scapy.ARP].psrc)
                return device[scapy.ARP].psrc  # Return the corresponding IP address

    return None  # Return None if the camera with the given MAC address is not found


def find_uap(mac):
      with open('user_data.json') as file:
        data = json.load(file)
        for obj in data:
            if obj.get('macaddress') == mac:
                return obj
    # If MAC address not found, return a message
      return 'not found' 

def generate_stream(rtsp_url):
    # ffmpeg command to capture RTSP stream and output MP4 stream
    global ffmpeg_process

    ffmpeg_cmd = [
        'ffmpeg',
        '-rtsp_transport', 'tcp',  # Use TCP transport for RTSP (optional, depending on your RTSP server)
        '-i', rtsp_url,
        '-c:v', 'copy',  # Copy video codec (to avoid re-encoding)
        '-an',  # No audio
        '-f', 'mp4',  # Output format is MP4
        '-movflags', 'frag_keyframe+empty_moov',  # Enable fragmented MP4 for live streaming
        '-']

    # Start ffmpeg process
    ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE)
    return ffmpeg_process.stdout


# while flag == True:

    #    data = ffmpeg_process.stdout.read(1024)
     #   if len(data) == 0:
      #      break
       # yield data

    # Return MP4 stream as response
    #return Response(generate(ffmpeg_process), mimetype='video/mp4')

#@app.route('/video_feed/<mac_address>')
def video_feed(mac_address):
    ip_address = find_camera_ip(mac_address)
    print(ip_address)
    userapass=find_uap(mac_address)#return the below data from user_data.json file
    if userapass != 'not found':
            username =userapass['user']
            password =userapass['password']
            cameratype = userapass['cameratype']

            print("username",username)
    else:
          return jsonify({'message': 'Data reterived failed.'})
    if ip_address:
        rtsp_urls = [
          #0/28:18:fd:95:58:6c/admin/admin123       cpplus  
         f'rtsp://{username}:{password}@{ip_address}:554/Streaming/Channels/0',
         #1/24:b1:05:72:7c:4e/admin/Squadcube12   hikvision
         f'rtsp://{username}:{password}@{ip_address}:554/cam/realmonitor?channel=1&subtype=0',
         #2/e0:50:8b:97:03:e1/admin/admin@123                     dahua
         f'rtsp://{username}:{password}@{ip_address}/cam/realmonitor?channel=1&subtype=0'
        ]
        rtsp_stream_url = rtsp_urls[int(cameratype)]
        return Response(generate_stream(rtsp_stream_url ), mimetype='video/mp4')
    else:
        return jsonify({'message': 'camera reterived failed.'})

#@app.route('/stop_stream', methods=['POST'])
def stop_stream():
    global ffmpeg_process
    if ffmpeg_process:
        ffmpeg_process.kill()
        ffmpeg_process = None
        return jsonify({'message': 'Stream stopped successfully.'}), 200
    else:
        return jsonify({'message': 'No active stream to stop.'}), 404

def stream_check():
    username=request.json.get('username')
    password= request.json.get('password')
    mac_address= request.json.get('mac_address')
    cameratype =request.json.get('cameratype')
    ip_address = find_camera_ip(mac_address)
    if ip_address:
        rtsp_urls = [
            # 0/28:18:fd:95:58:6c/admin/admin123       cpplus
            f'rtsp://{username}:{password}@{ip_address}:554/Streaming/Channels/0',
            # 1/24:b1:05:72:7c:4e/admin/Squadcube12   hikvision
            f'rtsp://{username}:{password}@{ip_address}:554/cam/realmonitor?channel=1&subtype=0',
            # 2/e0:50:8b:97:03:e1/admin/admin@123                     dahua
            f'rtsp://{username}:{password}@{ip_address}/cam/realmonitor?channel=1&subtype=0'
        ]
        rtsp_stream_url = rtsp_urls[int(cameratype)]
        return Response(generate_stream(rtsp_stream_url), mimetype='video/mp4')
    else:
        return jsonify({'message': 'camera reterived failed.'})

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=8080, debug=True)
