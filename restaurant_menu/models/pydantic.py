from pydantic import BaseModel
from datetime import datetime

class Restaurant(BaseModel):
    id: int
    name: str


class Feedback(BaseModel):
    id: int
    author: int
    feedback: str
    stars: int
    restaurant_id: int
    client_id: int


class Client(BaseModel):
    id: int
    chat_id: int
    name: str


class Order(BaseModel):
    id: int
    dish: str
    cost: float
    data: datetime
    comment: str
    client_id: int


class Dishe(BaseModel):
    id: int
    name:str
    cost: float
    type: str
    description: str
    restaurant_id: int
