import socket
from threading import Thread

# server ip address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
separator_token = "<SEPERATOR>"

# create a socket
client_sockets = set()


s = socket.socket()

# listening for connections
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")


# keeps listening for a message and whenever a message is received, it broadcasts it to other clients
def listen_client(cs):
    while True:
        try:
            # keep listening for message
            msg = cs.recv(1024).decode()
        except Exception as e:
            # client not connected
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            # if we received a message, replace the <SEP> with ": "
            msg = msg.replace(separator_token, ": ")

        # loop over all connected sockets
        for client_socket in client_sockets:
            # send message
            client_socket.send(msg.encode())

    while True:
        #  keep listening for new connections all the time
        client_socket, client_address = s.accept()
        print(f"[+] {client_address} connected.")

        # add client to our socket collection
        client_sockets.add(client_socket)

        # start a new thread, separate thread for separate clients
        t = Thread(target=listen_client, args=(client_socket,))
        t.daemon = True
        t.start()


# close sockets
for cs in client_sockets:
    cs.close()
s.close()
