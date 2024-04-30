from fastapi import FastAPI
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


client = MongoClient('mongodb://localhost:27017/')
db = client['test']
collection = db['db_test']


class EmployeeQueryParams(BaseModel):
    emp_id: int

class EmployeeResponse(BaseModel):
    emp_id: int
    emp_name: str
    entry_time: int
    leave_time: int



# for a particular employee -----
@app.get("/get_employee/{emp_id}")
async def get_employee(emp_id: int):
    result = collection.find_one({"emp_id": emp_id})
    if result:
        # Convert ObjectId to string
        result["_id"] = str(result["_id"])
        employee_data = EmployeeResponse(**result)
        return employee_data
    else:
        return {"error": "Employee not found"}
    


# to get all the value -------- roles --- admin
@app.get("/check_values/admin")
async def check_all_values():
    all_documents = list(collection.find({}))  # Fetch all documents from the collection
    for doc in all_documents:
        # Convert ObjectId to string in each document
        doc["_id"] = str(doc["_id"])
    return all_documents


# for vc ----
@app.get("/check_values/vc")
async def check_selected_values():
    emp_range_documents = list(collection.find({"emp_id": {"$gte": 100, "$lte": 104}}))
    for doc in emp_range_documents:
        # Convert ObjectId to string in each document
        doc["_id"] = str(doc["_id"])
    return emp_range_documents

# for hod -----
@app.get("/check_values/hod")
async def check_selected_values():
    emp_range_documents = list(collection.find({"emp_id": {"$gte": 104, "$lte": 109}}))
    for doc in emp_range_documents:
        # Convert ObjectId to string in each document
        doc["_id"] = str(doc["_id"])
    return emp_range_documents






if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)



