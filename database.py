from fastapi import FastAPI, Request
from typing import Union
from pydantic import BaseModel
# SQL Alchemy
from sqlalchemy import create_engine, Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker




# create sql engine
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)
 
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()


# ORM Class
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Integer)

# สร้างฐานข้อมูล
Base.metadata.create_all(bind=engine)


app = FastAPI()

# base
class Item(BaseModel):
    title:str
    description:str
    price:float

class ItemCreate(Item):
    pass