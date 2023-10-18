import socket, threading, hashlib, time
from myCreateKeyFile import myReadKeys
from myEncryption import myCipher, myDecipher


# <if you want a clear terminal uncomment the next two lines>
#import os
#os.system('cls') if os.name == 'nt' else os.system('clear')



# Encryption
myKeysPath = 'myKeys.txt'
try: open(myKeysPath).close()
except FileNotFoundError: 
    print(f'You are missing a file with keys.')
    print(f'You can create new keys with the "myGenerateKeys" function from "myCreateKeyFile.py"')
    print(f'This file must be shared between the server and the users')

myKey = myReadKeys()

def mySend(text):
    text = myCipher(text, myKey)
    return client.send(text.encode())

def myReadClient():
    message = client.recv(1024).decode()
    message = myDecipher(message, myKey)
    return message


# Authentication
def myLogin(client):
    while True:
        # Username
        username =  input(myReadClient())
        mySend(username)
        
        # Password
        password = input(myReadClient())
        password = hashlib.sha3_256(password.encode()).hexdigest()
        password = myCipher(password, myKey)
        client.send(password.encode())
        
        # Validation
        authentication = myReadClient()
        match authentication.split()[-1]:
            
            case 'successful!':
                print(authentication)
                threading.Thread(target=write,args=(username,)).start()
                threading.Thread(target=recieve).start()

            case _____________:
                print(authentication)
                continue

# Registration
def myRegistration(client):
    try:
        print(f'\nPlease register your account.')
        while True:
            # Username
            username = input(myReadClient())
            match username:
                case 'quit': break
                case ______: mySend(f"REGISTER {username}")


            # Password
            password = input(myReadClient())
            match password:
                case 'quit': break
                case ______:
                    password = hashlib.sha3_256(password.encode()).hexdigest()
                    password = myCipher(password, myKey)
                    client.send(password.encode())

            
            # Verification
            auth = myReadClient()
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
            message = myReadClient()
            if message: print(f'{message}')
    
            else: print('Connection Lost!');client.close;break
    except Exception as e:
        print(f'[Function "recieve"] ExceptionError:\n{e}')


def write(username):
    try:
        while True:
            text = f'{username}: {input(f"{username}: ").lstrip()}'
            match text.split(': ')[1]:
                case '': continue
                case __: mySend(text)
        
    except Exception as e:
        print(f'[Function "write"] ExceptionError:\n{e}')


"""
                <( End of functions )>
"""

"""
             <( This is the Main Menu )>
"""
                    # Main Menu
while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = input("Please enter the IP-Address of the Server you wish to connect to:\n>")
    match address:
        case "default": address, port = "192.168.1.20", 9999
        case "debug"  : address, port = "localhost"   , 9999
        case _________: 
            while True:
                port = int(input("Please enter a portnumber between 9000-65535:\n>"))
                if 9000 <= port <= 65535: break
    
    try: client.connect((address, port))
    except ConnectionRefusedError as c:
        print(c); continue
    
    except Exception as e:
        print(e)

    while True:
        try:
            userinput = input(f"1. Login\n2. Register\n>")
            match userinput:
                case "1": myLogin(client)
                case "2": myRegistration(client)
                case ___: continue

            client.close
            time.sleep(1)
            break
        except Exception as e:
            print(e)
            break
            
            
