#importaciones
from fastapi import FastAPI
from pydantic import BaseModel

#Se guarda Fastapi en la variable app
app = FastAPI()


@app.get("/login/all")
async def login():
    pass



