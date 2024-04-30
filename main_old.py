# from typing import Union
# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define a Pydantic model to represent the JSON data
class ItemUpdate(BaseModel):
    name: str
    price: float
    is_offer: bool
    item_id: int


# Dummy item data
items_db = []


# Create a POST endpoint to handle the JSON data
@app.post("/items/")
def create_item(item_data: ItemUpdate):
    items_db.append(item_data.dict())
    return item_data


# Create a GET endpoint to retrieve item information by ID
@app.get("/items/{item_id}")
def read_item(item_id: int):
    # if item_id not in items_db:
    #     return {"error": "Item not found"}
    # return items_db[item_id]
    for item in items_db:
        if item['item_id'] == item_id:
                return item
    return{"message": "Item not found"}


@app.get("/items/")
def read_items():
    return items_db

@app.get("/")
def read_root():
    return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}