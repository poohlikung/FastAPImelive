from sqlalchemy import Column,Integer,String
from .database import Base,engine

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