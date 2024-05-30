from pydantic import BaseModel

class IncomeBase(BaseModel):

    school_name: str
    category: str
    otros_especificar: str = None
    amount: float
    user_register: str

class IncomeCreate(IncomeBase):

    otros_especificar: str = None

class IncomeUpdate(BaseModel):
    school_name: str
    category: str
    date: str
    amount: str
    user_register: str
