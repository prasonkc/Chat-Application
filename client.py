import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back

# initialize colors
init()

colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX,
          Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
          Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX,
          Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
          ]

# choose a random color for the connected client
client_color = random.choice(colors)

# server's IP address
SERVER_HOST = "0.tcp.ap.ngrok.io"  # tcp server hosted at ngrok or other app
SERVER_PORT = 16491 # port at tcp server
separator_token = "<SEP>"

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")

# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

# Ask client for a name
name = input("Username: ")


def listen_for_messages():
    # keep listening to client's message
    while True:
        msg = s.recv(1024).decode()
        print("")
        print(msg)


# thread to listen for messages
t = Thread(target=listen_for_messages)
t.daemon = True
t.start()


while True:
    # input message
    to_send = input()
    # use :q to exit
    if to_send.lower() == ':q':
        break

    # send message
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    to_send = f"{client_color}[{date_now}] {name}: {to_send}{Fore.RESET}"
    s.send(to_send.encode())

# close the socket
s.close()
