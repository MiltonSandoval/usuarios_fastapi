cursor = connection.cursor()
consulta = "SELECT * FROM USERS"
cursor.execute(consulta)
connection.commit()