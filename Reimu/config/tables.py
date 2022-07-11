import sqlite3


def tablecreate():
    with sqlite3.connect("databases/database.db") as db:
        cur = db.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS private_voice(
            channel INT,
            id INT
        )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS shop(
            con INT,
            role_id INT,
            id BIGINT,
            const INT,
            quantity INT
            )
        """)

        cur.execute("""CREATE TABLE IF NOT EXISTS users(
            id BIGINT,
            hands BIGINT DEFAULT 0,
            bank BIGINT DEFAULT 1000,
            messages BIGINT DEFAULT 0,
            lvl BIGINT DEFAULT 0,
            xp BIGINT DEFAULT 0,
            biography TEXT DEFAULT 'отсутствует',
            spouse BIGINT DEFAULT NULL)
        """)