from pydantic import BaseModel

#defining Patient model
class Patient(BaseModel):
    name: str
    age: int

#function to insert patient data
def insert_patient_data(patient: Patient):
    print(f"Inserting patient data: Name = {patient.name}, Age = {patient.age}")
    print("Patient data inserted successfully.")

#function to update patient data
def update_patient_data(patient: Patient):
    print(f"Updating patient data: Name = {patient.name}, Age = {patient.age}")
    print("Patient data updated successfully.")

#creating patient instance
patient_info = {'name': 'piyush', 'age': 21}
patient1_info = {'name': 'pankaj', 'age': 20}

#validating and creating Patient object
patient1 = Patient(**patient_info)
patient2 = Patient(**patient1_info)

#inserting patient data  
insert_patient_data(patient1)

#updating patient data
update_patient_data(patient2)
update_patient_data(Patient(name='rahul', age=22))