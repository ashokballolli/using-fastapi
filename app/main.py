from typing import Optional

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class SubItem(BaseModel):
    lang01: str
    lang02: str

class Item(BaseModel):
    name: str
    age: int
    addr: Optional[str] = None
    lang: SubItem


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item.age > 40:
        return {"desc": "you are old already {}".format(item.age)}
    else:
        return {"desc": "you are going to be old, just {}".format(item.age)}

# Order matters

@app.get("/name/me")
def get_current_user():
    return {"logged_in_user": "fast API"}

@app.get("/user/{user_name}")
def get_user(user_name: str):
    return {"logged_in_user": user_name}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="debug", reload=True)