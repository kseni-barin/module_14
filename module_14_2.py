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

#дополнение к 14_2:
cursor.execute('DELETE FROM Users WHERE id = ?', (6,))

cursor.execute('SELECT COUNT(*) FROM Users')
total = cursor.fetchone()[0]

cursor.execute('SELECT SUM(balance) FROM Users')
total_balance = cursor.fetchone()[0]
print('Cредний баланс всех пользователей:', total_balance/total)

cursor.execute('SELECT AVG(balance) FROM Users')
avg_balance = cursor.fetchone()[0]
print('Cредний баланс всех пользователей:', avg_balance)

connection_2.commit()
connection_2.close()




