# Patient Management System — FastAPI

A minimal learning project that implements a Patient Management System API using FastAPI. This system manages patient health records with BMI calculations and sorting capabilities.

## Table of contents
- [Quick summary](#quick-summary)
- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Local setup](#local-setup)
- [Project structure](#project-structure)
- [Advanced usage](#advanced-usage)
- [Development notes](#development-notes)

## Quick summary
REST API with these capabilities:
- View all patient records
- Retrieve individual patient data
- Sort patients by health metrics
- BMI-based health status tracking

## Features
- JSON-based data persistence
- Async request handling
- Input validation
- Sortable patient records
- Error handling with proper HTTP status codes
- Interactive API documentation

## API Endpoints

| Endpoint | Method | Description | Example |
|----------|--------|-------------|---------|
| `/` | GET | Welcome message | `curl http://127.0.0.1:8000/` |
| `/about` | GET | API information | `curl http://127.0.0.1:8000/about` |
| `/status` | GET | Application status | `curl http://127.0.0.1:8000/status` |
| `/view` | GET | List all patients | `curl http://127.0.0.1:8000/view` |
| `/patient/{id}` | GET | Get patient by ID | `curl http://127.0.0.1:8000/patient/P001` |
| `/sort` | GET | Sort patients by metric | `curl "http://127.0.0.1:8000/sort?sort_by=height&order=desc"` |

### Sorting Parameters
The `/sort` endpoint accepts:
- `sort_by`: 'height', 'weight', or 'bmi'
- `order`: 'asc' or 'desc' (default: 'asc')

## Local setup

1. Clone and navigate to project
```powershell
git clone <repository-url>
cd FastAPI_playground
```

2. Set up virtual environment
```powershell
python -m venv myenv
.\myenv\Scripts\activate
```

3. Install dependencies
```powershell
pip install fastapi uvicorn
```

4. Start server
```powershell
uvicorn main:app --reload
```

5. Access API:
- API root: http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs
- Alternative docs: http://127.0.0.1:8000/redoc

## Project structure
```
FastAPI_playground/
├── main.py           # FastAPI application
├── data.json         # Patient database
├── README.md         # Documentation
├── concepts/         # Learning concepts and examples
│   └── 1_pydantic_why.py  # Pydantic usage examples
└── myenv/           # Virtual environment
```

## Advanced usage

### Data Format
Patient records follow this structure:
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

### Sorting Examples
1. Sort by height (ascending):
```bash
curl "http://127.0.0.1:8000/sort?sort_by=height&order=asc"
```

2. Sort by BMI (descending):
```bash
curl "http://127.0.0.1:8000/sort?sort_by=bmi&order=desc"
```

## Development notes

### Error handling
The API implements proper error handling:
- 404 for patient not found
- 400 for invalid sort parameters
- Detailed error messages in response

### Future enhancements
- Add POST/PUT/DELETE operations
- Implement database storage
- Add authentication
- Add filtering capabilities
- Implement pagination

## Troubleshooting

1. Server won't start:
   - Ensure virtual environment is activated
   - Verify all dependencies are installed
   - Check port 8000 is available

2. Data not loading:
   - Verify data.json exists in root directory
   - Check file permissions
   - Ensure JSON format is valid

## License
MIT License - Feel free to use and modify

---
Last updated: November 2025
Version: 1.1.0

## Learning Concepts

### Why Pydantic?
The `concepts` folder contains examples demonstrating important FastAPI concepts:

1. Type Checking and Validation (`1_pydantic_why.py`):
```python
# Without Pydantic - Basic Python
def insert_patient_data(name: str, age: int):
    # Only type hints, no validation
    pass

# With Pydantic - Strong validation
from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    age: int

    # Automatic validation
    # Type checking
    # Better IDE support
```

### Key Benefits of Pydantic
- Automatic data validation
- Type checking at runtime
- IDE support with autocompletion
- Serialization/deserialization
- Schema generation for API docs

### Running Concept Examples
```powershell
# From project root
python concepts/1_pydantic_why.py
```

## Code Examples

### Basic Endpoint
```python
@app.get("/patient/{patient_id}")
async def get_patient(patient_id: str):
    data = load_data()
    if patient_id in data:
        return {"patient": data[patient_id]}
    raise HTTPException(status_code=404)
```

### Data Validation
```python
from pydantic import BaseModel, Field

class PatientBase(BaseModel):
    name: str = Field(..., min_length=2)
    age: int = Field(..., gt=0, lt=150)
    height: float = Field(..., gt=0)
    weight: float = Field(..., gt=0)
```

## Testing Examples

### Using curl
```bash
# Get all patients
curl http://127.0.0.1:8000/view

# Get specific patient
curl http://127.0.0.1:8000/patient/P001

# Sort patients
curl "http://127.0.0.1:8000/sort?sort_by=bmi&order=desc"
```

### Using Python requests
```python
import requests

# Get patient data
response = requests.get("http://127.0.0.1:8000/patient/P001")
print(response.json())
```

