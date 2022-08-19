import sqlite3


con = sqlite3.connect('users.db')
cursor = con.cursor()
cursor.execute('create table if not exists Cred(website varchar, username varchar, password varchar)')

cursor.execute('insert into Cred values("sd","sd","sd")')

con.commit()
con.close()