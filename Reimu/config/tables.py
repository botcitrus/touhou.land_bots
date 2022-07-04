import sqlite3


def tablecreate():
    with sqlite3.connect("databases/database.db") as db:
        cur = db.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS private_voice(
            channel INT,
            id INT
        )""")