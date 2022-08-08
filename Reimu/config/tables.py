import sqlite3


async def tablecreate():
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

        cur.execute("""CREATE TABLE IF NOT EXISTS loveprofile(
            name TEXT,
            first_member INT,
            second_member INT,
            date INT,
            steamy_online INT DEFAULT 0,
            balance INT DEFAULT NULL,
            room TEXT
        )""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS warn(
            guild BIGINT,
            con BIGINT,
            id BIGINT,
            adm BIGINT,
            reason TEXT,
            date TEXT)
        """)

        cur.execute("""CREATE TABLE IF NOT EXISTS ticket(
            category BIGINT DEFAULT 1002633841086824530
            )
        """)

        cur.execute("""CREATE TABLE IF NOT EXISTS createdtickets(
            channel BIGINT,
            id BIGINT)
        """)
        cur.execute("""CREATE TABLE IF NOT EXISTS events(
            event_name TEXT,
            about_event BIGTEXT,
            event_gif BIGTEXT,
            awards BIGTEXT
        )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS created_events(
            eventer BIGINT,
            event_name TEXT,
            event_code TEXT,
            channel BIGINT
        )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS loverooms(
            channel
        )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS room_voice(
            channel INT,
            id INT
        )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS donate(
            user_id INT,
            money INT,
            bill_id VARCHAR,
            type TEXT
        )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS sponsor(
            user_id INT,
            date TEXT
        )""")


        

