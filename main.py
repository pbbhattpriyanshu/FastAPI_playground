from fastapi import FastAPI, Path, HTTPException, Query
import json
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Creating patient data model
class Patient(BaseModel):
    id: str
    name: str
    city: str
    age: int
    gender: str
    height: float
    weight: float

# Load data from JSON file
def load_data():
    with open('data.json', 'r') as file:
        data = json.load(file)
    return data

# Define API endpoints
@app.get("/")
async def read_root():
    return {"message": "Patients Mangement System API"}

# About endpoint
@app.get("/about")
async def read_about():
    return {"message": "A fully functional API for managing patients' data."}

# Status endpoint
@app.get("/status")
async def read_status():
    return {"message": "There is no such booking, regarding this application"}

# View data endpoint
@app.get("/view")
async def view_data():
    data = load_data()
    return {"data": data}

# Get patient by ID endpoint
@app.get("/patient/{patient_id}")
async def get_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example= "P001")):
    # Load data from JSON file
    data = load_data()

    if patient_id in data:
        return {"patient": data[patient_id]}
    else:
        raise HTTPException(status_code=404, detail="Patient not found")

# Sort patients endpoint
@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="The field to sort patients on the basis of height, weight or bmi"), order: str = Query("asc", description="The order of sorting: asc for ascending, desc for descending")):
    valid_sort_fields = {"height", "weight", "bmi"}

    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Choose from {valid_sort_fields}")
    
    if order not in {"asc", "desc"}:
        raise HTTPException(status_code=400, detail="Invalid order. Choose 'asc' or 'desc'")
    
    data = load_data()
    
    reverse = True if order == "desc" else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=reverse)

    return {"sorted_data": sorted_data}

#