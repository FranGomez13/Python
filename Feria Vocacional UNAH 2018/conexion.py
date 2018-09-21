import sqlite3


class Conexion:
    def __init__(self):
        self.__con = sqlite3.connect('feria.db')
        with self.__con:
            cursor = self.__con.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS 'tblferia' (\
                    'id'    INTEGER PRIMARY KEY AUTOINCREMENT,\
                    'nombre'  TEXT NOT NULL,\
                    'colegio' TEXT NOT NULL,\
                    'correo'  TEXT NOT NULL\
                )"
            )

    def insertar(self, nombre, colegio, correo):
        self.__con = sqlite3.connect('feria.db')
        with self.__con:
            cursor = self.__con.cursor()
            cursor.execute(
                "INSERT INTO tblferia('nombre','colegio','correo')VALUES('" +
                nombre + "','" + colegio + "','" + correo + "')"
            )
