import requests, json

#send public ip  to cloud
def send_pip(oldip):

    url='https://hook.ubeac.io/fs7niiuy'
    print(url)
    json_data={"data": oldip}
    print (json_data)
    querystring = {"foo": ["bar", "baz"]}
    payload = json.dumps(json_data)
    headers = {
         'cookie': "foo=bar; bar=baz",
         'accept': "application/json",
         'content-type': "application/json",
         'x-pretty-print': "2"
    }
    response=requests.request("POST",url, data=payload, headers=headers,params=querystring)
    print(response.text)
    if response.status_code == 200:
        print('ok')
    return ('success'),200

#it will send the connection status of the camera to cloud
#for showing the connection status to user for purticular camera
#by mac_address
def send_conn(ip):
    #url can be change as the endpoint
    url='https://hook.ubeac.io/fs7niiuy'
    json_data={"mac_address":ip}
#    print('from send_conn',ip)
    querystring = {"foo": ["bar", "baz"]}
    payload = json.dumps(json_data)
    headers = {
        'cookie': "foo=bar; bar=baz",
        'accept': "application/json",
        'content-type': "application/json",
        'x-pretty-print': "2"
    }
    response = requests.request("POST",url, data=payload, headers=headers, params=querystring)
    if response.status_code == 200:
        print('=====ok',response.status_code)


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