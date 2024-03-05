import requests, json

#send public ip  to cloud
def send_pip(oldip):
    url='https://hook.ubeac.io/Ok6uvZQO'
    json_data={"data": oldip}
    json_string = json.dumps(json_data)
    headers = {'Content-Type': 'application/json'}
    response=requests.post(url, data=json_string, headers=headers)
    if response.status_code == 200:
        print('ok')

def send_mac():
    macaddress=[]
    with open('user_data.json') as file:
        data = json.load(file)
        for obj in data:
            if obj.get('macaddress'):
               macaddress.append(obj.get('macaddress'))
        # If MAC address not found, return a message
        send_pip((macaddress))
        print(macaddress)
    return 'not found'

#send_mac()