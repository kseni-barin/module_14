import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

def initiate_db():
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    );
    ''')

    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT OT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        );
        ''')

def add_user(username, email, age):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)', (f'{username}',
                                                                                             f'{email}', f'{age}',
                                                                                             1000))
    connection.commit()

def is_included(username):
    cursor.execute('SELECT * FROM Users WHERE username = ?', (f'{username}',))
    return cursor.fetchone() is not None

def get_all_products():
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    #for product in products:
        #print(product)
    connection.commit()
    return products

initiate_db()

#for i in range(1, 5):
    #cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)', (f'Продукт{i}',
    #                                                                                    f'Описание{i}', f'{i*100}'))

connection.commit()
#connection.close()

