import sqlite3


class Db:

    def __init__(self, file):
        self.connect = sqlite3.connect(file)
        self.cursor = self.connect.cursor()

    def execute(self, request, params=None):
        if params:
            self.cursor.execute(request, params)
        else:
            self.cursor.execute(request)

        self.connect.commit()
        return self.cursor

    def fetch_all(self):
        return self.cursor.fetchall()