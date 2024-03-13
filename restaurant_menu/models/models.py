# from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, BigInteger, SmallInteger
# from datetime import datetime
# from sqlalchemy.orm import relationship
#
# from database import *
#
#
# class Restaurant(Base):
#     __tablename__ = "restaurant"
#
#     id = Column(SmallInteger, primary_key=True)  # Используются маленькие значения
#     name = Column(String(50), unique=True)
#
#
# class Feedback(Base):
#     __tablename__ = "feedback"
#
#     id = Column(Integer, primary_key=True)
#     author = Column(ForeignKey("client.id"))
#     feedback = Column(String(500))
#     stars = Column(Integer)
#     restaurant_id = Column(ForeignKey("restaurant.id"))
#     client_id = Column(ForeignKey("client.id"))
#
#
# class Client(Base):
#     __tablename__ = "client"
#
#     id = Column(BigInteger, primary_key=True)  # исользуются большие значения
#     chat_id = Column(Integer, unique=True)
#     name = Column(String)
#
#
# class Order(Base):
#     __tablename__ = "order"
#
#     id = Column(Integer, primary_key=True)
#     dish = Column(String(50))
#     cost = Column(Float)
#     data = Column(DateTime, default=datetime.now)
#     comment = Column(String(500))
#     client_id = Column(ForeignKey("client.id"))
# # Отношение many to many через association table
#     dish_replied = relationship("Dishe", back_populates="order_replied", secondary="DisheOrder")
#
#
# class Dishe(Base):
#     __tablename__ = "dishe"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50))
#     cost = Column(Float)
#     type = Column(String(20))
#     description = Column(String(500))
#     restaurant_id = Column(ForeignKey("restaurant.id"))
# # Отношение many to many через association table
#     order_replied = relationship("Order", back_populates="dish_replied", secondary="DisheOrder")
#
#
# # association table
# class DisheOrder(Base):
#     __tablename__ = "dishe_order"
#
#     dishe_id = Column(ForeignKey("dishe.id"), primary_key=True)
#     order_id = Column(ForeignKey("order_id"), primary_key=True)
