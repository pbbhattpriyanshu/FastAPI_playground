from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

#defining Patient model
class Patient(BaseModel):
    name: Annotated[str, Field(..., min_length=2, max_length=50, title='Name of the Patient', description='Give the name of the patient under 2 and 50 characters',  examples=['John Doe', 'Jane Smith'])]
    age: int = Field(..., ge=0, le=120, description="Age must be between 0 and 120") #age must be between 0 and 120
    weight: float = Field(..., gt=0, description="Weight must be greater than zero") #weight must be positive
    allergies: List[str]
    isMarried: Optional[bool] = None #optional field
    isFamilyMember: bool = True #default value
    email: EmailStr
    linkedIn: AnyUrl
    contact_details: Dict[str, str]
    fees: float = 500.0 #default fee

#function to insert patient data
def insert_patient_data(patient: Patient):
    print(f"Inserting patient data: Name = {patient.name}, Age = {patient.age}, Weight = {patient.weight}, Allergies = {patient.allergies}, IsMarried = {patient.isMarried}, IsFamilyMember = {patient.isFamilyMember}, Email = {patient.email}, LinkedIn = {patient.linkedIn}, Contact Details = {patient.contact_details} , Fees = {patient.fees}")
    print("Patient data inserted successfully.")

#creating patient instance
patient_info = {
    'name': 'rohit', 
    'age': 21, 
    'weight': 70.5, 
    'isMarried': False, 
    'isFamilyMember': True, 
    'allergies': ['pollen', 'nuts'], 
    'email': 'rohit@example.com', 
    'linkedIn': 'https://www.linkedin.com/in/rohit', 
    'contact_details': {'address': '542 A Mark Street Market, Near grandson Park', 'phone': '123-456-7890'},
    'fees': 1580.00}

patient_info_2 = {
    'name': 'anita',
    'age': 28,
    'weight': 62.3,
    'isMarried': True,
    'isFamilyMember': False,
    'allergies': ['dust', 'penicillin'],
    'email': 'anita28@example.com',
    'linkedIn': 'https://www.linkedin.com/in/anita28',
    'contact_details': {
        'address': '17 Green Valley Apartments, Sector 56, Gurugram',
        'phone': '987-654-3210'
    },    'fees': 2350.50
}



#validating and creating Patient object
patient1 = Patient(**patient_info)
patient2 = Patient(**patient_info_2)

#inserting patient data  
insert_patient_data(patient1)
insert_patient_data(patient2)

#updating patient data
# update_patient_data(Patient(name='rahul', age=22))