from sqlalchemy import Column, Integer, String, Date, TIMESTAMP
from database import Base
from sqlalchemy.orm import relationship

class Student(Base):
    
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True) #Indexing - fast lookup and retreival
    name = Column(String(50), nullable=False) # NOT NULL Constraint
    email = Column(String(50), nullable=False, unique=True) # Unique Constraint
    roll_number = Column(String(50), nullable=False, unique=True)
   