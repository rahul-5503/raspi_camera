import socket
import threading

def forward(source_port, target_host, target_port):
    try:
        # Create a socket to listen for incoming connections
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', source_port))
        server.listen(5)

        print(f"[*] Listening on localhost:{source_port}")

        while True:
            client_socket, addr = server.accept()
            print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

            # Create a socket to connect to the target
            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_socket.connect((target_host, target_port))
            print(f"[*] Connected to {target_host}:{target_port}")

            # Start two threads to forward data between the client and the target
            threading.Thread(target=forward_data, args=(client_socket, target_socket)).start()
            threading.Thread(target=forward_data, args=(target_socket, client_socket)).start()

    except Exception as e:
        print(f"[-] Error: {e}")
        server.close()


#it is a medium to get the data from client and send to server or
# get data from sever and send to client
def forward_data(source_socket, target_socket):
    while True:
        data = source_socket.recv(4096) #4kb -get a data
        if not data:
            break
        target_socket.send(data) #send data
    source_socket.close()
    target_socket.close()

if __name__ == "__main__":
    source_port = 9098  # Port on which the forwarder listens
    target_host = "192.168.1.2"  # Target host to forward data to
    target_port = 9098  # Target port to forward data to

    forward(source_port, target_host, target_port)
