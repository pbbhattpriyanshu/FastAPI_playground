# Packages/Dependencies
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, computed_field, Field
from typing import Annotated, Literal

# Initialize FastAPI app
app = FastAPI()

# Creating patient data model
class Patient(BaseModel):
    id: Annotated[str, Field(..., description="The ID of the patient to retrieve", examples= ["P001"])]
    name: Annotated[str, Field(..., min_length=2, max_length=50, description="The name of the patient", examples= ["John Doe", "Jane Smith"])]
    city: Annotated[str, Field(..., min_length=2, max_length=50, description="The city of the patient", examples= ["New York", "Los Angeles"])]
    age: Annotated[int, Field(..., ge=0, le=120, description="The age of the patient", examples= [25, 30])]
    gender: Annotated[str, Field(..., min_length=2, max_length=50, description="The gender of the patient", examples= ["Male", "Female"])]
    height: Annotated[float, Field(..., gt=0, le=10, description="The height of the patient", examples= [5.5, 6.0])]
    weight: Annotated[float, Field(..., gt=0, le=1000, description="The weight of the patient", examples= [150, 200])]

    @computed_field
    @property
    def bmi(self) -> float: 
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal weight"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obesity"

# Load data from JSON file
def load_data():
    with open('data.json', 'r') as file:
        data = json.load(file)
    return data

# Save data from model to JSON file
def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file)

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
async def get_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", examples= ["P001"])):
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


# Create new patient endpoint
@app.post("/create")
def create_patient(patient: Patient):
    #load data
    data = load_data()

    #check if patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    #add patient data
    data[patient.id] = patient.model_dump(exclude=['id'])
    
    #save data
    save_data(data)
    return JSONResponse(status_code=201, content={"message": "Patient added successfully"})

# Update patient data endpoint
# fixing issue