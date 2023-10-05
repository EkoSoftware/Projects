import sqlite3
import hashlib
import os


conn = sqlite3.connect('userdata.db')
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS userdata (
    id INTEGER PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
)
""")

username1, password1 = "doggo", hashlib.sha256("doggo".encode('utf-8')).hexdigest()
username2, password2 = "admin", hashlib.sha256("adminpass".encode('utf-8')).hexdigest()
username3, password3 = "joshua", hashlib.sha256("joshuapass".encode('utf-8')).hexdigest()
username4, password4 = "you", hashlib.sha256("shallnotpass".encode('utf-8')).hexdigest()
print(password1)

cur.execute("INSERT INTO userdata (username, password) VALUES (?,?)", (username1, password1))
cur.execute("INSERT INTO userdata (username, password) VALUES (?,?)", (username2, password2))
cur.execute("INSERT INTO userdata (username, password) VALUES (?,?)", (username3, password3))
cur.execute("INSERT INTO userdata (username, password) VALUES (?,?)", (username4, password4))
cur.execute("INSERT INTO userdata (username, password) VALUES (?,?)", ("textuser", "textpass"))
cur.execute("INSERT INTO userdata (username, password) VALUES (?,?)", ("användarnamn", "lösenord"))

conn.commit()
conn.close()