import sqlite3
import hashlib
import socket
import threading
import os

os.system('cls') if os.name == 'nt' else os.system('clear')
host, port = "localhost", 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

print()

def myNewUser(username, password, c):
    conn = sqlite3.connect('userdata.db')
    cur = conn.cursor()
    print('New User OsPath test:','userdata.db')
    
    cur.execute("SELECT * FROM userdata WHERE  username = ?", (username,)) 
    print(f'1.NewUserError: Requested for registration :', username)
    
    if not cur.fetchone():
        print(f'2. NewUser: username:', username, 'is Available')
        cur.execute("INSERT INTO userdata (username, password) VALUES (?,?)", (username, password))
        conn.commit()
        
        
        print(f'3. NewUser: {username} added!')
        
        c.send(f"Registration of account {username} was successful!".encode('utf-8'))
        cur.close()
        return
    
    print(f'1.NewUserError:', username,'was taken')
    c.send("Username taken.".encode('utf-8'))
    cur.close()

def authenticate(c):
    try:
        while True:
            c.send("Username: ".encode('utf-8'))
            username = c.recv(1024).decode('utf-8')
                
            c.send("Password: ".encode('utf-8'))
            password = c.recv(1024)
            password = hashlib.sha256(password).hexdigest()
            
            print(f'{username} : {password}')
            
            if username.startswith('REGISTER '): 
                username = username.split()[1]
                myNewUser(username, password, client)
                continue
            else:
                conn = sqlite3.connect('userdata.db')
                cur = conn.cursor()
                cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

                if cur.fetchall():
                    c.send("Login successful!".encode('utf-8'))
                else:
                    c.send("Login failed!".encode('utf-8'))
                cur.close()
                
    except Exception as e: 
        print(f'Authentication error: {e}')
        
print(F'Server IP: {host} \nPort: {port}')
print("Listening for Connections ...")
while True:
    
    client, addr = server.accept()
    threading.Thread(target=authenticate(client), args=(client,)).start()
