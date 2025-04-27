from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


# Инициализация базы данных
dogs_db = {
    0: Dog(name='Bob', pk=0, kind=DogType.terrier),
    1: Dog(name='Marli', pk=1, kind=DogType.bulldog),
    2: Dog(name='Snoopy', pk=2, kind=DogType.dalmatian),
    3: Dog(name='Rex', pk=3, kind=DogType.dalmatian),
    4: Dog(name='Pongo', pk=4, kind=DogType.dalmatian),
    5: Dog(name='Tillman', pk=5, kind=DogType.bulldog),
    6: Dog(name='Uga', pk=6, kind=DogType.bulldog)
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get("/", summary="Root")
def root():
    return {"message": "Welcome to the Dog API!"}


@app.post("/post", response_model=Timestamp, summary="Get Post")
def get_post():
    if not post_db:
        raise HTTPException(status_code=404, detail="No posts available")
    return post_db[-1]


@app.get("/dog", response_model=List[Dog], summary="Get Dogs")
def get_dogs(kind: Optional[DogType] = None):
    if kind:
        return [dog for dog in dogs_db.values() if dog.kind == kind]
    return list(dogs_db.values())


@app.post("/dog", response_model=Dog, summary="Create Dog")
def create_dog(dog: Dog):
    if dog.pk in dogs_db:
        raise HTTPException(status_code=400, detail="Dog with this pk already exists")
    dogs_db[dog.pk] = dog
    return dog


@app.get("/dog/{pk}", response_model=Dog, summary="Get Dog By Pk")
def get_dog_by_pk(pk: int):
    dog = dogs_db.get(pk)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    return dog


@app.patch("/dog/{pk}", response_model=Dog, summary="Update Dog")
def update_dog(pk: int, updated_dog: Dog):
    if pk not in dogs_db:
        raise HTTPException(status_code=404, detail="Dog not found")
    dogs_db[pk] = updated_dog
    return updated_dog
