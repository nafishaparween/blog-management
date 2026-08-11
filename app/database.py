import sqlite3

connection = sqlite3.connect('blog.db', check_same_thread=False)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL)
            """)

cursor.execute("""
                CREATE TABLE IF NOT EXISTS posts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                image TEXT,
                user_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id) 
                )"""
                )
connection.commit()
