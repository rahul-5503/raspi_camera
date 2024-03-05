import socket
import subprocess
def is_port_open(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.settimeout(2)  # Set a timeout for the connection attempt
        sock.connect((ip, port))
        return True
    except Exception as e:
        return False
    finally:
        sock.close()

public_ip = '106.205.124.173'
port = 8000

def port_check():
    result=subprocess.check_output([ 'nmap','-p8000','106.205.124.173'],universal_newlines=True)
    lines=result.split('\n')
    print(lines)

if is_port_open(public_ip, port):
    print(f"Port {port} is open for {public_ip}")
else:
    print(f"Port {port} is not open for {public_ip}")

#port_check()
