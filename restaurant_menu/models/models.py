
from sqlalchemy.orm import relationship

from .database import Base


class Restaurant(Base):
    __tablename__ = "restaurant"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    dishe = relationship("Dishe", backref="restaurant")
    feedback = relationship("Feefback", backref="restaurant")



class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    author = Column(ForeignKey("client.id"))
    feedback = Column(String(500))
    stars = Column(Integer)
    restaurant_id = Column(ForeignKey("restaurant.id"))
    client_id = Column(ForeignKey("client.id"))


class Client(Base):
    __tablename__ = "client"
    id = Column(BigInteger, primary_key=True)
    chat_id = Column(Integer, unique=True)
    name = Column(String)
    order = relationship("Dishe", backref="client")
    feedback = relationship("Feefback", backref="client")


class OrderDish(Base):
    __tablename__ = "dishe_order"
    dishe_id = Column(ForeignKey("dishe.id"))
    order_id = Column(ForeignKey("order_id"))



class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    dish = Column(String(50))
    cost = Column(Float)
    data = Column(DateTime, default=datetime.now)
    comment = Column(String(500))
    client_id = Column(ForeignKey("client.id"))
    dish_association = relationship("Dish", secondary=OrderDish, backref="Order")



class Dishe(Base):
    __tablename__ = "dishe"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    cost = Column(Float)
    type = Column(String(20))
    description = Column(String(500))
    restaurant_id = Column(ForeignKey("restaurant.id"))
