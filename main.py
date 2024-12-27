from fastapi import FastAPI, Depends, status, HTTPException
from schemas import StudentRequest, StudentResponse
from database import Base, engine, SessionLocal
from models import Student
from sqlalchemy.orm import Session

# create the table in the db if not created already
Base.metadata.create_all(bind=engine)

app = FastAPI()


#Db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

# CREATE Student       
@app.post("/students" , response_model=StudentResponse , status_code=status.HTTP_201_CREATED)
def create_student(student: StudentRequest, db: Session = Depends(get_db)):
    
    db_student = Student(
        name= student.name,
        email= student.email,
        roll_number= student.roll_number,
    )
    
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student
    
   
# Get all Students
@app.get("/students",  response_model=list[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students


# Get a student by its id
@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student Not found!")
    return db_student


# Delete a student
@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student Not found!")
    
    db.delete(db_student)
    db.commit()
    return {
        "msg": "Student Deleted Successfully!"
    }
    
# Update a student
@app.put("/students/{student_id}", response_model=StudentResponse )
def update_student(student_id: int, student: StudentRequest, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student Not found!")
    
    db_student.name = student.name
    db_student.email = student.email
    db_student.roll_number = student.roll_number
    db.commit()
    db.refresh(db_student)
    return db_student