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

# Predefined values

from enum import Enum
class Environments(str, Enum):
    dev = "development"
    prod = "production"

@app.get("/deploy/{env}")
def get_env_name(env: Environments):
    if env == Environments.dev:
        return {"env": Environments.dev.value, "key": "dev key"}
    elif env == Environments.prod:
        return {"env": Environments.prod.value, "key": "prod key"}
    else:
        return {"env": "should not come here"}

# Path parameters containing paths¶
@app.get("/release/{deploy_path: path}")
def deploy_app(deploy_path: str):
    return {"deploymentPath": deploy_path}

# Query Parameters
dummy_user_list = ['Ashok', 'Annu', 'Alok', 'Aditi', 'Shilpa', 'Arun']
@app.get("/userList/")
def get_user_list(skip: int, limit: int):
    return dummy_user_list[skip: skip+limit]

# Optional parameters
@app.get("/user_list/")
def getUserList(limit: int, skip: Optional[int] = 0):
    print("skip: ", skip)
    return dummy_user_list[skip : skip+limit]

# Query parameter type conversion
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="debug", reload=True)