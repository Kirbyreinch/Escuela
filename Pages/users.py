import random

from MySQLdb import IntegrityError

from database import User, User_Info, Escuela, DB

from fastapi import HTTPException


def create_username (name: str, last_name:str):

    username_base = (name[:2] + last_name[:2].lower())
    id_random = random.randint(0,9) * 10 + random.randint(0,9)

    username = f'{username_base}{id_random}'

    while User.select().where(User.username == username).exists():

        id_random = random.randint(0,9) * 10 + random.randint(0,9)
        username = f'{username_base}{id_random}'
    
    return username

async def get_user_id(id: None, activate):

    query = User.select(User, User_Info).join(User_Info)

    # Aplicar filtro por rol si se proporciona
    if id is not None:
        query = query.where((User.id == id) & (User.activate == activate))

    # Ejecutar la consulta
    user_info_with_id = query.execute()

    # Construir la lista de usuarios con su información y rol
    user_info_list = [{
        "id": user.id,
        "name": user.user_info.name,
        "last_name": user.user_info.last_name,
        "tel": user.user_info.tel,
        "email": user.user_info.email,
        "escuela": user.user_info.escuela,
        "username": user.username,
        "password": user.password,
        "rol": user.rol  # Obtener el rol desde la relación con User
    } for user in user_info_with_id]

    return user_info_list
    
async def get_all_users_info_escuela(escuela, activate):

    query = User.select(User, User_Info).join(User_Info)

    # Aplicar filtro por rol si se proporciona
    if id is not None:
        query = query.where((User_Info.escuela == escuela) & (User.activate == activate))

    # Ejecutar la consulta
    user_info_with_id = query.execute()

    # Construir la lista de usuarios con su información y rol
    user_info_list = [{
        "id": user.id,
        "name": user.user_info.name,
        "last_name": user.user_info.last_name,
        "tel": user.user_info.tel,
        "email": user.user_info.email,
        "rol": user.rol  # Obtener el rol desde la relación con User
    } for user in user_info_with_id]

    return user_info_list

async def get_all_users_info_rol(rol, activate):
    
    user_info = User.select(User, User_Info).where((User.activate == activate) & (User.rol == rol)).join(User_Info)

    user_info_list = [{

        "id": user.id,
        "name": user.user_info.name,
        "last_name": user.user_info.last_name,
        "tel": user.user_info.tel,
        "email": user.user_info.email,
        "escuela": user.user_info.escuela,

    } for user in user_info]

    return user_info_list

async def get_all_users_info(activate):

    users_info = User.select(User, User_Info).where(User.activate == activate).join(User_Info)

    # Construir la lista de usuarios con su información y rol
    user_info_list = [{
        "id": user.id,
        "username": user.username,
        "name": user.user_info.name,
        "last_name": user.user_info.last_name,
        "tel": user.user_info.tel,
        "email": user.user_info.email,
        "escuela": user.user_info.escuela,
        "rol": user.rol
    } for user in users_info]

    return user_info_list

async def create_user(rol, password, user_request):

    if User_Info.select().where(User_Info.email == user_request.email).exists():
        raise HTTPException(status_code=400, detail="El correo electrónico ya está en uso")
    
    if not Escuela.select().where(Escuela.nombre == user_request.escuela).exists():
        raise HTTPException(status_code=400, detail="La escuela no existe")

    escuela = Escuela.get_or_none(Escuela.nombre == user_request.escuela)
    username = create_username(user_request.name, user_request.last_name)

    puesto_actual = getattr(escuela, rol)

    if puesto_actual is not None:
        raise HTTPException(status_code=400, detail=f"El puesto de {rol} ya está ocupado en esta escuela.")
    
    try:

        with DB.atomic():

            user = User.create(
                username=username,
                password=password,
                rol=rol,
                activate=True,
            )

            user_info = User_Info.create(

                user_id=user.id,
                name=user_request.name,
                last_name=user_request.last_name,
                email=user_request.email,
                tel=user_request.tel,
                escuela=user_request.escuela,
            )


            setattr(escuela, rol, user_info.id)
            escuela.save()
            
    except IntegrityError:
        raise HTTPException(status_code=500, detail="Error interno del servidor. Por favor, contacta al administrador.")

    return {"mensaje": "Usuario creado exitosamente"}

async def update_user(user_request):

    user = User.select().where((User.username == user_request.username)).first()

    if not User.select().where((User.username == user_request.username)).first():
        raise HTTPException(status_code=404, detail="Usuario inexistente o incorrecto")

    user_dic = (User.select(User, User_Info).join(User_Info).where(User.username == user_request.username).first())

    if not user_dic or not user_dic.activate:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    
    escuela = Escuela.get_or_none(Escuela.nombre==user_dic.user_info.escuela)

    if escuela is None:
        raise HTTPException(status_code=404, detail="La escuela no existe")


    if user.username == user_request.username:

        puesto_actual = getattr(escuela, user_request.rol)

        if puesto_actual:
            raise HTTPException(status_code=400, detail="Ya existe un usuario en la misma escuela con ese rol")
            
        if user_request.rol not in ["presidente", "director", "tesorero"]:
            raise HTTPException(status_code=400, detail="El rol no existe")

            
        setattr(escuela, user.rol, None)
        setattr(escuela, user_request.rol, user_dic.id)

        user.rol = user_request.rol

        user.save()
        escuela.save()

        return {"mensaje": "Datos del usuario actualizados exitosamente"}

async def update_user_info(user_request):

    user_dic = (User.select(User, User_Info).join(User_Info).where(User.id == user_request.id).first())

    if not user_dic or  user_dic.activate == False:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    
    if not Escuela.select().where(Escuela.nombre == user_request.escuela).exists():
        raise HTTPException(status_code=404, detail="La escuela no existe")

    user_info = User_Info.get_or_none((User_Info.user_id == user_request.id))
    user = User.get_or_none(User.id == user_info.user_id)

    if user_request.email == user_info.email:
        
        if user_info.escuela != user_request.escuela:

            escuela = Escuela.get_or_none(Escuela.nombre==user_info.escuela)
            
            nueva_escuela = Escuela.get_or_none(Escuela.nombre == user_request.escuela)
            puesto_actualizado = getattr(nueva_escuela, user.rol)

            if nueva_escuela is None:
                raise HTTPException(status_code=404, detail="La nueva escuela no existe")

            if puesto_actualizado:
                raise HTTPException(status_code=400, detail="Ya existe un usuario con ese rol")
            
            
            user_info.name = user_request.name
            user_info.last_name = user_request.last_name
            user_info.tel = user_request.tel
            user_info.escuela = user_request.escuela
            user_info.save()

            setattr(escuela, user.rol, None)
            escuela.save()

            setattr(nueva_escuela, user.rol, user.id)
            nueva_escuela.save()

            return {"mensaje": "Datos del usuario actualizados exitosamente"}
        
        if user_request.escuela == user_info.escuela:

            print("no")
            user_info.name = user_request.name
            user_info.last_name = user_request.last_name
            user_info.tel = user_request.tel
            user_info.save()

            return {"mensaje": "Datos del usuario actualizados exitosamente"}
        

    if user_request.email != user_info.email:

        if  User_Info.select().where(User_Info.email == user_request.email).exists():
            raise HTTPException(status_code=404, detail="El correo electronico que ingreso ya esta en uso")

        if user_info.escuela != user_request.escuela:

            escuela = Escuela.get_or_none(Escuela.nombre==user_info.escuela)
            
            nueva_escuela = Escuela.get_or_none(Escuela.nombre == user_request.escuela)
            puesto_actualizado = getattr(nueva_escuela, user.rol)

            if nueva_escuela is None:
                raise HTTPException(status_code=404, detail="La nueva escuela no existe")

            if puesto_actualizado:
                raise HTTPException(status_code=400, detail="Ya existe un usuario con ese rol")
            
            print("si2")
            user_info.name = user_request.name
            user_info.last_name = user_request.last_name
            user_info.tel = user_request.tel
            user_info.email = user_request.email
            user_info.escuela = user_request.escuela
            user_info.save()

            setattr(escuela, user.rol, None)
            escuela.save()

            setattr(nueva_escuela, user.rol, user.id)
            nueva_escuela.save()

            return {"mensaje": "Datos del usuario actualizados exitosamente"}
        
        if user_request.escuela == user_info.escuela:


            print("si")
            user_info.name = user_request.name
            user_info.last_name = user_request.last_name
            user_info.email = user_request.email
            user_info.tel = user_request.tel
            user_info.save()

            return {"mensaje": "Datos del usuario actualizados exitosamente"}
        
async def delete_user(user_id: int):

    # Verificar si el usuario existe
    user_dic = User.get_or_none(User.id == user_id)
    
    if user_dic is None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    # Cargar explícitamente la relación con User
    user_info_with_user = User.select(User, User_Info).join(User_Info).where(User.id == user_id).first()

    # Verificar si el usuario tiene una relación con la tabla User
    if user_info_with_user.user_info is not None:

        # Obtener el puesto del usuario
        puesto = user_info_with_user.rol
        
        # Obtener la escuela asociada al usuario
        escuela = Escuela.get_or_none(Escuela.nombre == user_info_with_user.user_info.escuela)
        
        if escuela is not None:

            user_dic.activate = False
            user_dic.save()

            setattr(escuela, puesto, None)
            escuela.save()

    return {"mensaje": "Usuario dado de baja exitosamente"}
