from pydantic import BaseModel

class PDFBase(BaseModel):

    id: int
    school: str
    start_year: str
    end_year: str
    
class PDFCreate(PDFBase):
    
    pass