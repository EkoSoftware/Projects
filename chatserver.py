import socket
import threading
import os
import time
clear_screen = 'cls' if os.name == 'nt' else 'clear';os.system(clear_screen)

if not os.path.exists('banlist.txt'):
    open('banlist.txt', 'x').close()
    

host = socket.gethostbyname(socket.gethostname())
while True:
    choice = input("1. Device IP\n2. Local Host\n")
    if choice == "2": host = "127.0.0.1"
    if choice in "12": break 
    else: continue
    
while True:
    try:
        port = int(input("Enter port between 10000-65000:\n>"))
        if not 10000 <= port <= 65000: 
            print("port must be between 10000-65000")
        else:break   
    except ValueError:
        print("Please enter only digits")
    


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

admins = []
clients = []
nicknames = []
os.system(clear_screen)

    
print(F'A banlist.txt has been created in \n{os.getcwd()}\\banlist.txt\n')
print(F'Server ip: {host} \nPort: {port}')

def broadcast(message, whichclient=None):
    if whichclient:
        if client != whichclient:
            client.send(message)
    for client in clients:
            client.send(message)

def handle(client):
    while True:
        try:
            msg = message = client.recv(1024)
            if msg.decode('utf-8').startswith('KICK') and client in admins:
                parts = msg.decode('utf-8').split()
                if len(parts) == 2:
                    name_to_kick = parts[1]
                    kick_user(name_to_kick)
                elif client not in admins:
                    client.send('Command was refused!'.encode('utf-8'))
                        
            elif msg.decode('utf-8').startswith('BAN') and client in admins:
                parts = msg.decode('utf-8').split()
                print(parts)
                if len(parts) == 2:
                    name_to_ban = parts[1]
                    with open('banlist.txt', 'a',) as f:
                        f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} was banned!')
                else:
                    client.send('Command was refused!'.encode('utf-8'))
            else:
                broadcast(message, client)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close
                nickname = nicknames[index]
                broadcast(f"{nickname} left the chat!".encode('utf-8'))
                nicknames.remove(nickname)
                break

def recieve():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        
        with open('banlist.txt', 'r') as f:
            bans = f.readlines()
        
        if nickname+'\n' in bans:
            client.send('BAN'.encode('utf-8'))
            client.close()
            continue
            
        if nickname == 'admin':
            client.send('PASS'.encode('utf-8'))
            password = client.recv(1024).decode('utf-8')
            if password != 'adminpass':
                client.send('REFUSE'.encode('utf-8'))
                client.close()
                continue
            else:
                admins.append(client)
        nicknames.append(nickname)
        clients.append(client)
        
        print(f'Nickname of {address[0]} is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        
def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You were kicked by an admin').encode('utf-8')
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked by an admin!').encode('utf-8')
    
print(f'[LISTENING] Server is listening for connections...')
recieve()    