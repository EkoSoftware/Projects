import socket
import threading
import os

clear_screen = 'cls' if os.name == 'nt' else 'clear';os.system(clear_screen)
    
while True:
    choice = input("Enter Server IP:\n>")
    if choice == "localhost": host = "127.0.0.1"
    elif choice == "default": host = "192.168.1.10"
    else: host = choice
    host_check = ''.join(x for x in host if x != ".")
    
    if host_check.isdigit(): break
    else: print('Invalid IP try again.')
while True:
    try:
        port = int(input("Enter port between 10000-65000:\n>"))
        if not 10000 <= port <= 65000: 
            print("port must be between 10000-65000")
        else:break   
    except ValueError:
        print("Please enter only digits")
        
#host = "192.168.1.10"    
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

os.system(clear_screen)
nickname = input("Choose a nickname\n>")
if nickname == 'admin':
    password = input('Enter password for admin:\n>')
nickLength = len(nickname)+2

stop_thread = False 

colors = {
    "black": "\u001b[30m",
    "red": "\u001b[31m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33m",
    "blue": "\u001b[34m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m"
}
usercolor = colors["blue"]

def recieve():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
                next_message = client.recv(1024).decode('utf-8')
                if next_message == 'PASS':
                    client.send(password.encode('utf-8'))
                    if client.recv(1024).decode('utf-8') == 'REFUSE':
                        print('Connection was refused!: Wrong password!')
                        stop_thread = True
                elif next_message == 'BAN':
                    print('Connection was refused because you are banned.')
                    client.close()
                    stop_thread = True
            else:
                if nickname in message[len(nickname):]:
                    continue
                else:
                    print(message)
        except:
            print("Connection Lost!")
            client.close()
            break

def write():
    global usercolor
    while True:
        try:
            if stop_thread:
                break
            
            message = f'{nickname}: {usercolor+input(f"{usercolor+nickname}: ")}'
            text = message.split()[1]
            print('debug:',message.split())
            
            
            if text.startswith(usercolor+'/'):
                if text.startswith(usercolor+'//'):
                    if nickname == 'admin':
                        userToKickBan = message.split()[2]
                        if text.startswith(usercolor+'//kick'):
                            client.send(f'KICK {userToKickBan}'.encode('utf-8'))
                            print(f'debugSend:\nKICK {userToKickBan}')
                        elif text.startswith(usercolor+'//ban'):
                            client.send(f'BAN {userToKickBan}'.encode('utf-8'))
                            print(f'debugSend:\nBAN {userToKickBan}')

                if text.startswith(usercolor+'/color'):
                    color_command = message.split()[2]
                    if color_command in colors:
                        usercolor = colors[color_command]
                        continue
                    else:
                        print("Invalid color. Available colors:", list(colors.keys()))
                        continue
                elif text.startswith(usercolor+'/help'):
                    print("Commands available to you:\n/color white\nAvailable colors: black, red, green, yellow, blue, magenta, cyan, white")
                    continue
            else:
                client.send(message.encode('utf-8'))
        except Exception as e:
            print(e)
            
recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
