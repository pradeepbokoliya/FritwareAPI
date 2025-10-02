from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel
import json


app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data



@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get('/view')
def view():
    data = load_data()

    return data



@app.post('/patent/{patient_id}')
def view_patient(patient_id:str = Path(..., description = "Id of patient")):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found in database")



@app.get('/sort')
def sort_patients(sort_by:str = Query(..., description="short of the basis of ?"), order:str = Query('asc', description= "sort in asc and desc order") ):

    valis_fields = ['hight', 'weight', 'bmi']

    if sort_by not in valis_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valis_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail=f'Invaild order selected' )
    
    data = load_data()

    
    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data