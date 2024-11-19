import sqlite3

connection_2 = sqlite3.connect('not_telegram.db')
cursor = connection_2.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

'''
for i in range(1, 11):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)', (f'User{i}',
                                                                                           f'example{i}@gmail.com',
                                                                                            f'{i}0', '1000'))
'''
#for i in range(1, 11, 2):
    #cursor.execute('UPDATE Users SET balance = ? WHERE username = ?', (500, f'User{i}'))

#for i in range(1, 11, 3):
    #cursor.execute('DELETE FROM Users WHERE username = ?', (f'User{i}',))

cursor.execute('SELECT * FROM Users WHERE age != ?', (60,))
users = cursor.fetchall()
for user in users:
    print(f'Имя: {user[1]} | Почта:{user[2]} | Возраст:{user[3]}| Баланс: {user[4]}')

connection_2.commit()
connection_2.close()



