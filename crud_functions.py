import sqlite3


def initiate_db(db_name="products.db"):
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL,
            image_url TEXT NOT NULL
        )
        """)
        

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL DEFAULT 1000
        )
        """)
        
        connection.commit()
        connection.close()
        print("Таблицы Products и Users успешно созданы или уже существуют.")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")


def add_user(username, email, age, db_name="products.db"):
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        

        cursor.execute("""
        INSERT INTO Users (username, email, age, balance) 
        VALUES (?, ?, ?, 1000)
        """, (username, email, age))
        
        connection.commit()
        connection.close()
        print(f"Пользователь '{username}' успешно добавлен.")
    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")


def is_included(username, db_name="products.db"):
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        

        cursor.execute("""
        SELECT 1 FROM Users WHERE username = ?
        """, (username,))
        user_exists = cursor.fetchone() is not None
        
        connection.close()
        return user_exists
    except Exception as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return False



def get_all_products(db_name="products.db"):
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        

        cursor.execute("SELECT id, title, description, price, image_url FROM Products")
        products = cursor.fetchall()
        
        connection.close()
        return products
    except Exception as e:
        print(f"Ошибка при получении продуктов: {e}")
        return []
