from pydantic import BaseModel, EmailStr, AnyUrl, field_validator
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

    # Custom validator for email field
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):

        valid_domains = ['hdfc.com', 'icici.com']
        #abc@gmail.com
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain.')
        return value


#function to insert patient data
def insert_patient_data(patient: Patient):
    print(f"Inserting patient data: Name = {patient.name}, Age = {patient.age}, Weight = {patient.weight}, Allergies = {patient.allergies}, IsMarried = {patient.isMarried}, IsFamilyMember = {patient.isFamilyMember}, Email = {patient.email}, LinkedIn = {patient.linkedIn}, Contact Details = {patient.contact_details} , Fees = {patient.fees}")
    print("Patient data inserted successfully.")