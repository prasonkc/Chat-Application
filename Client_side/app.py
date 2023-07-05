from flask import Flask, render_template, request,redirect, session
from helpers import login_required
import sqlite3
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

# # server's IP address
# SERVER_HOST = "0.0.0.0"  # tcp server hosted at ngrok or other app
# SERVER_PORT = 8000 # port at tcp server
# separator_token = "<SEP>"

# # initialize TCP socket
# s = socket.socket()
# print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")

# # connect to the server
# s.connect((SERVER_HOST, SERVER_PORT))
# print("[+] Connected.")

# set up sqlite database
app = Flask(__name__)
con = sqlite3.connect('chats.db', check_same_thread=False)
db = con.cursor()


@login_required
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        usn = request.form.get("username")
        return redirect("/")



@login_required
@app.route("/send", methods=['GET', 'POST'])
def send():
    if request.method == "GET":
        return
    else:
        # get the message sent by user
        msg = request.form.get('msg')
        print("Sent a message")
        print(msg)
        
        time_now = datetime.now().strftime('%H:%M:%S')
        # to_send = f"{client_color}[{time_now}] {usn}: {msg}{Fore.RESET}"
        # s.send(to_send.encode())
        
        
        data = [usn, msg, time_now]
        db.execute("INSERT INTO chat (usn, msg, timestamp) VALUES (?, ?, ?);", data)

        return redirect("/")