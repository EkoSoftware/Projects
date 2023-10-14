import socket
import threading
import hashlib
from icecream import ic
import os
import time
from cryptography.fernet import Fernet
# Notis: Kryptering klar,
# Ska börja rensa upp texten

os.system('cls') if os.name == 'nt' else os.system('clear')
address, port = "localhost", 9998

# Cipher
myKey = b'q7qDPOZInGtw50dngbM3MZdVKejQFzYPrURqaks5kxU='
myCipher = Fernet(myKey)
def mySend(text):
    text = text.encode()
    text = myCipher.encrypt(text)
    return client.send(text)

def myReadClient():
    message = client.recv(1024)
    message = myCipher.decrypt(message).decode()
    return message
    
# Authentication
def myLogin(client):
    while True:
        username =  input(myReadClient())
        mySend(username)
        
        password = input(myReadClient())
        password = hashlib.sha3_256(password.encode()).hexdigest()
        password = myCipher.encrypt(password.encode())
        client.send(password)
        
        
        authentication = myReadClient()
        #time.sleep(1)
        match authentication.split()[-1]:
            
            case 'successful!':
                print(authentication)
                threading.Thread(target=write,args=(username,)).start()
                threading.Thread(target=recieve).start()

            case _:
                print(authentication)
                continue

# Registration
def myRegistration(client):
    try:
        print(f'\nPlease register your account.')
        #print(f'\nWrite "quit" at any time to return to the main menu.')
    
        while True:
            username = input(myReadClient())
            match username:
                case 'quit': break
                case ______: mySend(f"REGISTER {username}")

            #print(f'[Debug myRegistration (1)] username sent : {username}')
            password = input(myReadClient())
            match password:
                case 'quit': break
                case ______:
                    #ic('[Debug myRegistration (2)] password sent :',password)
                    password = hashlib.sha3_256(password.encode()).hexdigest()
                    password = password.encode()
                    password = myCipher.encrypt(password)
                    client.send(password)


                    auth = myReadClient()
                    #print(auth.split())
                    ic('[Debug myRegistration (3)]  : Waiting for authentication')
                    match auth.split()[-1]:
                        case "successful!":
                            print(auth);client.close;return
                        case _:
                            print(auth);continue

        return
    
    except Exception as e:
        print(f'[Function myRegistration Error]\n{e}!If this is the only text there is a Fernet Error!')    

# Chat Functions
def recieve():
    try:
        while True:
            getMsg = myReadClient()
            if getMsg: print(f'{getMsg}')
            
            
            else: print('Connection Lost!')
            client.close
            break
    
    except Exception as e:
        print(f'[Function "recieve"] ExceptionError:\n{e}')
        
def write(username):
    try:
        while True:
            text = input(f'{username}: ')
            sendMsg = f"{username}: {text}"
            mySend(sendMsg)
        
    except Exception as e:
        print(f'[Function "write"] ExceptionError:\n{e}')
    

# Main Loop
while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((address, port))
    
    while True:
        userinput = input(f"1. Login\n2. Register\n>")
        match userinput:
            case "1": myLogin(client)
            case "2": myRegistration(client)
            case ___: continue
        
        client.close
        time.sleep(1)
        break

            
