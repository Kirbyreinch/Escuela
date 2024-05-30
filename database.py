from peewee import *
import mysql.connector

DB = MySQLDatabase(
    'escuela',
    user = 'root',
    #password = 'dali12345',
    password = 'rem123',
    host = 'localhost',
    port = 3306
)

class Supervisor(Model):
    
    id = AutoField(primary_key=True)
    name = CharField(max_length=20)
    estado = CharField(max_length=20)

    def __str__(self):
        return self.name
    
    class Meta:
        database = DB
        table_name = 'supervisor'


class User(Model):

    id = AutoField(primary_key=True)
    username = CharField(max_length=6, unique= True)
    password = CharField(max_length=10)
    rol = CharField(constraints=[Check('rol IN (\'presidente\', \'tesorero\', \'director\', \'supervisor\')')])
    activate = BooleanField()

    def __str__(self):
        return self.name
    
    class Meta:
        database = DB
        table_name = 'users'

class User_Info(Model):

    id = AutoField(primary_key=True)
    user_id = ForeignKeyField(User, backref='user_info')
    name = CharField()
    last_name = CharField()
    tel = CharField(max_length=10)
    email = CharField()
    escuela = CharField()

    def __str__(self):
        return self.name
    
    class Meta:
        database = DB
        table_name = 'users_info'

#tabla Categoria
class Categoria(Model):
    id = AutoField()
    nombre = CharField(max_length=30, null=True)
    identificador = CharField(max_length=7, constraints=[Check('identificador IN (\'ing\', \'egr\')')])

    def __str__(self):
        return str(self.id)

    class Meta:
        database = DB
        table_name = 'categoria'

class Income(Model):
    id = AutoField()
    school_name = CharField()
    category = ForeignKeyField(Categoria, backref='incomes')
    otros_especificar = CharField(null=True)
    date = DateField()
    amount = FloatField()
    user_register = CharField(max_length=6)

    def __str__(self):
        return self.school_name

    class Meta:
        database = DB
        table_name = 'income'

def create_database(nombre_base_de_datos):

    config = {
        'user': 'root',
        #'password': 'dali12345',
        'password': 'rem123',
        'host': 'localhost',
        'port': 3306,
    }

    try:
        # Crear una conexión temporal
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Crear la base de datos si no existe
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {nombre_base_de_datos}")

        # Cerrar la conexión temporal
        cursor.close()
        connection.close()

        # Reabrir la conexión utilizando la base de datos recién creada
        config['database'] = nombre_base_de_datos
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        return connection, cursor

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None, None
    
#tabla escuela con PK Nombre
class Escuela(Model):
    id = AutoField()
    nombre= CharField(max_length=80, unique=True)
    logo = CharField(max_length=1000)
    presidente = ForeignKeyField(User_Info, null=True, to_field='id')
    director = ForeignKeyField(User_Info, null=True, to_field='id')
    tesorero = ForeignKeyField(User_Info, null=True, to_field='id')
    activate = BooleanField()
#sobreescribir el archivo str
    def __str__(self):
        return self.nombre
    
    class Meta:
        database = DB
        table_name = 'escuela'

#tabla DetalleEscuela con FK de la tabla escuela por medio del nombre
class DetalleEscuela(Model):
    id = AutoField()
    escuela_nombre = ForeignKeyField(Escuela, backref='escuela_nombre', column_name = 'escuela_nombre', to_field='nombre', on_update='CASCADE')
    clave= CharField(max_length=10, unique=True)
    domicilio= CharField(max_length=30, unique=True)
    localidad= CharField(max_length=30)
    zona= CharField(max_length=3)
    sector= CharField(max_length=1)
    telefono= CharField(max_length=14, unique=True)
    activate = BooleanField()
#sobreescribir el archivo str
    def __str__(self):
        return self.id
    
    class Meta:
        database = DB
        table_name = 'detalle_escuela'

#tabla ExtraEscuela con FK de la tabla escuela por medio del nombre
class ExtraEscuela(Model):
    id = AutoField()
    escuela_nombre = ForeignKeyField(Escuela, backref='escuela_nombre', column_name = 'escuela_nombre', to_field='nombre', on_update='CASCADE')
    no_familia= IntegerField()
    cuota= IntegerField()
    tt_alumnos= IntegerField()
    tt_grupos= IntegerField()
    turno= CharField(max_length=15)
    activate = BooleanField()
#sobreescribir el archivo str
    def __str__(self):
        return self.id
    
    class Meta:
        database = DB
        table_name = 'extra_escuela'

class Reports(Model):
    id = AutoField()
    escuela = CharField()
    fecha = DateField()
    numero_reporte = IntegerField()
    
    class Meta:
        database = DB
        table_name = 'reports'



#tabla DetalleEscuela con FK de la tabla escuela por medio del nombre
class SubCategoria(Model):
    id = AutoField()
    nombre= CharField(max_length=30, unique=True)
    identificador= CharField(max_length=7, constraints=[Check('identificador IN (\'ing\', \'egr\')')])

#sobreescribir el archivo str
    def __str__(self):
        return self.id
    
    class Meta:
        database = DB
        table_name = 'sub_categoria'

class Expenses(Model):
    id = AutoField()
    escuela_nombre = CharField()
    category = ForeignKeyField(Categoria, backref='incomes')
    fecha = DateField()
    monto = FloatField()
    user_register = CharField(max_length=6)

    def __str__(self):
        return self.escuela_nombre
    
    class Meta:
        database = DB
        table_name = 'expenses'

class Validate_Expenses(Model):
    id = AutoField()
    id_expenses = IntegerField()
    presidente = BooleanField()
    tesorero = BooleanField()
    director = BooleanField()
    validado = BooleanField()

    def __str__(self):
        return self.name
    
    class Meta:
        database = DB
        table_name = 'validate_expenses'

class Expenses_Field(Model):
    id = AutoField()
    id_expenses = IntegerField()
    archivo = CharField(max_length=1000)

    def __str__(self):
        return self.name
    
    class Meta:
        database = DB
        table_name = 'expenses_field'