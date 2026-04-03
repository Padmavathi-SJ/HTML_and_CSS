import sqlite3
from datetime import datetime

conn = sqlite3.connect("chat.db") 
cursor = conn.cursor() #

def create_table():
    cursor.execute("""
        create table if not exists messages (
            id integer primary key autoincrement,
            room text,
            sender text,
            receiver text,
            message text,
            timestamp text
        )
    """)
    conn.commit()

def save_message(room, sender, receiver, message):
    cursor.execute(
        "insert into messages (room, sender, receiver, message, timestamp) values (?, ?, ?, ?, ?)",
        (room, sender, receiver, message, str(datetime.now())
         )
    )
    conn.commit()

def get_messages(room):
    return cursor.execute(
        "select sender, message, timestamp from messages where room=? order by id asc",
        (room,)
    ).fetchall()