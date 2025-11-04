from pydantic import BaseModel
from typing import List, Dict

#defining Patient model
class Patient(BaseModel):
    name: str
    age: int
    weight: float
    isMarried: bool = False
    allergies: list[str]
    contact_details: Dict[str, str]
    fees: float = 500.0

#function to insert patient data
def insert_patient_data(patient: Patient):
    print(f"Inserting patient data: Name = {patient.name}, Age = {patient.age}, Weight = {patient.weight}, IsMarried = {patient.isMarried}, Allergies = {patient.allergies}, Contact Details = {patient.contact_details} , Fees = {patient.fees}")
    print("Patient data inserted successfully.")

#function to update patient data
def update_patient_data(patient: Patient):
    print(f"Updating patient data: Name = {patient.name}, Age = {patient.age}")
    print("Patient data updated successfully.")

#creating patient instance
patient_info = {'name': 'rohit', 'age': 21, 'weight': 70.5, 'isMarried': False, 'allergies': ['pollen', 'nuts'], 'contact_details': {'email': 'rohit@example.com', 'phone': '123-456-7890'}, 'fees': 1580.00}

#validating and creating Patient object
patient1 = Patient(**patient_info)

#inserting patient data  
insert_patient_data(patient1)

#updating patient data
# update_patient_data(Patient(name='rahul', age=22))