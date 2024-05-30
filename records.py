from datetime import datetime, date, timedelta

from dateutil.relativedelta import relativedelta

from database import User, User_Info, Escuela, Categoria, Income, Expenses, Validate_Expenses, DetalleEscuela, ExtraEscuela, Supervisor
########################################################

def all_records():
    
    record_user()

    record_school()

    record_school_tec()

    record_category()

    record_incomes()

    recdord_incomes_tec()
    
    record_info_school()
    
    record_supervisor()
    
    record_expenses()

def record_supervisor():
    
    if not Supervisor.select().where(Supervisor.name == 'Willyam').exists():
        
        new_supervisor = Supervisor.create(
            name    = "Willyam",
            estado  = "Sinaloa"
        )
        
def record_user():

    if not User.select().where(User.rol ==  'supervisor').exists():
                    
        
        new_user = User.create(
            username="damu55",
            password="123",
            rol="supervisor",
            activate=True,
        )

        new_role = User_Info.create(

            user_id = new_user.id,
            name = "dali",
            last_name = "munoz",
            tel = "3511667212",
            email = "prueba@example.com",
            escuela = "UAS",
        )   

def record_school():

    if not Escuela.select().where(Escuela.nombre ==  'UAS').exists():

        new_director = User.create(
            username="maria55",
            password="123",
            rol="director",
            activate=True,
        )

        director_role = User_Info.create(

            user_id = new_director.id,
            name = "maria",
            last_name = "cisneros",
            tel = "3511667211",
            email = "maria@example.com",
            escuela = "UAS",
        )   
        
        new_presidente = User.create(
            username="rem44",
            password="123",
            rol="presidente",
            activate=True,
        )

        presidente_role = User_Info.create(

            user_id = new_presidente.id,
            name = "rembrandt",
            last_name = "Muñoz",
            tel = "3511667210",
            email = "rem@example.com",
            escuela = "UAS",
        )   
        
        new_tesorero = User.create(
            username="leo33",
            password="123",
            rol="tesorero",
            activate=True,
        )

        tesorero_role = User_Info.create(

            user_id = new_tesorero.id,
            name = "leonardo",
            last_name = "Navarro",
            tel = "3511667214",
            email = "leo@example.com",
            escuela = "UAS",
        )   

        new_school = Escuela.create(
            
            nombre      = "UAS",
            logo        = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Logo_Uas.svg/1200px-Logo_Uas.svg.png",
            presidente  = presidente_role.id,
            director    = director_role.id,
            tesorero    = new_tesorero.id,
            activate    = True,
        )

def record_school_tec():

    if not Escuela.select().where(Escuela.nombre ==  'TEC').exists():

            new_school = Escuela.create(
            
            nombre      = "TEC",
            logo        = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Logo_Uas.svg/1200px-Logo_Uas.svg.png",
            activate    = True,
        )

def record_info_school():
    
    if not DetalleEscuela.select().where(DetalleEscuela.clave == '25DPR1821R'):
        
        new_info_school = DetalleEscuela.create(
            
            escuela_nombre = "UAS",
            clave = "25DPR1821R",
            domicilio = "Infornavit Bachomo",
            localidad = "Los Mochis, Sinaloa",
            zona = "018",
            sector = "I",
            telefono = "6881231212",
            activate    = True,
            
        )
        
        new_info_extra_school = ExtraEscuela.create(
            
            escuela_nombre = "UAS",
            no_familia  = "150",
            cuota       = "1000",
            tt_alumnos  = "190",
            tt_grupos   = "6",
            turno       = "Matutino",
            activate    = True,
            
        )
        
def record_category():

    if not Categoria.select().where((Categoria.nombre ==  'colegiaturas') & (Categoria.identificador ==  'ing')).exists():

        new_category_income = Categoria.create(

            nombre = "colegiaturas",
            identificador = "ing",
        )

        new_category_income2 = Categoria.create(

            nombre = "cuotas",
            identificador = "ing",
        )

        new_category_income3 = Categoria.create(

            nombre = "otros",
            identificador = "ing",
        )


    if not Categoria.select().where((Categoria.nombre ==  'limpieza') & (Categoria.identificador ==  'egr')).exists():

        new_category_egress = Categoria.create(

            nombre = "limpieza",
            identificador = "egr",
        )
        
        new_category_egreso2 = Categoria.create(

            nombre = "otros",
            identificador = "egr",
        )
    
def record_incomes():

    start = datetime.strptime("2024-04-13", "%Y-%m-%d").date()

    if not Income.select().where((Income.school_name == "UAS") & (Income.date == start)):

        # Fecha base
        base_date = datetime.strptime("2024-01-13", "%Y-%m-%d").date()

        # Iterar 11 veces (para sumar 0 a 10 meses)
        for i in range(12):
            # Calcular la fecha sumando i meses a la fecha base
            new_date = base_date + relativedelta(months=i)

            # Crear el registro de ingreso con la nueva fecha
            new_incomes_c = Income.create(
    
                school_name="UAS",
                category=1,
                date=new_date,
                amount=2000,
                user_register="damu55",       
            )

            new_incomes_c2 = Income.create(
    
                school_name="UAS",
                category=1,
                date=new_date,
                amount=2000,
                user_register="damu55",       
            )

            new_incomes_cu = Income.create(
    
                school_name="UAS",
                category=2,
                date=new_date,
                amount=10,
                user_register="damu55",       
            )

            new_incomes_cu2 = Income.create(
    
                school_name="UAS",
                category=2,
                date=new_date,
                amount=10,
                user_register="damu55",       
            )

        new_incomes_other = Income.create(
            
            school_name="UAS",
            category=3,
            otros_especificar="comida",
            date=new_date,
            amount=2000,
            user_register="damu55",       
        )

def recdord_incomes_tec():

    start = datetime.strptime("2024-04-13", "%Y-%m-%d").date()

    if not Income.select().where((Income.school_name == "TEC") & (Income.date == start)):

        # Fecha base
        base_date = datetime.strptime("2024-01-13", "%Y-%m-%d").date()

        # Iterar 11 veces (para sumar 0 a 10 meses)
        for i in range(12):
            # Calcular la fecha sumando i meses a la fecha base
            new_date = base_date + relativedelta(months=i)

            # Crear el registro de ingreso con la nueva fecha
            new_incomes_c = Income.create(
    
                school_name="TEC",
                category=1,
                date=new_date,
                amount=2000,
                user_register="damu55",       
            )

def record_expenses():
    
    start = datetime.strptime("2023-04-13", "%Y-%m-%d").date()
    
    if not Expenses.select().where((Expenses.escuela_nombre == "UAS") & (Expenses.fecha == start)):
        
        # Fecha base
        base_date = datetime.strptime("2023-04-13", "%Y-%m-%d").date()

        # Iterar 5 veces
        for i in range(5):
            # Calcular la fecha sumando i días a la fecha base
            new_date = base_date + timedelta(days=i)

            # Crear el registro de ingreso con la nueva fecha
            new_expenses = Expenses.create(
                
                escuela_nombre  = "UAS",
                category        = 4,
                fecha           = new_date,
                monto           = 150,
                user_register   = "Damu55",   
            )
            
            validate_expense = Validate_Expenses.create(
                id_expenses = new_expenses.id,
                presidente  = False,
                tesorero    = False,
                director    = False,
                validado    = False,
            )
        
        for i in range(2):
            
            new_date = base_date + timedelta(days=i)

            # Crear el registro de ingreso con la nueva fecha
            other_expenses = Expenses.create(
                
                escuela_nombre  = "UAS",
                category        = 5,
                fecha           = new_date,
                monto           = 10,
                user_register   = "Damu55",   
            )
            
            validate_other_expense = Validate_Expenses.create(
                id_expenses = other_expenses.id,
                presidente  = False,
                tesorero    = False,
                director    = False,
                validado    = False,
            )
