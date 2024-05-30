from fastapi import FastAPI

from typing import Optional

from database import DB as connection 
from database import create_database
from database import User, User_Info, Income, Escuela, DetalleEscuela, ExtraEscuela, Categoria, SubCategoria, Supervisor, Reports, Validate_Expenses,Expenses, Expenses_Field

#region Pages

import Pages.login as p_login
import Pages.users as p_users
import Pages.categoria as p_categoria
import Pages.escuelas as p_escuelas
import Pages.income as p_income
import Pages.pdf as p_pdf
import Pages.expenses as p_expenses


#endregion

#region Record

from records import all_records

#endregion 

#region schemas

from schemas.sch_categorias import CategoriaUpdate, CategoriaCrear
from schemas.sch_users import UserInfoCreate, UserInfoUpdate, UserUpdate
from schemas.sch_income import  IncomeCreate
from schemas.sch_escuela import DetalleEscuelaCreate, DetalleEscuelaUpdate, ExtraEscueCreate, ExtraEscueUpdate
from schemas.sch_pdf import PDFCreate
from schemas.sch_escuela import DetalleEscuelaCreate, DetalleEscuelaUpdate, ExtraEscueCreate, ExtraEscueUpdate
from schemas.sch_expenses import ExpensesCreate

#endregion

app = FastAPI(title="Escuela", description="Software para el uso y administracion de una escuela", version='1.0.1')

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


create_database('escuela')

#region Inicio del servidor
@app.on_event('startup')
def startup():
        
    if connection.is_closed():
        connection.connect()

    connection.create_tables([Supervisor])
    connection.create_tables([User])
    connection.create_tables([User_Info])

    connection.create_tables([Categoria])
    connection.create_tables([Income])
    connection.create_tables([Escuela])
    connection.create_tables([DetalleEscuela])
    connection.create_tables([ExtraEscuela])
    connection.create_tables([Reports])
    connection.create_tables([SubCategoria])

    connection.create_tables([Expenses])
    connection.create_tables([Validate_Expenses])
    connection.create_tables([Expenses_Field])

    all_records()

@app.on_event('shutdown')
def shutdown():

    if not connection.is_closed():
            connection.close()  
#endregion


@app.get("/")
def read_root():
    return {"Hello": "World"}

#region Login

@app.post('/login', tags=["login"])
async def Login(user: str, password: str):
    return await p_login.login(user, password)

#endregion

#region Users

@app.get("/user/info/consulta/id/{id}", tags=["User"])
async def get_user_id(id: str, activate: Optional[bool] = True):
    return await p_users.get_user_id(id, activate)

@app.get("/users/info/consulta/escuela/{escuela}", tags=["User"])
async def get_all_users_info_escuela(escuela: str, activate: Optional[bool] = True):
    return await p_users.get_all_users_info_escuela(escuela, activate)

@app.get("/users/info/consulta/rol/{rol}", tags=["User"])
async def get_all_users_info_rol(rol: str, activate: Optional[bool] = True):
    return await p_users.get_all_users_info_rol(rol, activate)

@app.get("/users/info/consulta/", tags=["User"])
async def get_all_users_info(activate: Optional[bool] = True):
    return await p_users.get_all_users_info(activate)

@app.post('/users/create', tags=["User"])
async def create_user(rol: str, password: str, user_request: UserInfoCreate):
    return await p_users.create_user(rol, password, user_request)

@app.put("/users/update/user", tags=["User"])
async def update_user(user_request: UserUpdate):
    return await p_users.update_user(user_request)

@app.put("/users/update/user_info", tags=["User"])
async def update_user_info(user_request: UserInfoUpdate):
    return await p_users.update_user_info(user_request)

@app.delete('/users/delete', tags=["User"])
async def delete_user(user_id: str):
    return await p_users.delete_user(user_id)

#endregion

#region Categoria

@app.get('/categoria/consulta/all/ingresos', tags=["categoria"])
async def consultar_categoria_todos_ingresos():
    return await p_categoria.get_all_incomes()

@app.get('/categoria/consulta/all/egresos', tags=["categoria"])
async def consultar_categoria_todos_egresos():
    return await p_categoria.get_all_expenses()

@app.get('/categoria/consulta/ingresos', tags=["categoria"])
async def consultar_categoria_ingresos():
    return await p_categoria.consult_categoria_income()

@app.get('/categoria/consulta/egresos', tags=["categoria"])
async def consultar_categoria_egresos():
    return await p_categoria.consult_categoria_expenses()

@app.post('/categoria/crear', tags=["categoria"])
async def crear_categoria(categoria_request: CategoriaCrear):
    return await p_categoria.create_categoria(categoria_request)

@app.put('/categoria/actualizar', tags=['categoria'])
async def update_cliente(categoria_nombre, categoria_tipo,categoria_request: CategoriaUpdate):
    return await p_categoria.update_categoria(categoria_nombre, categoria_tipo, categoria_request)

#endregion

#region incomes
@app.get('/income/consulta/escuela/{escuela}', tags=["Income"])
async def get_all_incomes_with_school(school:str):
    return await p_income.get_all_incomes_with_school(school)

@app.get('/income/consulta/date/{escuela}', tags=["Income"])
async def get_all_incomes_with_date(school:str, start_date:str, end_date:str):
    return await p_income.get_all_incomes_with_date(school, start_date, end_date)

@app.post('/income/create', tags=["Income"])
async def create_income(income_request:IncomeCreate):
    return await p_income.create_income(income_request)

#endregion

#region Escuelas

@app.get('/escuela/consulta/', tags=["Escuela"])
async def get_all_schools():
    return await p_escuelas.get_all_schools()

@app.post('/escuela/create', tags=["Escuela"])
async def create_user(nombre:str, logo:str ,detalle_request: DetalleEscuelaCreate, extra_request: ExtraEscueCreate):
    return await p_escuelas.create_escuela(nombre,logo,detalle_request,extra_request )

@app.get('/escuela/consulta/{escuela}', tags=["Escuela"])
async def get_all_schools(school:str):
    return await p_escuelas.consult_escuelas(school)

@app.put("/escuela/actualizar/nombre", tags=["Escuela"])
async def update_schools(school:str,newname:str,newlogo:str):
    return await p_escuelas.update_school_base(school,newname,newlogo)

@app.put("/escuela/actualizar/localizacion", tags=["Escuela"])
async def update_schools_place(school_request: DetalleEscuelaUpdate):
    return await p_escuelas.update_school_place(school_request)

@app.put("/escuela/actualizar/alumnado", tags=["Escuela"])
async def update_schools_parents(school_request: ExtraEscueUpdate):
    return await p_escuelas.update_school_parents(school_request)

@app.delete('/escuela/delete', tags=["Escuela"])
async def delete_school(school: str):
    return await p_escuelas.delete_school(school)
#endregion

@app.get("/supervisor/consulta/id/{id}", tags=["Supervisor"])
async def get_supervisor(id: int):
    return await p_pdf.get_supervisor(id)



@app.post("/pdf/create/", tags=["Supervisor"])
async def crete_pdf(pdf_request:PDFCreate):
    return await p_pdf.create_pdf(pdf_request)


#region expenses

@app.post('/expenses/create', tags=["Expenses"])
async def create_expense(expenses_request:ExpensesCreate):
    return await p_expenses.create_expenses(expenses_request)

@app.put('/expenses/validated', tags=["Expenses"])
async def validate_expense(id_expense:int,user_register:str,user_position:str):
    return await p_expenses.validate_expenses(id_expense,user_register,user_position)

@app.post('/expenses/saveField', tags=["Expenses"])
async def save_field(id_expense: int, field:str):
    return await p_expenses.save_field(id_expense, field)

@app.get('/expenses/consultar/escuela/{escuela_nombre}', tags=["Expenses"])
async def consult_expenses_for_schoolname(escuela_nombre:str):
    return await p_expenses.consult_expenses_for_schoolname(escuela_nombre)

@app.get('/expenses/consultar/fecha/{fecha}', tags=["Expenses"])
async def consult_expenses_for_date(escuela_nombre:str,fechaInicial:str,fechaFinal:str):
    return await p_expenses.consult_expenses_for_date(escuela_nombre,fechaInicial,fechaFinal)

#endregion

#region dashboard

@app.get('/dashboard/get/incomes', tags=["Dashboard"])
async def get_all_incomes(school: str):
    return await p_income.get_tt_amounts_with_income(school)

@app.get('/dashboard/get/expenses', tags=["Dashboard"])
async def get_all_expenses():
    return await p_expenses.consult_expenses_for_schoolname()



#endregion


#python -m uvicorn main:app --reload