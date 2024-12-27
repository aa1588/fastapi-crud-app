from pydantic import BaseModel

class StudentRequest(BaseModel):
    name: str
    email: str
    roll_number: str
    
class StudentResponse(StudentRequest):
    id: int
    
    class Config:
        orm_mode = True
        
