import sqlite3
from sqlite3 import OperationalError


class DbConexion:
    def __init__(self):
        self.conexion = sqlite3.connect("bd1.db")
        self.create_tables()


    def get_db_connection(self):
        connection = sqlite3.connect('bd1.db')
        connection.row_factory = sqlite3.Row
        return connection


    def create_tables(self):
        try:
            self.conexion.execute("""create table movie (
                                      id integer primary key autoincrement,
                                      title text,
                                      genre text,
                                      premiere text,
                                      runtime integer,
                                      score real,
                                      language text)""")
        except OperationalError as op:
            print('WARN: ' + str(op))


