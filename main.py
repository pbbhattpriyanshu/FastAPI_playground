from fastapi import FastAPI, Path
import json

app = FastAPI()

def load_data():
    with open('data.json', 'r') as file:
        data = json.load(file)
    return data

@app.get("/")
async def read_root():
    return {"message": "Patients Mangement System API"}

@app.get("/about")
async def read_about():
    return {"message": "A fully functional API for managing patients' data."}

@app.get("/view")
async def view_data():
    data = load_data()
    return {"data": data}

@app.get("/patient/{patient_id}")
async def get_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example= "P001")):
    # Load data from JSON file
    data = load_data()

    if patient_id in data:
        return {"patient": data[patient_id]}
    else:
        return {"error": "Patient not found"}