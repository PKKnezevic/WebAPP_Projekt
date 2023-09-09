from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Person, PersonUpdate

router = APIRouter()

@router.post("/", response_description="Add a new person", status_code=status.HTTP_201_CREATED, response_model=Person)
def create_person(request: Request, person: Person = Body(...)):
    person = jsonable_encoder(person)
    new_person = request.app.database["PeopleCN"].insert_one(person)
    created_person = request.app.database["PeopleCN"].find_one(
        {"id": new_person.inserted_id}
    )
    
    return created_person

@router.get("/", response_description="List all people", response_model=List[Person])
def list_people(request: Request):
    people = list(request.app.database["PeopleDB"].find())
    return people

@router.get("/{id}", response_description="Get a single person by id", response_model=Person)
def find_person(id: int, request: Request):
    if (person := request.app.database["PeopleCN"].find_one({"id": id})) is not None:
        return person
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Person with ID {id} not found")

@router.put("/{id}", response_description="Update a person", response_model=Person)
def update_person(id: int, request: Request, person: PersonUpdate = Body(...)):
    person = {k: v for k, v in person.dict().items() if v is not None}
    if len(person) >= 1:
        update_result = request.app.database["PeopleCN"].update_one(
            {"id": id}, {"$set": person}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Person with ID {id} not found")

    if (
        existing_person := request.app.database["PeopleCN"].find_one({"id": id})
    ) is not None:
        return existing_person

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Person with ID {id} not found")

@router.delete("/{id}", response_description="Remove a person")
def remove_person(id: int, request: Request, response: Response):
    delete_result = request.app.database["PeopleCN"].delete_one({"id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Person with ID {id} not found")
