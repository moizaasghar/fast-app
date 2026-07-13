from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

class Student(BaseModel):
    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=0)
    email: EmailStr

class updateStudentAge(BaseModel):
    id: int = Field(..., gt=0)
    age: int = Field(..., ge=0)

class DeleteStudent(BaseModel):
    id: int = Field(..., gt=0)

app = FastAPI()


# list of Students

students = [
    Student(id=1, name="John Doe", age=20, email="john@example.com"),
    Student(id=2, name="Jane Smith", age=22, email="jane@example.com"),
    Student(id=3, name="Alice Johnson", age=21, email="alice@example.com"),
]

@app.get("/")
async def home():
    return {"message": "Welcome to the Student Services Application!"} # Key/Value


@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/students")
async def get_students():
    return {"students": students}

# Path Parameters

@app.get("/getStudentsViaId/{student_id}")
async def get_student(student_id: int):
    student = next((s for s in students if s.id == student_id), None)
    if student:
        return {"student": student}
    return {"error": "Student not found"}, 404

@app.get("/getStudentsViaIdAndEmail/{student_id}/{email}")
async def get_student(student_id: int, email: str):
    student = next((s for s in students if s.id == student_id and s.email == email), None)
    if student:
        return {"student": student}
    return {"error": "Student not found"}, 404

# Query Parameters
@app.get("/getStudentsViaQuery")
async def get_students_via_query(student_id: int = None, email: str = None):
    if student_id is not None and email is not None:
        student = next((s for s in students if s.id == student_id and s.email == email), None)
        if student:
            return {"student": student}
    elif student_id is not None:
        student = next((s for s in students if s.id == student_id), None)
        if student:
            return {"student": student}
    elif email is not None:
        student = next((s for s in students if s.email == email), None)
        if student:
            return {"student": student}
    return {"error": "Student not found"}, 404

@app.post("/addStudent", response_model=Student)
async def add_student(student: Student):
    students.append(student)
    return student

@app.put("/updateStudent/{student_id}", response_model=Student)
async def update_student(student_id: int, updated_student: Student):
    for index, student in enumerate(students):
        if student.id == student_id:
            students[index] = updated_student
            return updated_student
    return {"error": "Student not found"}, 404


@app.patch("/updateStudentAge/{student_id}", response_model=Student)
async def update_student_age(student_id: int, updated_age: updateStudentAge):
    for index, student in enumerate(students):
        if student.id == student_id:
            students[index].age = updated_age.age
            return students[index]
    return {"error": "Student not found"}, 404

@app.patch("/updateStudentAgeViaQuery", response_model=Student)
async def update_student_age_via_query(updated_age: updateStudentAge):
    for index, student in enumerate(students):
        if student.id == updated_age.id:
            students[index].age = updated_age.age
            return students[index]
    return {"error": "Student not found"}, 404
        
@app.delete("/deleteStudent/{student_id}")
async def delete_student(student_id: int):
    for index, student in enumerate(students):
        if student.id == student_id:
            deleted_student = students.pop(index)
            return {"message": "Student deleted successfully", "student": deleted_student}
    return {"error": "Student not found"}, 404

@app.delete("/deleteStudentViaQuery")
async def delete_student_via_query(student: DeleteStudent):
    for index, s in enumerate(students):
        if s.id == student.id:
            deleted_student = students.pop(index)
            return {"message": "Student deleted successfully", "student": deleted_student}
    return {"error": "Student not found"}, 404

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)