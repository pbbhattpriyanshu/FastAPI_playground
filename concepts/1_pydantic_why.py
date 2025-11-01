# In python there is no strict type checking, so the following function will not raise any error
# even if the types of the arguments do not match the expected types.

def insert_patient_data(name: str, age: int): #give only information not type error
    if type(name) == str and type(age) == int:
        if age < 0:
            raise ValueError("Age cannot be negative.")
        else:
            print(f"Inserting patient data: Name={name}, Age={age}") 
            print("Patient data inserted successfully.")
    else: 
        raise TypeError("Invalid data types. Name must be a string and Age must be an integer.")


insert_patient_data("john doe", 13)
insert_patient_data("john doe", "thirty")


def update_patient_data(name: str, age: int): #give only information not type error
    if type(name) == str and type(age) == int:
        print(f"Inserting patient data: Name={name}, Age={age}") 
        print("Patient data update successfully.")
    else: 
        raise TypeError("Invalid data types. Name must be a string and Age must be an integer.")


insert_patient_data("john doe", 13)
insert_patient_data("john doe", "thirty")

# At production level code this can lead to unexpected errors, slow code by duing repeatation of same code.

#type checking = not in python
#data validation = not in python

# To avoid such issues we use Pydantic which provides data validation and settings management using python type annotations.