# Patient Management System — FastAPI

A minimal learning project that implements a Patient Management System API using FastAPI. This system manages patient health records with BMI calculations, sorting capabilities, and includes learning examples for Pydantic.

## Table of contents
- [Quick summary](#quick-summary)
- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Local setup](#local-setup)
- [Project structure](#project-structure)
- [Advanced usage](#advanced-usage)
- [Development notes](#development-notes)
- [Learning Concepts](#learning-concepts)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Quick summary
REST API with these capabilities:
- View all patient records
- Retrieve individual patient data
- Sort patients by health metrics
- BMI-based health status tracking
- Small concept examples showing why and how to use Pydantic

## Features
- JSON-based data persistence (data.json)
- Async request handling with FastAPI
- Input validation ideas (Pydantic examples in `concepts/`)
- Sortable patient records via query params
- Error handling with HTTP status codes
- Interactive API docs (Swagger / ReDoc)

## API Endpoints

| Endpoint | Method | Description |
|---|---:|---|
| `/` | GET | Welcome message |
| `/about` | GET | API information |
| `/status` | GET | Application status |
| `/view` | GET | List all patients (returns complete data.json) |
| `/patient/{id}` | GET | Get patient by ID (e.g. P001) |
| `/sort` | GET | Sort patients: query params `sort_by` = height|weight|bmi, `order` = asc|desc |

Examples:
- GET root: `curl http://127.0.0.1:8000/`
- GET patient: `curl http://127.0.0.1:8000/patient/P001`
- Sort by BMI desc:
  `curl "http://127.0.0.1:8000/sort?sort_by=bmi&order=desc"`

Interactive docs:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Local setup (Windows)

1. Open PowerShell in project root `d:\Concepts\FastAPI_playground`
2. Activate venv (if present):
   ```powershell
   .\myenv\Scripts\Activate.ps1
   ```
   or (CMD)
   ```bat
   myenv\Scripts\activate.bat
   ```
3. Install dependencies (if needed):
   ```powershell
   pip install fastapi uvicorn
   ```
4. Run the server (development, autoreload):
   ```powershell
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

## Project structure
```
FastAPI_playground/
├── main.py                # FastAPI application (endpoints described above)
├── data.json              # Patient database (JSON file)
├── README.md              # Project documentation (this file)
├── concepts/              # Learning examples (Pydantic demos)
│   ├── 1_pydantic_why.py  # Why Pydantic (illustration)
│   ├── 2_use_pydantic.py  # Pydantic model usage + validation examples (uses Annotated)
│   ├── 3_field_validator.py # Field-level validation examples
│   ├── 4_model_validator.py # Model-level cross-field validation
│   ├── 5_computed_fields.py # Dynamically computed fields
│   ├── 6_nested_model.py  # Nested models examples
│   └── 7_serialization.py # Data serialization and deserialization
└── myenv/                 # (Optional) virtual environment
```

## Advanced usage

### Data format
Patient records in `data.json` follow the shape:
```json
{
  "P001": {
    "name": "Aarav Sharma",
    "city": "Delhi",
    "age": 28,
    "gender": "Male",
    "height": 1.75,
    "weight": 72.0,
    "bmi": 23.5,
    "verdict": "Normal weight"
  }
}
```
Ensure keys and numeric fields are correct before running the app.

### Sorting details
- Allowed `sort_by` values: `height`, `weight`, `bmi`.
- Allowed `order` values: `asc`, `desc`.
- Returns sorted list of patient objects.

### Strict Type Validation in Pydantic

The `strict` parameter in Pydantic's Field helps prevent unwanted type coercion. This is particularly useful when you want to ensure exact type matches in your API.

#### Why Use Strict Validation?
- Prevents implicit type conversions
- Catches potential data issues early
- Ensures data integrity
- Helps maintain consistent API behavior

Example with strict validation:
```python
from pydantic import BaseModel, Field
from typing import Annotated

class PatientStrict(BaseModel):
    # Without strict=True, "72.5" (string) would be accepted and converted to float
    # With strict=True, only actual float values are accepted
    weight: Annotated[float, Field(..., gt=0, strict=True)]
    age: Annotated[int, Field(..., ge=0, le=120, strict=True)]

# This will work:
patient = PatientStrict(weight=72.5, age=25)

# These will raise ValidationError:
patient = PatientStrict(weight="72.5", age=25)  # String not allowed for weight
patient = PatientStrict(weight=72.5, age="25")  # String not allowed for age
```

#### Comparison: Strict vs Non-Strict

```python
from pydantic import BaseModel, Field

# Non-strict (default behavior)
class PatientNonStrict(BaseModel):
    weight: float = Field(gt=0)

# This works (automatic conversion):
p1 = PatientNonStrict(weight="72.5")  # Converts string to float

# Strict validation
class PatientStrict(BaseModel):
    weight: float = Field(gt=0, strict=True)

# This raises ValidationError:
p2 = PatientStrict(weight="72.5")  # Error: string not allowed
```

Real-world example from our project:
```python
class Patient(BaseModel):
    # Strict validation for numerical fields
    weight: Annotated[float, Field(..., gt=0, strict=True, 
        title='Enter the weight',
        description="Weight must be greater than zero")]
    
    age: Annotated[int, Field(..., ge=0, le=120, strict=True,
        description="Age must be between 0 and 120")]
    
    # Non-strict fields (allow reasonable coercion)
    name: Annotated[str, Field(..., min_length=2, max_length=50)]
    isMarried: Optional[bool] = None
```

#### When to Use Strict Validation

1. Financial data:
```python
class Payment(BaseModel):
    amount: Annotated[float, Field(..., gt=0, strict=True)]
    currency: str
```

2. Medical measurements:
```python
class VitalSigns(BaseModel):
    temperature: Annotated[float, Field(..., ge=35, le=42, strict=True)]
    blood_pressure: Annotated[int, Field(..., ge=70, le=190, strict=True)]
```

3. Scientific calculations:
```python
class ExperimentData(BaseModel):
    measurement: Annotated[float, Field(..., strict=True)]
    timestamp: Annotated[int, Field(..., strict=True)]
```

#### Testing Strict Validation

```python
# Run this to test strict validation:
try:
    patient = Patient(weight="70.5", age=25)  # Should fail
    print("Validation succeeded (unexpected)")
except ValidationError as e:
    print("Validation failed (expected):", e)
```

### Field Validators in Pydantic — Complex Business Logic

Field validators allow you to implement complex business rules and custom validation logic that goes beyond simple type checking and constraints.

#### Why Use Field Validators?
- Implement complex business rules
- Perform cross-field validation
- Transform input data
- Validate against external systems/databases
- Custom error messages for specific scenarios

#### Basic Field Validator Example
```python
from pydantic import BaseModel, field_validator

class Patient(BaseModel):
    email: str
    
    @field_validator('email')
    @classmethod
    def validate_company_email(cls, value: str) -> str:
        valid_domains = ['hdfc.com', 'icici.com']
        domain = value.split('@')[-1]
        
        if domain not in valid_domains:
            raise ValueError(f'Email must be from {valid_domains}')
        return value

# Usage:
patient = Patient(email="john@hdfc.com")     # Valid
patient = Patient(email="john@gmail.com")     # Raises ValidationError
```

#### Advanced Validation Examples

1. Cross-field validation:
```python
class MedicalRecord(BaseModel):
    systolic: int
    diastolic: int
    
    @field_validator('diastolic')
    @classmethod
    def validate_blood_pressure(cls, diastolic: int, info) -> int:
        systolic = info.data.get('systolic')
        if systolic and diastolic >= systolic:
            raise ValueError('Diastolic pressure must be lower than systolic')
        return diastolic
```

2. Complex date validation:
```python
from datetime import date

class Appointment(BaseModel):
    appointment_date: date
    
    @field_validator('appointment_date')
    @classmethod
    def validate_future_date(cls, v: date) -> date:
        if v <= date.today():
            raise ValueError('Appointment must be in the future')
        if v.weekday() >= 5:  # Weekend check
            raise ValueError('No appointments on weekends')
        return v
```

3. Data transformation:
```python
class PatientName(BaseModel):
    full_name: str
    
    @field_validator('full_name')
    @classmethod
    def capitalize_name(cls, v: str) -> str:
        return ' '.join(word.capitalize() for word in v.split())

# Usage:
patient = PatientName(full_name="john doe")  # Transforms to "John Doe"
```

#### Real-world Example from Our Project

From `concepts/3_field_validator.py`:
```python
class Patient(BaseModel):
    name: str
    email: EmailStr
    fees: float = 500.0  # default fee
    
    @field_validator('email')
    @classmethod
    def email_validator(cls, value: str) -> str:
        valid_domains = ['hdfc.com', 'icici.com']
        domain_name = value.split('@')[-1]
        
        if domain_name not in valid_domains:
            raise ValueError('Not a valid corporate domain.')
        return value

# Test the validator:
try:
    patient = Patient(
        name="Mayank",
        email="mayank@hdfc.com"  # Valid
    )
    print("Valid patient:", patient)
    
    patient = Patient(
        name="John",
        email="john@gmail.com"  # Will raise ValidationError
    )
except ValidationError as e:
    print("Validation failed:", e)
```

#### Best Practices for Field Validators

1. Always use `@classmethod` decorator
2. Provide clear error messages
3. Handle edge cases (None, empty strings, etc.)
4. Document the validation rules
5. Use type hints for better IDE support

```python
class Patient(BaseModel):
    age: int
    
    @field_validator('age')
    @classmethod
    def validate_adult_age(cls, v: int) -> int:
        """
        Validates that patient is an adult (18+)
        Raises ValueError if age is < 18
        """
        if v < 18:
            raise ValueError('Patient must be an adult (18+ years)')
        return v
```

To run the field validator examples:
```powershell
python concepts\3_field_validator.py
```

### Field Validator Modes in Pydantic

Field validators in Pydantic can run in two modes: 'before' and 'after'. The mode determines when the validator runs in relation to the basic parsing/validation.

#### Mode Comparison
- `mode='before'`: Runs before any parsing/validation
- `mode='after'`: Runs after basic parsing/validation (default)

#### Examples of Before vs After Validation

```python
from pydantic import BaseModel, field_validator
from typing import List

class Patient(BaseModel):
    age: int
    medications: List[str]

    # Before mode - runs before type conversion
    @field_validator('age', mode='before')
    @classmethod
    def validate_age_string(cls, value):
        if isinstance(value, str) and value.endswith('y'):
            # Convert "25y" to 25
            return int(value.rstrip('y'))
        return value

    # After mode - runs after type conversion
    @field_validator('age', mode='after')
    @classmethod
    def validate_age_range(cls, value: int) -> int:
        if value < 0 or value > 120:
            raise ValueError('Age must be between 0 and 120')
        return value

    # Before mode for list preprocessing
    @field_validator('medications', mode='before')
    @classmethod
    def lowercase_medications(cls, values):
        if isinstance(values, list):
            return [v.lower() for v in values]
        return values

# Usage examples:
try:
    # Works with both string and integer ages
    patient1 = Patient(age="25y", medications=["ASPIRIN", "INSULIN"])
    print(patient1.model_dump())  
    # Output: {'age': 25, 'medications': ['aspirin', 'insulin']}

    patient2 = Patient(age=30, medications=["PARACETAMOL"])
    print(patient2.model_dump())
    # Output: {'age': 30, 'medications': ['paracetamol']}

    # This will fail age validation
    patient3 = Patient(age=150, medications=[])
    # Raises ValueError: Age must be between 0 and 120
except ValueError as e:
    print(f"Validation error: {e}")
```

#### When to Use Each Mode

Use `mode='before'`:
- When you need to preprocess raw input data
- For string formatting/cleaning before type conversion
- To handle multiple input formats
- For data normalization

```python
class MedicalRecord(BaseModel):
    blood_pressure: str

    @field_validator('blood_pressure', mode='before')
    @classmethod
    def normalize_bp_format(cls, value):
        if isinstance(value, str):
            # Convert "120/80" or "120-80" to standard format
            return value.replace('-', '/')
        return value
```

Use `mode='after'`:
- For validation that requires the correct type
- When checking value ranges
- For business rule validation
- When working with parsed data

```python
class Prescription(BaseModel):
    dosage: float

    @field_validator('dosage', mode='after')
    @classmethod
    def validate_safe_dosage(cls, value: float) -> float:
        max_safe_dosage = 500.0
        if value > max_safe_dosage:
            raise ValueError(f'Dosage exceeds maximum safe limit of {max_safe_dosage}mg')
        return value
```

#### Real-world Example Using Both Modes

```python
from datetime import datetime
from pydantic import BaseModel, field_validator

class Appointment(BaseModel):
    date: datetime
    patient_id: str

    @field_validator('date', mode='before')
    @classmethod
    def parse_multiple_date_formats(cls, value):
        if isinstance(value, str):
            try:
                # Try multiple date formats
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
                    try:
                        return datetime.strptime(value, fmt)
                    except ValueError:
                        continue
                raise ValueError('Invalid date format')
            except Exception as e:
                raise ValueError(f'Date parsing error: {e}')
        return value

    @field_validator('date', mode='after')
    @classmethod
    def validate_future_date(cls, value: datetime) -> datetime:
        if value < datetime.now():
            raise ValueError('Appointment date must be in the future')
        return value

    @field_validator('patient_id', mode='before')
    @classmethod
    def normalize_patient_id(cls, value: str) -> str:
        # Convert "P-123" or "P123" to standard "P123" format
        return value.replace('-', '')

# Usage example:
appointment = Appointment(
    date="2024-12-25",  # Accepts various formats
    patient_id="P-123"   # Will be normalized to "P123"
)
```

#### Best Practices for Using Modes

1. Use `before` for:
   - Input normalization
   - Format standardization
   - Type conversion
   - Data cleaning

2. Use `after` for:
   - Business rules
   - Range validation
   - Relationship checks
   - Final data validation

3. Chain validators effectively:
```python
class Patient(BaseModel):
    name: str

    @field_validator('name', mode='before')
    @classmethod
    def normalize_name(cls, value: str) -> str:
        return value.strip().title()

    @field_validator('name', mode='after')
    @classmethod
    def validate_name_length(cls, value: str) -> str:
        if len(value) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return value
```

To test these examples:
```powershell
python concepts\3_field_validator.py
```

## Learning Concepts

This repository includes a `concepts/` folder with simple scripts to demonstrate Pydantic benefits:

- `1_pydantic_why.py` — shows why Python type hints alone are insufficient for runtime validation.
- `2_use_pydantic.py` — defines a Pydantic `Patient` model, validates sample data, and prints the validated instance.
- `3_field_validator.py` — demonstrates custom field-level validation and complex business logic.
- `4_model_validator.py` — demonstrates model-level validation for cross-field dependencies.
- `5_computed_fields.py` — demonstrates dynamically computed fields.
- `6_nested_model.py` — demonstrates handling complex nested structured models.
- `7_serialization.py` — demonstrates serialization and deserialization of models using JSON.

Why Pydantic (brief):
- Validates data at runtime (types, ranges, formats)
- Produces clear errors when input is invalid
- Integrates with FastAPI to auto-generate request/response schemas
- Simplifies serialization/deserialization

### Annotated Types (typing.Annotated) — brief explanation and example

What it is:
- typing.Annotated lets you attach metadata to a type. Pydantic reads this metadata (commonly Field()) to apply validation and to enrich the OpenAPI schema.
- Useful when you want to keep type + validation metadata together, and when you need rich per-field docs / examples in FastAPI.

Why use it:
- Cleaner field declarations for complex types
- Attaches title/description/examples directly to the type annotation (improves generated API docs)
- Works well with Pydantic v2 and FastAPI for clearer schemas

Example (short):

```python
from typing import Annotated
from pydantic import BaseModel, Field, EmailStr, AnyUrl

class Patient(BaseModel):
    # name is annotated with Field metadata — validation + docs
    name: Annotated[str, Field(..., min_length=2, max_length=50, title="Patient name", description="Full name (2-50 chars)", examples=["John Doe"])]
    age: int = Field(..., ge=0, le=120, description="Age in years")
    weight: float = Field(..., gt=0, description="Weight in kg")
    email: EmailStr
    linkedIn: AnyUrl
```

Usage:

```python
# Valid data -> creates Patient instance
p = Patient(
    name="Rohit Kumar",
    age=21,
    weight=70.5,
    email="rohit@example.com",
    linkedIn="https://www.linkedin.com/in/rohit"
)

# Invalid data -> raises pydantic.ValidationError (e.g., name too short or invalid email)
```

Effect in FastAPI:
- OpenAPI schema will include titles, descriptions and examples from Annotated Field metadata.
- Validation happens automatically on request bodies using the same model.

How to run the concept script:
```powershell
python concepts\2_use_pydantic.py
```
You should see the printed validated patient data; invalid inputs raise ValidationError with details.

## Model Validators

Model validators in Pydantic allow you to validate across multiple fields at once. This is essential for cross-field validation where the validity of one field depends on the value of another.

Example (from `concepts/4_model_validator.py`):

```python
from pydantic import BaseModel, model_validator

class Patient(BaseModel):
    age: int
    contact_details: dict

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Emergency contact is required for patients over 60 years old.')
        return model
```

How to run the example
```powershell
python concepts\4_model_validator.py
```

## Computed Fields

Computed fields let you dynamically compute properties of your model, which will then be included in the serialized output or when generating the JSON schema.

Example (from `concepts/5_computed_fields.py`):

```python
from pydantic import BaseModel, computed_field

class Patient(BaseModel):
    height: float
    weight: float

    @computed_field
    @property
    def bmi(self) -> float:
        return round((self.weight / self.height**2), 2)
```

How to run the example
```powershell
python concepts\5_computed_fields.py
```

## Nested Models

Nested models let you compose Pydantic models inside other models. This is useful for structured data (addresses, contacts, measurements) and keeps validation, documentation and serialization clean and reusable.

Why use nested models
- Encapsulate related fields (Address, Contact, Insurance)
- Reuse models across endpoints
- Automatic nested validation and clear OpenAPI schemas
- Easier to access/serialize nested data in code

Example (from concepts/6_nested_model.py):

```python
from pydantic import BaseModel

class Address(BaseModel):
    house_no: str
    landmark: str
    city: str
    pincode: str
    state: str

class PatientInfo(BaseModel):
    name: str
    age: int
    gender: str
    address: Address

# Create nested instances
address = Address(
    house_no="534 C",
    landmark="Near Gamer Street Market",
    city="Delhi",
    pincode="110096",
    state="Delhi"
)

patient = PatientInfo(
    name="Pankaj",
    age=19,
    gender="Male",
    address=address
)

print(patient)
# Access nested field:
print(patient.address.landmark)
```

FastAPI usage (request body example):

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Address(BaseModel):
    house_no: str
    city: str
    pincode: str

class PatientIn(BaseModel):
    name: str
    age: int
    address: Address

@app.post("/patients/")
async def create_patient(payload: PatientIn):
    # payload.address.city is already validated and available
    return {"received": payload.model_dump()}
```

Notes and tips
- OpenAPI docs will show Address as a nested schema under PatientIn.
- Validation errors clearly indicate nested field issues (e.g., address.pincode).
- You can mix nested models with lists: List[Address] for multiple addresses.
- For partial updates use optional nested fields or separate update models.

How to run the example
```powershell
python concepts\6_nested_model.py
```

## Serialization

Serialization allows you to convert Pydantic models back into dictionaries or JSON strings. You can conditionally `include` or `exclude` certain fields during serialization.

Example (from `concepts/7_serialization.py`):

```python
# Printing serialized JSON data
print(patient1.model_dump_json())

# Deserializing with include filters
# include only specific fields within nested models
temp1 = patient1.model_dump(include={'address': {'city'}})
print(temp1)
```

How to run the example
```powershell
python concepts\7_serialization.py
```

## Examples

1. Call endpoints with curl (PowerShell):
```powershell
# Get all patients
curl http://127.0.0.1:8000/view

# Get a specific patient
curl http://127.0.0.1:8000/patient/P002

# Sort patients
curl "http://127.0.0.1:8000/sort?sort_by=height&order=desc"
```

2. Using Python requests:
```python
import requests
r = requests.get("http://127.0.0.1:8000/patient/P003")
print(r.json())
```

3. Example Pydantic model (from `concepts/2_use_pydantic.py`) — brief snippet:
```python
from pydantic import BaseModel, Field, EmailStr, AnyUrl
from typing import List, Optional, Dict, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(..., min_length=2, max_length=50)]
    age: int = Field(..., ge=0, le=120)
    weight: float = Field(..., gt=0)
    allergies: List[str]
    email: EmailStr
    linkedIn: AnyUrl
    contact_details: Dict[str, str]
```

## Development notes

Planned improvements (learning path):
- Add POST / PUT / DELETE endpoints and Pydantic request models
- Move persistence to SQLite (SQLModel / SQLAlchemy)
- Add authentication (JWT/OAuth2)
- Add pagination, filtering, and tests

## Troubleshooting

- JSON decode error on startup:
  - Check `data.json` for trailing commas or invalid JSON (e.g., a trailing comma after last field will raise an error).
  - Example fix: remove trailing comma in the last object fields.
- If server cannot read `data.json`:
  - Ensure your working directory is the project root.
  - Verify file encoding is UTF-8.

- PowerShell execution policy blocks venv activation:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  .\myenv\Scripts\Activate.ps1
  ```

## License
MIT — feel free to use and modify.

---
Last updated: November 2025
Version: 1.3.0

