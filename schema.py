from pydantic import BaseModel


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
