from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
from database import db

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, Render!"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Default to 8000 if PORT is not set
    uvicorn.run(app, host="0.0.0.0", port=port)

class AddressModel(BaseModel):
    city: str
    country: str

class StudentModel(BaseModel):
    name: str
    age: int
    address: AddressModel

class UpdateStudentModel(BaseModel):
    name: Optional[str]
    age: Optional[int]
    address: Optional[AddressModel]

@app.post("/students", status_code=201)
async def create_student(student: StudentModel):
    student_dict = jsonable_encoder(student)
    result = await db["students"].insert_one(student_dict)
    return {"id": str(result.inserted_id)}

@app.get("/students")
async def list_students(
    country: Optional[str] = Query(None),
    age: Optional[int] = Query(None)
):
    query = {}
    if country:
        query["address.country"] = country
    if age is not None:
        query["age"] = {"$gte": age}

    students = await db["students"].find(query).to_list(100)
    for student in students:
        student["id"] = str(student.pop("_id"))
    return {"data": students}

@app.get("/students/{id}")
async def fetch_student(id: str):
    student = await db["students"].find_one({"_id": ObjectId(id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student["id"] = str(student.pop("_id"))
    return student

@app.patch("/students/{id}", status_code=204)
async def update_student(id: str, updates: UpdateStudentModel):
    update_data = {k: v for k, v in updates.dict().items() if v is not None}
    if "address" in update_data:
        update_data["address"] = jsonable_encoder(update_data["address"])

    result = await db["students"].update_one(
        {"_id": ObjectId(id)},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return JSONResponse(status_code=204)

@app.delete("/students/{id}")
async def delete_student(id: str):
    result = await db["students"].delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
