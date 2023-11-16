import sqlite3, hashlib, socket, threading
from myEncryption import myCipher, myDecipher
from myCreateKeyFile import myGenerateKeys, myReadKeys
import init_db



""" 
Status:
    Login funkar
    Registrering funkar
    Kryptering funkar
    Krypteringsnyckel-generering funkar
    Filprotokollet för kryptering implementerat
Att göra:
#Whisper funktion
"""

# Uncomment if you want a clear commandline
#import os
#os.system('cls') if os.name == 'nt' else os.system('clear')

# Initialize Server

while True:
    host = input("Server IP or localhost?")
    match host:
        case "debug"      : host, port = "localhost"   , 9999;break
        case "localhost"  : host, port = "localhost"   , 9999;break
        case _________: 
            host = socket.gethostbyname(socket.gethostname())
    port = int(input("Please enter a portnumber between 9000-65535:\n>"))
    if 9000 <= port <= 65535: break

    
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

admins    = list()
clients   = list()
usernames = list()

black = "\u001b[30m"
red = "\u001b[31m"
green = "\u001b[32m"
yellow = "\u001b[33m"
blue = "\u001b[34m"
magenta = "\u001b[35m"
cyan = "\u001b[36m"
white = "\u001b[37m"
reset = "\u001b[0m"

# Encryption
myKeysPath = 'myKeys.txt'
try: open(myKeysPath).close()
except FileNotFoundError: myGenerateKeys()
myKey = myReadKeys()


def mySend(client, text):
    text = myCipher(text, myKey)
    return client.send(text.encode())

def myReadClient(client, *username):
    message = client.recv(1024).decode()
    if message:
        return myDecipher(message, myKey)
    else:
        return None


# Register new users
def myNewUser(username, password, c):
    # Connect to database
    conn = sqlite3.connect('userdata.db')
    cur = conn.cursor()
    print('1. NewUser: OsPath test:','userdata.db')
    cur.execute("SELECT * FROM userdata WHERE  username = ?", (username,)) 
    print(f'2. NewUser: Requested for registration :', username)
    
    # If username is available
    if not cur.fetchone():
        print(f'3. NewUser: Username:', username, 'is Available')
        cur.execute("INSERT INTO userdata (username, password) VALUES (?,?)", (username, password))
        conn.commit()
        
        print(f'4. NewUser: {username} added!')
        mySend(c,f'[Server]:\nRegistration of account "{username}" was successful!')
        c.close
        cur.close()
        return
    
    # If username is taken
    print(f'X. NewUserDebug: username: {username} was taken')
    mySend(c, "Username taken.")
    cur.close()
    
# Accepts Connections and creates a thread for each client while sending them off to authentication.
def recieve():
    while True:
        client, addr = server.accept()
        print('Connected with',str(addr))
        
        thread = threading.Thread(target=authenticate, args=(client,))
        thread.start()
        

# Authentication
def authenticate(client,):
    try:
        while True:
            # Requesting Account details
            mySend(client, f'Username: ')
            username = myReadClient(client)
            if not username: client.close;break
            
                
            mySend(client, f'Password: ')
            password = myReadClient(client)
            if not password: client.close;break
            password = hashlib.sha3_256(password.encode()).hexdigest()
            
            # Debug
            print(f'{username} : \nHashed password: {password}')
            
            # If Client Registers...
            if username.startswith('REGISTER '): 
                username = username.split()[1]
                
                myNewUser(username, password, client)
                continue
            
            # Authenticating Login Details
            else:
                print(f"{green}AuthDebug 1: checking logins against database...{reset}")
                conn = sqlite3.connect('userdata.db')
                cur = conn.cursor()
                cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))
                
                # Valid
                if cur.fetchall():
                    print(f"{green}AuthDebug 2: Login Success{reset}")
                    clients.append(client)
                    usernames.append(username)
                    mySend(client,"Login successful!")
                    
                    print(f"{green}AuthDebug 3: Broadcasting that client has joined.{reset}")
                    broadcast(f'[Server] : {username} has joined the chat!',whichclient=client)
                    
                    print(f"{green}AuthDebug 4: Sending client to 'handle_client'{reset}")
                    handle_client(client, username)
                
                # Invalid
                else:
                    mySend(client,"Login failed!")
                cur.close()
            
    except Exception as e: 
        print(f'{red}Authentication error: {e}{reset}')


# Chat Stuff
def handle_client(client, username):
    amountSent = 0
    while True:
        try:
            while client in clients:
                print("HandleDebug 1: Waiting for message from client")
                msg = myReadClient(client)
                
                if not msg:
                    client.close
                    clients.remove(client)
                    usernames.remove(username)
                    broadcast(f'{username} has left the chat!')
                    break
                
                match msg:
                    case ' ': continue
                    case __:
                            print("HandleDebug 2: Sending message to broadcast function.")
                            broadcast(msg, whichclient=client)

                            amountSent += 1
                            print(f"HandleDebug Messages : {amountSent}")
                
        except Exception as e:
            print(f'{red}["Handle Client" ExceptionError]:\n{e}{reset}')


# Broadcast messages
def broadcast(message, whichclient=None):
    try:
        originalmessage = message[:]
        message = myCipher(message, myKey)

        print("BroadcastDebug 1: Trying to broadcast message from client")
        for client in clients: 
            if client != whichclient:
                client.send(message)

        print(f'{blue}{"[Broadcasting message]":^50}{reset}\n{yellow}{originalmessage:^50}{reset}\n{blue}{"[End Of Message]":^50}{reset}')

    
    except Exception as e:
        print(f'{red}["Broadcast" ExceptionError]:\n{e}{reset}')
    

# Starta Servern
print(f'{blue}Server IP: {green}{host}{reset} \nPort: {yellow}{port}{reset}')
print(f"{cyan}[Listening...]{reset}")
recieve()
