import mysql.connector

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='127.0.0.1',
            user='adms2',
            password='9ss3xa',
            database='s9923aas'
        )
        self.cursor = self.connection.cursor()

    def insertar_autor(self, nombre, apellido):
        sql = "INSERT INTO autores (nombre, apellido) VALUES (%s, %s)"
        self.cursor.execute(sql, (nombre, apellido))
        self.connection.commit()
        return self.cursor.lastrowid

    def insertar_libro(self, titulo, autor_id):
        sql = "INSERT INTO libros (titulo, autor_id) VALUES (%s, %s)"
        self.cursor.execute(sql, (titulo, autor_id))
        self.connection.commit()
        return self.cursor.lastrowid

    def obtener_libros(self):
        sql = "SELECT l.id, l.titulo, a.nombre, a.apellido FROM libros l JOIN autores a ON l.autor_id = a.id"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def cerrar_conexion(self):
        self.cursor.close()
        self.connection.close()