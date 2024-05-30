from database import DB, Expenses, Validate_Expenses, Expenses_Field

from datetime import date

from fastapi import HTTPException

from MySQLdb import IntegrityError

from Pages.validation import validate_school, validate_category, validate_user

from peewee import Join, JOIN

async def create_expenses(expenses_request):

    await validate_school(expenses_request.escuela_nombre)
    await validate_category(expenses_request.category)
    await validate_user(expenses_request.user_register)

    try:

        with DB.atomic():

            expense = Expenses.create(

                escuela_nombre=expenses_request.escuela_nombre,
                category=expenses_request.category,
                fecha=date.today(),
                monto=expenses_request.monto,
                user_register=expenses_request.user_register,
            )
            validate_expense = Validate_Expenses.create(
                id_expenses=expense.id,
                presidente=False,
                tesorero=False,
                director=False,
                validado=False,
            )
            
    except IntegrityError:
        raise HTTPException(status_code=500, detail="Error interno del servidor. Por favor, contacta al administrador.")

    return {"mensaje": "Egreso registrado exitosamente"}

async def validate_expenses(id_expense,user_register,user_position):

    if not Expenses.select().where(Expenses.id == id_expense).exists():
        raise HTTPException(status_code=400, detail="El egreso no existe")
    
    await validate_user(user_register)

    try:
        query = Validate_Expenses.select().where(Validate_Expenses.id_expenses == id_expense).first()

        if query.validado:
            raise HTTPException(status_code=400, detail="El egreso ya se encuentra validado")

        if user_position == "presidente":
            Validate_Expenses.update(presidente=True).where(Validate_Expenses.id_expenses == id_expense).execute()
        elif user_position == "tesorero":
            Validate_Expenses.update(tesorero=True).where(Validate_Expenses.id_expenses == id_expense).execute()
        elif user_position == "director":
            Validate_Expenses.update(director=True).where(Validate_Expenses.id_expenses == id_expense).execute()

        query = Validate_Expenses.select().where(Validate_Expenses.id_expenses == id_expense).first()

        if query.presidente==True and query.tesorero==True and query.director==True:
            Validate_Expenses.update(validado=True).where(Validate_Expenses.id_expenses == id_expense).execute()

    except IntegrityError:
        raise HTTPException(status_code=500, detail="Error interno del servidor. Por favor, contacta al administrador.")

    return {"mensaje": "Egreso validado exitosamente"}


async def save_field(id_expense, field):

    if not Expenses.select().where(Expenses.id == id_expense).exists():
        raise HTTPException(status_code=400, detail="El egreso no existe")
    
    if Expenses_Field.select().where((Expenses_Field.id_expenses == id_expense) &(Expenses_Field.archivo==field)).exists():
        raise HTTPException(status_code=400, detail="El Documento ya existe")

    field_request = Expenses_Field.create(
        id_expenses = id_expense,
        archivo= field
    )
    return {"mensaje": "Documento guardado exitosamente"}


async def consult_expenses_for_schoolname(escuela_nombre):
    
    if not Expenses.select().where(Expenses.escuela_nombre == escuela_nombre).exists():
        raise HTTPException(status_code=400, detail="No existen egresos de la escuela.")
    
    expenses_dict  = []
    try:
        query=Expenses.select(Expenses.id,
                        Expenses.category,
                        Expenses.fecha,
                        Expenses.monto,
                        Expenses.user_register,
                        Validate_Expenses.presidente,
                        Validate_Expenses.tesorero,
                        Validate_Expenses.director,
                        Validate_Expenses.validado).join(Validate_Expenses, on=(Expenses.id == Validate_Expenses.id_expenses)).where(Expenses.escuela_nombre == escuela_nombre)

        for expense in query:
            archivo = Expenses_Field.select().where(Expenses_Field.id_expenses == expense.id).first()
            expen_dict = {
                "id": expense.id,
                "escuela_nombre": escuela_nombre,
                "category": expense.category,
                "fecha": expense.fecha,
                "monto": expense.monto,
                "user_register": expense.user_register,
                "archivo": archivo.archivo,
                "presidente": expense.validate_expenses.presidente,
                "tesorero": expense.validate_expenses.tesorero,
                "director": expense.validate_expenses.director,
                "validado": expense.validate_expenses.validado,
            }
            expenses_dict.append(expen_dict)

    except IntegrityError:
        raise HTTPException(status_code=500, detail="Error interno del servidor. Por favor, contacta al administrador.")
    return expenses_dict

async def consult_expenses_for_date(escuela_nombre, fechaInicio, fechaFinal):
    
    if not Expenses.select().where(Expenses.escuela_nombre == escuela_nombre).exists():
        raise HTTPException(status_code=400, detail="No existen egresos de la escuela.")
    
    if not Expenses.select().where((Expenses.escuela_nombre == escuela_nombre) & (Expenses.fecha >= fechaInicio) &(Expenses.fecha <= fechaFinal)).exists():
        raise HTTPException(status_code=400, detail="No existen egresos en la fecha.")
    
    expenses_dict  = []
    try:
        
        query=Expenses.select(Expenses.id,
                        Expenses.category,
                        Expenses.fecha,
                        Expenses.monto,
                        Expenses.user_register,
                        Validate_Expenses.presidente,
                        Validate_Expenses.tesorero,
                        Validate_Expenses.director,
                        Validate_Expenses.validado).join(Validate_Expenses, on=(Expenses.id == Validate_Expenses.id_expenses)).where((Expenses.escuela_nombre == escuela_nombre) & (Expenses.fecha >= fechaInicio) &(Expenses.fecha <= fechaFinal))

        for expense in query:
            archivo = Expenses_Field.select().where(Expenses_Field.id_expenses == expense.id).first()
            expen_dict = {
                "id": expense.id,
                "escuela_nombre": escuela_nombre,
                "category": expense.category,
                "fecha": expense.fecha,
                "monto": expense.monto,
                "user_register": expense.user_register,
                "archivo": archivo.archivo,
                "presidente": expense.validate_expenses.presidente,
                "tesorero": expense.validate_expenses.tesorero,
                "director": expense.validate_expenses.director,
                "validado": expense.validate_expenses.validado,
            }
            expenses_dict.append(expen_dict)

    except IntegrityError:
        raise HTTPException(status_code=500, detail="Error interno del servidor. Por favor, contacta al administrador.")
    return expenses_dict