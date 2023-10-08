import socket
import threading
import hashlib
from icecream import ic
import os
import time
os.system('cls') if os.name == 'nt' else os.system('clear')


address, port = "192.168.1.20", 9999

    

def myLogin(client):
    while True:
        message = client.recv(1024).decode()
        username =  input(message)
        client.send(username.encode())
        passwordrequest = client.recv(1024).decode()
        password = hashlib.sha256(input(passwordrequest).encode()).hexdigest()
        client.send(password.encode())
        authentication = client.recv(1024).decode()
        if authentication.endswith("successful!"):
            print(authentication)
            write_thread = threading.Thread(target=write,args=(username,))
            write_thread.start()
            recieve_thread = threading.Thread(target=recieve())
            recieve_thread.start()
        else:
            print(authentication)
            continue


def myRegistration(client):
    print(f'Write "quit" at any time to return to the main menu.')
    username = ''
    while True:
        username = client.recv(1024).decode()
        username = input(username)
        if "quit" == username: break
        client.send(f"REGISTER {username}".encode())
        
        password = client.recv(1024).decode()
        password = input(password)
        if password == 'quit': break
        client.send((hashlib.sha256(password)).hexdigest().encode())
        auth = client.recv(1024).decode()
        
        if auth.endswith("successful!"):
            print(auth)
            client.close
            return
        else:
            print(auth)
            continue
    
    
    ic(client.send("CLOSE".encode()*8))
    ic(client.close)
    return

def recieve():
    try:
        while True:
            getMsg = client.recv(1024).decode()
            if not getMsg:
                print('Connection Lost!')
                break
                client.close
            print(f'[SERVER]: {getMsg}')
    except Exception as e:
        print('RcvExceptionError',e)
        
def write(username):
    try:
        while True:
            sendMsg = f"{username}: {input(f'{username}: ')}"
            client.send(sendMsg.encode())
    except Exception as e:
        print('Write ExceptionError: ',e)
    except KeyboardInterrupt:
        print('KeyboardInterrupt noted\nShutting down connection.')
        client.close


while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((address, port))
    while True:
        userinput = input(f"1. Login\n2. Register\n>")
        if userinput in "12":
            if userinput == "1": myLogin(client)
            if userinput == "2": myRegistration(client)
            client.close
            time.sleep(1)

            break
            
