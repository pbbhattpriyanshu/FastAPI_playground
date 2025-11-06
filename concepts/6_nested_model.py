from pydantic import BaseModel

#defining Address model
class Address(BaseModel):
    HouseNo: str
    landmark: str
    city: str
    pincode: str
    state: str

#defining Patient model
class PatientInfo(BaseModel):
    name: str
    age: int
    gender: str
    address: Address

#creating address instance
address_data = {
    'HouseNo': '534 C',
    'landmark': 'Near Gamer Street Market',
    'city': 'Delhi',
    'pincode': '110096',
    'state': "Delhi"
}

#validating and creating Address object
address1 = Address(**address_data)

#creating Patient instance
patient_data = {'name': 'Pankaj', 'age': 19, 'gender': "Male", 'address': address1}

#validating and creating Patient object
patient1 = PatientInfo(**patient_data)

print(patient1)
print(patient1.name)
print(patient1.address.landmark)