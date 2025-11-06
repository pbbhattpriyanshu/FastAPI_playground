from pydantic import BaseModel, EmailStr, AnyUrl, model_validator
from typing import List, Dict, Optional, Annotated

#defining Patient model
class Patient(BaseModel):
    name: str
    age: int
    weight: float
    allergies: List[str]
    isMarried: Optional[bool] = None #optional field
    isFamilyMember: bool = True #default value
    email: EmailStr
    linkedIn: AnyUrl
    contact_details: Dict[str, str]
    fees: float = 500.0 #default fee

# Custom validator for entire model
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Emergency contact is required for patients over 60 years old.')
        else:
            print('Model validation passed.')
            return model

#function to insert patient data
def insert_patient_data(patient: Patient):
    print(f"Inserting patient data: Name = {patient.name}, Age = {patient.age}, Weight = {patient.weight}, Allergies = {patient.allergies}, IsMarried = {patient.isMarried}, IsFamilyMember = {patient.isFamilyMember}, Email = {patient.email}, LinkedIn = {patient.linkedIn}, Contact Details = {patient.contact_details} , Fees = {patient.fees}")
    print("Patient data inserted successfully.")


#creating patient instance
patient_info = {
    'name': 'Mayank', 
    'age': 67, 
    'weight': 90.5, 
    'isMarried': False, 
    'isFamilyMember': True, 
    'allergies': ['pollen', 'nuts', 'chicken pox'], 
    'email': 'mayank@hdfc.com', 
    'linkedIn': 'https://www.linkedin.com/in/mayank', 
    'contact_details': {'address': '542 A Mark Street Market, Near grandson Park', 'phone': '123-456-7890', 'emergency': '453-753-2677'},
    'fees': 4580.00}



#validating and creating Patient object
patient1 = Patient(**patient_info)   #validation -> typecasting


#inserting patient data  
insert_patient_data(patient1)