from flask import Flask, render_template, request,redirect, session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from helpers import login_required
from flask_session import Session
from threading import Thread
import socket
import random
from datetime import datetime
# from colorama import Fore, init, Back

app = Flask(__name__)


app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# initialize colors
# init()

# colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX,
#           Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
#           Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX,
#           Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
#           ]

# choose a random color for the connected client
# client_color = random.choice(colors)

# server's IP address

SERVER_HOST = "0.0.0.0"  # tcp server hosted at ngrok or other app
SERVER_PORT = 8000 # port at tcp server
separator_token = "<SEP>"


# initialize TCP socket
s = socket.socket()

print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")

# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

message = []




@app.route("/")
@login_required
def index():
    def listen_for_messages():
    # keep listening to client's message
        while True:
            msg = s.recv(1024).decode()
            if msg:
                message.append(msg)
                print("")
                print(msg)
                return render_template("index.html", message = message)
    # thread to listen for messages
    t = Thread(target=listen_for_messages)
    t.daemon = True
    t.start()

    print(message)
    return render_template("index.html", message = message)

usn = []
@app.route("/login", methods = ['GET', 'POST'])
def login():
    session.clear()
    
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        usn.append(username)
        session["user_id"] = 1
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
        print(usn)
        
        time_now = datetime.now().strftime('%H:%M:%S')
        to_send = f"{usn[0]}: {msg}"
        s.send(to_send.encode())

        return redirect("/")