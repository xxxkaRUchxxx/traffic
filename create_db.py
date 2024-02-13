import sqlite3

conn = sqlite3.connect('db.sqlite3')

try:
    cursor = conn.cursor()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS upload_list (
                        id INTEGER PRIMARY KEY,
                        date TEXT,
                        donor_video TEXT,
                        channel_id INTEGER,
                        upload_ch_url TEXT,
                        FOREIGN KEY (channel_id) REFERENCES upload_channel(id))''')
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS upload_channel (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        tematic TEXT,
                        url TEXT,
                        email TEXT,
                        pass TEXT)''')
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS donor_channel (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        tematic TEXT,
                        count INTEGER,
                        url TEXT)''')
    cursor.execute(f"INSERT INTO orders (order_id, user_id, count, discount, master, order_list, order_date) "
                   f"VALUES (?, ?, ?, ?, ?, ?, ?)", (0, 0, 0, 0, 0, 0, 0))
    conn.commit()
    print('База данных "db.sqlite3" успешно создана')
except Exception as e:
    print('Error create db\n', e)
finally:
    conn.close()
