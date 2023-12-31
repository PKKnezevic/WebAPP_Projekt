from fastapi import FastAPI
from dotenv import dotenv_values

from pymongo import MongoClient

from database import router as router

config = dotenv_values(".env")

app = FastAPI()
    
@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")
    
@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close() 
    
app.include_router(router, tags=["People"], prefix="/person")

### LOCAL DATABASE ###    
#with open('people.json', 'r') as f:
#    people = json.load(f)

#@app.get('/person/{p_id}')
#def get_person(p_id: int):  
#    person = [p for p in people if p['id'] == p_id]
#    return person[0] if len(person) > 0 else {}


#@app.get("/search", status_code=200)
#def search_person(age: Optional[int] = Query(None, title="Age", description="Age filter"),
#                name: Optional[str] = Query(None, title="Name", description="Name filter")):
#    
#    persons1 = [p for p in people if p['age'] == age]
#    
#    if name is None:
#        if age is None:
#            return people
#        else:
#            return persons1
#    else:
#        persons2 = [p for p in people if name.lower() in p['name'].lower()]
#        if age is None:
#            return persons2
#        else:
#            combined = [p for p in persons1 if p in persons2]
#            return combined
   
#@app.post("/login")
#async def login(form: OAuth2PasswordRequestForm = Depends()):
#    return await security.login(form.username, form.password)
    
#@app.post('/addPerson', status_code=201)        
#def add_person(person: Person):
#    p_id = max([p['id'] for p in people]) + 1 
#    new_person = {
#        "id": p_id,
#        "name": person.name,
#        "age": person.age,
#        "gender": person.gender
#    }
    
#    people.append(new_person)
    
#    with open('people.json', 'w') as f:
#        json.dump(people, f)
        
#    return new_person

#@app.put('/changePerson', status_code=204)
#def change_person(person: Person):
#    new_person = {
#        "id": person.id,
#        "name": person.name,
#        "age": person.age,
#        "gender": person.gender
#    }
#    person_list = [p for p in people if p['id'] == person.id]
#    if len(person_list) > 0:
#        people.remove(person_list[0])
#        people.append(new_person)
#        with open('people.json', 'w') as f:
#            json.dump(people, f)
#        return new_person
#    else:
#        return HTTPException(status_code=404, detail=f"Person with id {person.id} not found")
    
#@app.delete('/deletePerson/{p_id}')    
#def delete_person(p_id: int):
#    person = [p for p in people if p['id'] == p_id]
#    if len(person) > 0:
#        people.remove(person[0])
#        with open('people.json', 'w') as f:
#            json.dump(people, f)
#    else:
#        raise HTTPException(status_code=404, detail=f"Person with id {p_id} not found")