# Sources:
# Building a Chatbot using Telegram and Python (Part 2) by Gareth Dwyer

from time import strftime, time
from pretty_date import prettify_date
import sqlite3

pholder = "?"
db_name = "robodb.sqlite"
tb_name = "robotb"
col_def = "timestamp INTEGER, name TEXT, location TEXT, description TEXT"
col_all = "timestamp, name, location, description"
col_sub = "{0}, {0}, {0}, {0}".format(pholder)
sec_per_wk = 604800     # 1 week
sec_per_yr = 31540000   # 1 year
min_data_length = 10    # 10 characters
max_data_length = 70    # 70 characters

# See https://stackoverflow.com/questions/7929364 for more details

class DBHelper:
    def __init__(self):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)

    def create_table(self):
        stmt = "CREATE TABLE IF NOT EXISTS {0} ({1})".format(tb_name, col_def)
        self.connection.execute(stmt)
        self.connection.commit()

    def insert(self, input_row):
        is_valid, violations = self.validate_row(input_row)
        if is_valid:
            name, location, description = input_row
            date = int(time())
            args = (date, name, location, description)
            stmt = "INSERT INTO {0} ({1}) VALUES ({2})".format(tb_name, col_all, col_sub)
            self.connection.execute(stmt, args)
            self.connection.commit()
        return (is_valid, violations)

    def select_recent(self):
        last = int(time()) - sec_per_wk
        stmt = "SELECT {0} FROM {1} WHERE timestamp >= {2} ORDER BY timestamp DESC".format(col_all, tb_name, last)
        rows = self.connection.execute(stmt)
        return rows

    def delete_old(self):
        last = int(time()) - sec_per_yr
        stmt = "DELETE FROM {0} WHERE timestamp >= {1}".format(tb_name, last)
        self.connection.execute(stmt)
        self.connection.commit()

    def select_recent_pretty(self):
        return self.prettify_rows(self.select_recent())

    def prettify_rows(self, rows):
        str_builder = ['\n']
        for row in rows:
            str_builder.append("When: {}".format(prettify_date(row[0])))
            str_builder.extend(row[1:])
            str_builder.append("")
        return '\n'.join(str_builder)

    def validate_row(self, input_row):
        bad_length = [data for data in input_row if len(data) > max_data_length or len(data) < min_data_length]
        if bad_length:
            return (False, bad_length)
        return (True, [])
