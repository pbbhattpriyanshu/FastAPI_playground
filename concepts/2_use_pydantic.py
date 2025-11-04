from pydantic import BaseModel
from typing import List, Dict, Optional

#defining Patient model
class Patient(BaseModel):
    name: str
    age: int
    weight: float
    isMarried: Optional[bool] = None #optional field
    allergies: List[str]
    contact_details: Dict[str, str]
    fees: float = 500.0 #default fee

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

patient1_info = {'name': 'mohit', 'age': 26, 'weight': 90.5, 'allergies': ['pollen', 'rabbies'], 'contact_details': {'email': 'mohit@example.com', 'phone': '723-895-7880'}, 'fees': 5580.00}

#validating and creating Patient object
patient1 = Patient(**patient_info)
patient2 = Patient(**patient1_info)

#inserting patient data  
insert_patient_data(patient1)
insert_patient_data(patient2)

#updating patient data
# update_patient_data(Patient(name='rahul', age=22))