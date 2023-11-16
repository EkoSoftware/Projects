import sqlite3
import hashlib
conn = sqlite3.connect('userdata.db')
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS userdata (
    id INTEGER PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
)
""")

from myCreateKeyFile import myReadKeys
from myEncryption import myCipher
myKey = myReadKeys()    


# Creates Serverside account if this file runs independently.
username = "admin"
password = "adminpass"
original_password = password[:]
password = hashlib.sha3_256(password.encode()).hexdigest()
myCipher(password, myKey)
password = hashlib.sha3_256(password.encode()).hexdigest()

cur = conn.cursor()
cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))
if not cur.fetchall():
    cur.execute("INSERT INTO userdata (username, password) VALUES (?,?)", (username, password))
    conn.commit()
    print(f'Account {username} was created with password {original_password}!')
    conn.close()

