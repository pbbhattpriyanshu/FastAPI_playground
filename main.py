from fastapi import FastAPI
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