from fastapi import FastAPI, Request
from typing import Union
from pydantic import BaseModel




app = FastAPI()


#part hello
@app.get("/hello")
def hello_world():
    return {"message" : "hello world hee"}

# Union query String
@app.get("/items/{item_id}")
def read_item(item_id: int,q: Union[str,None] = None):
    return {"item_id": item_id,"q":q}


# Post # Async
# ส่งอะไรมาก็ได้
'''
@app.post("/items")
async def create_item(request : Request):
    body = await request.json()
    # debug
    print(f'username : {body["name"]}')
    return {"body" : body}
'''


# Pydantic
# ต้องใช้ท่านี้เสมอในการpost
# type checking 
# มี docs สอนถ้าใช้ท่านี้
class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
def create_item(item : Item):
    print(item.name)
    return {"body" : item}

# put แก้ไข
@app.put("/items/{item_id}")
def edit_item(item_id:int,item: Item):
    return{"id":item_id,"request body": item}