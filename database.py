import pymysql

class Database:
    def __init__(self):
        # Configuración de conexión a la base de datos
        self.host = 'localhost'        # Cambia esto si usas otro host
        self.user = 'tu_usuario'       # Usuario de la base de datos
        self.password = 'tu_contraseña' # Contraseña de la base de datos
        self.db = 'nombre_de_tu_base_de_datos' # Nombre de tu base de datos

        # Conectar a la base de datos
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.db,
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.connection.cursor()
            print("Conexión exitosa a la base de datos")
        except Exception as e:
            print(f"Error en la conexión a la base de datos: {e}")

    def fetch_user(self, username, password):
        """Método para obtener un usuario según su username y password"""
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(sql, (username, password))
        return self.cursor.fetchone()

    def close(self):
        """Cerrar la conexión a la base de datos"""
        self.connection.close()

# Ejemplo de uso en caso de ejecutar este archivo por separado
if __name__ == "__main__":
    db = Database()
    user = db.fetch_user('admin', 'adminpassword')
    if user:
        print("Usuario encontrado:", user)
    else:
        print("Usuario no encontrado")
    db.close()
