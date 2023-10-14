import sqlite3, hashlib, socket, threading, os, time
import init_db
from icecream import ic
from cryptography.fernet import Fernet

""" 
Status:
    Login funkar
    Registrering funkar
    Kryptering funkar
    
Att göra:
#Skapa en funktion som skriver en fil med Fernet nycklar för 30 dagar -
#-och som automatiskt väljer nyckel beroende på dag i månaden.
#Whisper funktion
"""

myFernetKey = b'q7qDPOZInGtw50dngbM3MZdVKejQFzYPrURqaks5kxU='
myFernetCipher = Fernet(myFernetKey)


os.system('cls') if os.name == 'nt' else os.system('clear')
host, port = "localhost", 9998

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

admins    = list()
clients   = list()
usernames = list()

# Cipher
myKey = b'q7qDPOZInGtw50dngbM3MZdVKejQFzYPrURqaks5kxU='
myCipher = Fernet(myKey)
def mySend(client, text):
    text = text.encode()
    text = myCipher.encrypt(text)
    return client.send(text)

def myReadClient(client, *username):
    message = client.recv(1024)
    if message:
        return myCipher.decrypt(message).decode()
    else:
        return None
    
# Register new users
def myNewUser(username, password, c):
    conn = sqlite3.connect('userdata.db')
    cur = conn.cursor()
    print('1. NewUser: OsPath test:','userdata.db')
    
    cur.execute("SELECT * FROM userdata WHERE  username = ?", (username,)) 
    print(f'2. NewUser: Requested for registration :', username)
    
    if not cur.fetchone():
        print(f'3. NewUser: Username:', username, 'is Available')
        cur.execute("INSERT INTO userdata (username, password) VALUES (?,?)", (username, password))
        conn.commit()
        
        
        print(f'4. NewUser: {username} added!')
        mySend(c,f'[Server]:\nRegistration of account "{username}" was successful!')
        c.close
        cur.close()
        return
    
    print(f'X. NewUserDebug: username: {username} was taken')
    mySend(c, "Username taken.")
    cur.close()
    
# Setting up connections and authentication.
def recieve():
    while True:
        client, addr = server.accept()
        ic('Connected with',str(addr))
        
        thread = threading.Thread(target=authenticate, args=(client,))
        thread.start()
        
        
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
                ic("AuthDebug 1: checking logins against database...")
                conn = sqlite3.connect('userdata.db')
                cur = conn.cursor()
                cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))
                

                if cur.fetchall():
                    ic("AuthDebug 2: Login Success")
                    clients.append(client)
                    usernames.append(username)
                    mySend(client,"Login successful!")
                    
                    ic("AuthDebug 3: Broadcasting that client has joined.")
                    broadcast(f'[Server] : {username} has joined the chat!',whichclient=client)
                    
                    ic("AuthDebug 4: Sending client to 'handle_client'")
                    handle_client(client, username)
                    
                else:
                    mySend(client,"Login failed!")
                cur.close()
            
    except Exception as e: 
        print(f'Authentication error: {e}')


# Chat Stuff
def handle_client(client, username):
    amountSent = 0
    while True:
        try:
            while client in clients:
                ic("HandleDebug 1: Waiting for message from client")
                msg = myReadClient(client)
                
                if not msg:
                    client.close
                    clients.remove(client)
                    usernames.remove(username)
                    broadcast(f'{username} has left the chat!')
                    break
                
                match msg.split()[1]:
                    case '': pass
                    case __:
                            ic("HandleDebug 2: Sending message to broadcast function.")
                            broadcast(msg, whichclient=client)

                            amountSent += 1
                            ic(f"HandleDebug Messages : {amountSent}")
                
        except Exception as e:
            print(f'["Handle Client" ExceptionError]:\n{e}')

# BROADCAST
def broadcast(message, whichclient=None):
    try:
        originalmessage = message[:]
        message = message.encode()
        message = myCipher.encrypt(message)

        #ic("BroadcastDebug 1: Trying to broadcast message from client")
        for client in clients: 
                if client != whichclient:
                    ic(client.send(message))

        print(f'[Broadcasting message]\n{originalmessage}\n[End Of Message]')

        #ic("BroadcastDebug 2: Broadcast Completed on this part")
    
    except Exception as e:
        print(f'["Broadcast" ExceptionError]:\n{e}')
    

# Starta Servern

print(f'Server IP: {host} \nPort: {port}')
print(f"[Listening...]")
recieve()
