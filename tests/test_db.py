from restaurant_menu.models.database import *


client = [
    Client(chat_id=743509842, name="Valentin"),
    Client(chat_id=743509842, name="Oleg"),
    Client(chat_id=743509842, name="Vadim"),
    Client(chat_id=743509842, name="Sergay"),
    Client(chat_id=743509842, name="Feofil")
          ]


restaurant = [
    Restaurant(name="Istanbul Han Halal")
]


feedback = [
    Feedback(author=1, feedback="Супер рестик", stars=5, restaurant_id=1),
    Feedback(author=3, feedback="Хуйня, а не рестик", stars=1, restaurant_id=1),
    Feedback(author=5, feedback="Норм рестик", stars=3, restaurant_id=1)
]


dish = [
    Dishe(name="Шавуха", cost=149.99, type="Основное", description="Песдатая шавуха", restaurant_id=1),
    Dishe(name="Чай", cost=49.99, type="Напиток", description="Песдатый чай", restaurant_id=1),
    Dishe(name="Борщ", cost=99.50, type="Суп", description="Охуенный Истамбуловский борщец", restaurant_id=1),
    Dishe(name="Пахлава", cost=25.49, type="Десерт", description="Жопа слипнется", restaurant_id=1),
    Dishe(name="Цезарь", cost=50, type="Салат", description="Со вкусом ножа в спину", restaurant_id=1),
    Dishe(name="Плов", cost=201.99, type="Основное", description="Охапка дров и плов готов", restaurant_id=1),
    Dishe(name="Кофе", cost=9.99, type="Напиток", description="Крепкий как жопа той телки", restaurant_id=1),
    Dishe(name="Уха", cost=20.99, type="Суп", description="Супец из ухуенной рыбки", restaurant_id=1),
    Dishe(name="Мороженое", cost=27.99, type="Десерт", description="Мясо", restaurant_id=1),
    Dishe(name="Греческий", cost=15.99, type="Салат", description="Со вкусом гнета Османской Империи", restaurant_id=1)
]


order = [

]
class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    dish = Column(String(50))
    cost = Column(Float)
    data = Column(DateTime, default=datetime.now)
    comment = Column(String(500))
    client_id = Column(ForeignKey("client.id"))
    dish_replied = relationship("Dishe", secondary=DisheOrder)

with SessionLocal() as session:
   session.query()