from pydantic import BaseModel

class ExpensesBase(BaseModel):

    escuela_nombre: str
    
    category: str
    monto: float
    user_register: str

class ExpensesCreate(ExpensesBase):

    pass

class ExpensesUpdate(BaseModel):
    escuela_nombre: str
    category: str
    fecha: float
    monto: str
    user_register: str