from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional

import json

app = FastAPI()

class Person(BaseModel):
    id: Optional[int] = None
    name: str
    age: int
    gender: str
    
    
with open('people.json', 'r') as f:
    people = json.load(f)['people']

@app.get('/person/{p_id}')
def get_person(p_id: int):
    person = [p for p in people if p['id'] == p_id]
    return person[0] if len(person) > 0 else {}


@app.get("/search", status_code=200)
def search_person(age: Optional[int] = Query(None, title="Age", description="Age filter"),
                name: Optional[str] = Query(None, title="Name", description="Name filter")):
    
    persons1 = [p for p in people if p['age'] == age]
    
    if name is None:
        if age is None:
            return people
        else:
            return persons1
    else:
        persons2 = [p for p in people if name.lower() in p['name'].lower()]
        if age is None:
            return persons2
        else:
            combined = [p for p in persons1 if p in persons2]
            return combined
