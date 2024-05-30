from pydantic import BaseModel
from typing import Optional

#Tabla Escuela

#Modelo de la tabla escuela
class EscuelaBase(BaseModel):
    id: int 
    nombre: str
    activate: bool

class EscuelaCreate(EscuelaBase):
    pass

class EscuelaUpdate(EscuelaBase):
    nombre: str


#Modelo base de la tabla DetalleEscuela y ExtraEscuela
class DetalleEscuelaBase(BaseModel):
    id: int 

    escuela_nombre: str
    clave: str
    domicilio: str
    localidad: str
    zona: str
    sector: str


#Modelo de la tabla detalle escuela
class DetalleEscuelaCreate(BaseModel):
    clave: str
    domicilio: str
    localidad: str
    zona: str
    sector: str
    telefono: str

class DetalleEscuelaUpdate(BaseModel):

    escuela_nombre: str
    clave: str
    domicilio: str
    localidad: str
    zona: str
    sector: str
    telefono: str



#Modelo base de la tabla DetalleEscuela y ExtraEscuela
class ExtraEscueBase(BaseModel):
    id: int 
    escuela_nombre: str
    NoFamilia: int
    Cuota: int
    TTAlumnos: int
    TTGrupos: int
    Turno: str


#Modelo de la tabla extra escuela
class ExtraEscueCreate(BaseModel):
    NoFamilia: int
    Cuota: int
    TTAlumnos: int
    TTGrupos: int
    Turno: str

class ExtraEscueUpdate(BaseModel):
    
    escuela_nombre: str
    NoFamilia: int
    Cuota: int
    TTAlumnos: int
    TTGrupos: int
    Turno: str


