import sqlite3, time

db_name = "robodb.sqlite"
tb_name = "robotb"
columns = "(date INTEGER, location TEXT, name TEXT, description TEXT)"
seconds = 604800    # 1 week
ancient = 31540000  # 1 year

class DBHelper:
    def __init__(self):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)

    def create_table(self):
        # Question mark style does not work here for some unknown reason
        # This way of string formatting may be vulnerable to SQL injction
        stmt = "CREATE TABLE IF NOT EXISTS {} {}".format(tb_name, columns)
        self.connection.execute(stmt)
        self.connection.commit()

    def insert(self, location, name, description):
        stmt = "INSERT INTO ? ? VALUES ?"
        args = (int(time.time()), location, name, description)
        self.connection.execute(stmt, (tb_name, columns, str(args)))
        self.connection.commit()

    def select_recent(self):
        last = int(time.time()) - seconds
        stmt = "SELECT * FROM ? WHERE date >= ?"
        rows = self.connection.execute(stmt, (tb_name, last))
        return rows

    def delete_old(self):
        last = int(time.time()) - ancient
        stmt = "DELETE FROM ? WHERE date >= ?"
        self.connection.execute(stmt, (tb_name, last))
        self.connection.commit()
