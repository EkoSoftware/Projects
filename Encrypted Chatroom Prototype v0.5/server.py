import sqlite3
import hashlib
import socket
import threading
import os
import init_db
from icecream import ic
import time


os.system('cls') if os.name == 'nt' else os.system('clear')
host, port = "192.168.1.20", 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

admins = list()
clients = list()
usernames = list()

print()

def myNewUser(username, password, c):
    conn = sqlite3.connect('userdata.db')
    cur = conn.cursor()
    print('1. NewUser OsPath test:','userdata.db')
    
    cur.execute("SELECT * FROM userdata WHERE  username = ?", (username,)) 
    print(f'2. NewUser: Requested for registration :', username)
    
    if not cur.fetchone():
        print(f'3. NewUser: Username:', username, 'is Available')
        cur.execute("INSERT INTO userdata (username, password) VALUES (?,?)", (username, password))
        conn.commit()
        
        
        print(f'4. NewUser: {username} added!')
        c.send(f"Registration of account {username} was successful!".encode())
        c.close
        cur.close()
        return
    
    print(f'X. NewUserError: username: ', username,'was taken')
    c.send("Username taken.".encode())
    cur.close()
    
# Setup
def recieve():
    i = 1
    while True:
        client, addr = server.accept()
        ic(f'Connected with {str(addr)}')
        
        thread = threading.Thread(target=authenticate, args=(client,))
        thread.start()
        
        
def authenticate(client,):
    try:
        while True:
            client.send("Username: ".encode())
            username = client.recv(1024).decode()
            if 'CLOSE'*8 == username: ic('Client has stopped the connection',client.close);break
                
            client.send("Password: ".encode())
            password = client.recv(1024).decode()
            if 'CLOSE'*8 == password: ic('Client has stopped the connection',client.close);break
            
            
            print(f'{username} : {password}')
            
            if username.startswith('REGISTER '): 
                username = username.split()[1]
                ic(myNewUser(username, password, client))
                continue
            else:
                ic("AuthDebug 1: checking logins against database...")
                conn = sqlite3.connect('userdata.db')
                cur = conn.cursor()
                cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

                if cur.fetchall():
                    ic("AuthDebug 2: Login Success")
                    client.send("Login successful!".encode())
                    clients.append(client)
                    usernames.append(username)
                    ic("AuthDebug 3: Broadcasting that client has joined.")
                    broadcast(f'[Server] : {username} has joined the chat!'.encode(),whichclient=client)
                    
                    ic("AuthDebug 4: Sending client to 'handle_client'")
                    handle_client(client, username)
                    
                else:
                    client.send("Login failed!".encode())
                cur.close()
            
    except Exception as e: 
        print(f'Authentication error: {e}')


# Chat Stuff
def handle_client(client, username):
    amountSent = 0
    while True:
        try:
            while client in clients:
                empty = False
                ic("HandleDebug 1: Waiting for message from client")
                msg = client.recv(1024).decode()
                
                if not msg:
                    client.close
                    clients.remove(client)
                    usernames.remove(username)
                    broadcast(f'{username} has left the chat!')
                    break
                
                ic("HandleDebug 2: Sending message to broadcast function.")
                broadcast(msg, client)
                amountSent += 1
                ic(f"HandleDebug Messages : {amountSent}")
            
                
        except Exception as e:
            print(f'Handle Client ExceptionError: {e}')

# BROADCAST
def broadcast(message, whichclient=None):
    ic("BroadcastDebug 1: Trying to broadcast message from client")
    
    for client in clients: 
            if client != whichclient:
                ic(client.send(message.encode()))
    
    print(f'[Broadcasting message]\n{message}\n[End Of Message]')
    
    ic("BroadcastDebug 2: Broadcast Completed on this part")
    
    

# Starta Servern

print(f'Server IP: {host} \nPort: {port}')
print(f"[Listening...]")
recieve()
