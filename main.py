from fastapi import FastAPI, Request,Depends,HTTPException
from typing import Union,List

from sqlalchemy.orm import Session
from .database import engine,Base,Session,get_db
from .model import Item
from .schema import ItemCreate,ItemResponse

app = FastAPI()

@app.post("/items",response_model=ItemResponse)
def create_item(item:ItemCreate,db: Session= Depends(get_db)):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# get item
@app.get("/items/{item_id}",response_model=ItemResponse)
def read_item(item_id:int,db: Session= Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    return db_item


# get all item
@app.get("/items",response_model=List[ItemResponse])
def read_items(db: Session= Depends(get_db)):
    db_item = db.query(Item).all()
    return db_item


# put item
@app.put("/items/{item_id}",response_model=ItemResponse)
async def update_item(item_id:int,item:ItemCreate,db: Session= Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404,detail="Item not found")
    for key,value in item.model_dump().items():
        setattr(db_item,key,value)
    db.commit()
    db.refresh(db_item)   
    return db_item

# delete item
@app.delete("/items/{item_id}")
async def delete_item(item_id:int,db: Session= Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404,detail="Item not found")
    db.delete(db_item)   
    db.commit()
    return {"messege" : "item deleted"}