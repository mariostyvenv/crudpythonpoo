import sqlite3

class ConexionSqlite:

    def __init__(self):
        self.conexion = sqlite3.connect("./db/words.sqlite")