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
