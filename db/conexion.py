import pyodbc

# Configura la cadena de conexión con Windows Authentication
server = 'LAPTOP-3MN70QT8'
database = 'users'

try:
    # Intenta establecer la conexión
    connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    )
    print("Conexión exitosa")
except pyodbc.Error as e:
    print(f"Error al conectar: {e}")


cursor = connection.cursor()
consulta = "insert into Users values('Milton', 'Sandoval', 19, 'sandoval@gmail.com','saijdjiasd', '62207713', 1)"
cursor.execute(consulta)
cursor.commit()

cursor = connection.cursor()
consulta = "SELECT * FROM users"
cursor.execute(consulta)
filas = cursor.fetchall()
for fila in filas:
    print(fila)

consulta = "SELECT * FROM users"
cursor.execute(consulta)

connection.close()
