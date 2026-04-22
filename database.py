from fastapi import FastAPI, Request,Depends
from typing import Union
from pydantic import BaseModel
# SQL Alchemy
from sqlalchemy import create_engine, Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session


# create sql engine
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)
 
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()


# ORM Class 
# ส่ง payload ว่าจะทำอะไรก็ได้เกี่ยวกับตารางนี้ ต้องกำหนดตรงนี้ออกมาก่อน
class Item(Base):
    # กำหนดตารางที่ต้องการส่ง
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Integer)

# สร้างฐานข้อมูล (การซิ้งสกีม่า)
Base.metadata.create_all(bind=engine)


app = FastAPI()

# base การทำ class ในโปรแกรมข้างใน
class ItemBase(BaseModel):
    title:str
    description:str
    price:float

# request ขาเข้า
class ItemCreate(ItemBase):
    pass

# response ขาออก
class ItemResponse(ItemBase):
    id : int
    class Config:
        from_attributes = True

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

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
