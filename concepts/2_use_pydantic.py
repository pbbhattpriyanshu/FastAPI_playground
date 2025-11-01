from pydantic import BaseModel

#defining Patient model
class Patient(BaseModel):
    name: str
    age: int

#function to insert patient data
def insert_patient_data(patient: Patient):
    print(f"Inserting patient data: Name = {patient.name}, Age = {patient.age}")
    print("Patient data inserted successfully.")

#creating patient instance
patient_info = {'name': 'piyush', 'age': 30}

#validating and creating Patient object
patient1 = Patient(**patient_info)

#inserting patient data  
insert_patient_data(patient1)