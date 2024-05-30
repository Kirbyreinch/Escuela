from database import DB, Income

from datetime import datetime, date

from fastapi import HTTPException

from MySQLdb import IntegrityError

from peewee import fn

from Pages.validation import validate_school, validate_category, validate_user
######################################################################################

async def get_tt_amounts_with_income(school):

    query = (Income
            .select(Income.category, fn.SUM(Income.amount).alias('total_amount'))
            .where(Income.school_name == school)
            .group_by(Income.category))

    income_list = []
    # Ejecutar la consulta y obtener los resultados
    for income in query:
        income_list.append({
            "categoria": income.category.nombre,
            "total_monto": income.total_amount,
        })

    return income_list

async def get_all_incomes_with_school(school):
    
    if not Income.select().where(Income.school_name == school).exists():
        raise HTTPException(status_code=400, detail="No existen ingresos de la escuela")

    income_info = (Income.select().where(Income.school_name == school).order_by(Income.id.desc()))

    school_info_list = []
 
    for income in income_info:

        if income.category == "otros":

            school_info_list.append({
                "id": income.id,
                "escuela": income.school_name,
                "categoria": income.category.nombre,
                "especificar": income.otros_especificar,
                "date": income.date,
                "amount": income.amount,
                "user_register": income.user_register,
            })
        
        else:

            school_info_list.append({

                "id": income.id,
                "escuela": income.school_name,
                "categoria": income.category.nombre,
                "date": income.date,
                "amount": income.amount,
                "user_register": income.user_register,
            })


    
    return school_info_list

async def get_all_incomes_with_date(school, start_date, end_date):
    
    if not Income.select().where(Income.school_name == school).exists():
        raise HTTPException(status_code=400, detail="No existen ingresos de la escuela")
    
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    
    income_info = (Income.select().where((Income.school_name == school) & (Income.date >= start_date) & (Income.date <= end_date)).order_by(Income.id.desc()))

    school_info_list = []
    
    for income in income_info:

        if income.category == "otros":

            school_info_list.append({
                "id": income.id,
                "escuela": income.school_name,
                "categoria": income.category.nombre,
                "especificar": income.otros_especificar,
                "date": income.date,
                "amount": income.amount,
                "user_register": income.user_register,
            })
        
        else:

            school_info_list.append({

                "id": income.id,
                "escuela": income.school_name,
                "categoria": income.category.nombre,
                "date": income.date,
                "amount": income.amount,
                "user_register": income.user_register,
            })

    return school_info_list

async def create_income(income_request):

    await validate_school(income_request.school_name)

    if income_request.category.lower() == "otros":

        print(income_request.category.lower())
        print(income_request.otros_especificar)

        if income_request.otros_especificar == "":
            raise HTTPException(status_code=400, detail="Se requiere especificar una categoría adicional para 'Otros'")
        elif income_request.otros_especificar is None:
            raise HTTPException(status_code=400, detail="El valor de 'otros_especificar' no puede ser None cuando la categoría es 'otros'")
        
    else:

        await validate_category(income_request.category)
        income_request.otros_especificar = None


    await validate_user(income_request.user_register)

    try:

        with DB.atomic():

            income = Income.create(

                school_name=income_request.school_name,
                category=income_request.category,
                otros_especificar=income_request.otros_especificar,
                date=date.today(),
                amount=income_request.amount,
                user_register=income_request.user_register,
            )
            
    except IntegrityError:
        raise HTTPException(status_code=500, detail="Error interno del servidor. Por favor, contacta al administrador.")

    return {"mensaje": "Ingreso registrado exitosamente"}