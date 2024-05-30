from database import User, Escuela, Categoria

from typing import Dict, Any

from fastapi import HTTPException


async def validate_rol(rol_oauth: str):

    if rol_oauth != "supervisor":
        raise HTTPException(status_code=400, detail="No tiene permisos para realizar esta operacion")


async def validate_school(school: str):

    if not Escuela.select().where(Escuela.nombre == school).exists():
        raise HTTPException(status_code=400, detail="La escuela no existe")
    
async def validate_category(category: str):

    if not Categoria.select().where(Categoria.nombre == category).exists():
        raise HTTPException(status_code=400, detail="La categoria no existe")
    
async def validate_user(user: str):

    if not User.select().where(User.username == user).exists():
        raise HTTPException(status_code=400, detail="El usuario no existe")


async def validate_item(item: Dict[str, Any]):
    for key, value in item.items():
        if not value:
            raise HTTPException(status_code=400, detail=f"El campo '{key}' no puede estar vacío")