from pydantic import BaseModel
from typing import Optional


#Tabla Categoria y SubCategoria
class CategoriaBase(BaseModel):
    id: int
    nombre: str
    identificador: str

class CategoriaCrear(CategoriaBase):

    pass

class CategoriaUpdate(CategoriaBase):

    nombre: str
    identificador: str 


