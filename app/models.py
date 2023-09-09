import uuid
from pydantic import BaseModel, Field
from typing import Optional

class Person(BaseModel):
    id: int = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    age: int = Field(...)
    gender: str = Field(...)
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Petar",
                "age": "23",
                "gender": "M"
            }
        }
    
    
class PersonUpdate(BaseModel):
    name: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Jadranka",
                "age": "46",
                "gender": "F"
            }
        }
    