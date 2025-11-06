from pydantic import BaseModel, EmailStr, AnyUrl, computed_field
from typing import List, Dict, Optional, Annotated, Tuple
from enum import Enum

class BMICategory(str, Enum):
    UNDERWEIGHT = "Underweight"
    NORMAL = "Normal weight"
    OVERWEIGHT = "Overweight"
    OBESE = "Obese"

#defining Patient model
class Patient(BaseModel):
    name: str
    age: int
    height: float
    weight: float
    bmi: float = 0.0
    allergies: List[str]
    isMarried: Optional[bool] = None #optional field
    isFamilyMember: bool = True #default value
    email: EmailStr
    linkedIn: AnyUrl
    contact_details: Dict[str, str]
    fees: float = 500.0 #default fee


# Computed field for BMI - dynamically calculated
    @computed_field
    @property
    def calculate_bmi(self) -> float:
        bmi_value = round((self.weight / self.height**2), 2)
        return bmi_value

    @computed_field
    @property
    def bmi_status(self) -> Tuple[float, BMICategory]:
        bmi = self.calculate_bmi
        
        if bmi < 18.5:
            category = BMICategory.UNDERWEIGHT
        elif 18.5 <= bmi < 25:
            category = BMICategory.NORMAL
        elif 25 <= bmi < 30:
            category = BMICategory.OVERWEIGHT
        else:
            category = BMICategory.OBESE
            
        return (bmi, category)


#function to insert patient data
def insert_patient_data(patient: Patient):
    bmi, category = patient.bmi_status
    print(f"""
Patient Details:
---------------
Name: {patient.name}
Age: {patient.age}
Height: {patient.height}m
Weight: {patient.weight}kg
BMI: {bmi} ({category.value})
Allergies: {patient.allergies}
IsMarried: {patient.isMarried}
IsFamilyMember: {patient.isFamilyMember}
Email: {patient.email}
LinkedIn: {patient.linkedIn}
Contact Details: {patient.contact_details}
Fees: {patient.fees}
""")
    print("Patient data inserted successfully.")


#creating patient instance
patient_info = {
    'name': 'Mayank', 
    'age': 67, 
    'height': 1.75,
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