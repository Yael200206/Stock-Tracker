import pymysql
import base64

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='stocktracker',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()

    def validate_login(self, username, password):
        """Método para validar el inicio de sesión."""
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(sql, (username, password))
        return self.cursor.fetchone()

    def fetch_personnel(self):
        """Método para obtener el personal."""
        sql = "SELECT * FROM personnel"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def fetch_stock(self):
        """Método para obtener el stock de productos."""
        sql = "SELECT * FROM stock"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_person_by_id(self, person_id):
        """Método para obtener una persona específica por ID."""
        sql = "SELECT * FROM personnel WHERE id = %s"
        self.cursor.execute(sql, (person_id,))
        return self.cursor.fetchone()

    def update_person_status(self, person_id, status):
        """Método para actualizar el estado de una persona."""
        sql = "UPDATE personnel SET status = %s WHERE id = %s"
        self.cursor.execute(sql, (status, person_id))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
