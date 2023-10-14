import sqlite3
import hashlib
import os
from cryptography.fernet import Fernet

conn = sqlite3.connect('userdata.db')
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS userdata (
    id INTEGER PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
)
""")
if __name__ == '__main__':
    username1, password1 = "doggo", hashlib.sha3_256("doggo".encode()).hexdigest()
    username2, password2 = "admin", hashlib.sha3_256("adminpass".encode()).hexdigest()
    
    myKey = b'q7qDPOZInGtw50dngbM3MZdVKejQFzYPrURqaks5kxU='
    myCipher = Fernet(myKey)
    
    password1 = hashlib.sha3_256(password1.encode()).hexdigest()
    password2 = hashlib.sha3_256(password2.encode()).hexdigest()

    #print(type(password2))

    cur.execute("INSERT INTO userdata (username, password) VALUES (?,?)", (username1, password1))
    cur.execute("INSERT INTO userdata (username, password) VALUES (?,?)", (username2, password2))
    

    conn.commit()
    conn.close()
else:
    conn.close()
