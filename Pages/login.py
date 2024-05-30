from fastapi import HTTPException
from database import User, User_Info


async def login(username, password):

    try:

        if User.select().where(User.activate == False).exists():
            raise HTTPException(status_code=404, detail="El usuario no existe")

        if not User.select().where(User.username == username).exists():
            raise HTTPException(status_code=404, detail="Incorrect username or password")
        
        if not User.select().where(User.password ==  password).exists():
            raise HTTPException(status_code=404, detail="Incorrect username or password")

        user = User.get_or_none(User.username == username)
        user_info = User_Info.select().where(User_Info.user_id == user.id)


        user_info_list = [{

            "id": user.id,
            "rol": user.rol,
            "escuela": user_i.escuela,

        } for user_i in user_info]
        
        return user_info_list
    
    except User.DoesNotExist as e:
        raise HTTPException(status_code=404, detail=f"El usuario: '{user.username}' no fue encontrado")