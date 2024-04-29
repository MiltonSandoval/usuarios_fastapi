#importaciones
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
#Importaciones Locales
from db.conexion import db_client
from db.schema.esquema_users import user_json, user_list

#Se guarda Fastapi en la variable app
app = FastAPI()


#Se crea una clase usuario y se hereda de la importacion Basemodel
#Clase que llevara los datos del registro de los usuarios
class usuario(BaseModel):
    id : str = None
    nombre : str
    apellido : str
    edad : int
    correo : str
    contrasena : str
    telefono : str
#classe que recogera los datos del login y los comparara con los del registro
class login_user(BaseModel):
    correo : str
    contrasena : str

#endpoint que muestra todos los usuarios registrados en la base de datos
@app.get("/login/usuarios",response_model= list[usuario])
async def user_all():
    # Obtener la lista de objetos JSON
    return user_list(db_client.local.users.find())

#endpoint que sirve para registrarte y se guarda en la base de datos
@app.post("/registro", status_code=201)
async def registro(usuarios:usuario):
    #se busca si el correo ya se encuentra registrado en la base de datos o no
    if type(buscar_correo("correo", usuarios.correo)) == usuario:
        #si el correo ya esta registrado, se devuelve un 404 con los detalles
        raise HTTPException(status_code=404,
                            detail="El usuario ya existe")
    #si no esta registrado, se transforma el usuario en un diccionario para eliminar el id que trae
    users_dic = dict(usuarios)
    del users_dic["id"]
    #se guarda el usuario y al mismo tiempo se trae el id con el que fue guardado
    id = db_client.local.users.insert_one(users_dic).inserted_id
    #se busca en la base de datos el usuario guardad con el id generado
    new_users = user_json(db_client.local.users.find_one({"_id":id}))
    #se devuelve el usuario registrado en la base de datos
    return new_users
#endpoint login que recibe correo y contrasena
@app.post("/login", status_code=200)
async def login(user: login_user):
    #se guarda en la variable el usuario completo con el correo pasado
    user_busqueda = buscar_correo("correo", user.correo)
    #si no se encuentra el correo, se llama a la funcion error_login() para que se ejecute un raise
    if not type(user_busqueda) == usuario:
        error_login()
    #aqui se verifica si la contrasena es incorrecta y se repite lo del error
    if not user_busqueda.contrasena == user.contrasena:
        error_login()
    #si no se a entrado a ningun raise, entonces los datos estan bien y se procede a dar la bienvenida
    return {"Mesagge":"Bienvenido " + user_busqueda.nombre}

#FUNCION QUE SIRVE PARA BUSCAR ALGUN DATO EN LA BASE DE DATOS, SE RECIBE EL CAMPO Y EL DATO A BUSCAR
def buscar_correo(llave: str, password):
    #TRY QUE SIRVE PARA MANEJAR LOS DATOS NO ENCONTRADOS Y NO ENCONTRADOS
    try:
        return usuario(**user_json(db_client.local.users.find_one({llave:password})))
    except:
        return {"message":"Error al buscar al usuario"}
#FUNCION DE ERROR QUE DA UN 404 Y EL MENSAJE DE DATOS INVALIDOS
def error_login():
    raise HTTPException(status_code=404, detail="Datos invalidos")
