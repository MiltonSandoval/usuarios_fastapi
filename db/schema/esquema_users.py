def user_json(user):
    return {"id": str(user["_id"]),
            "nombre": user["nombre"],
            "apellido": user["apellido"],
            "edad": user["edad"],
            "correo": user["correo"],
            "contrasena": user["contrasena"],
            "telefono": user["telefono"] }

def user_list(users) -> list:
    return [user_json(user) for user in users]
