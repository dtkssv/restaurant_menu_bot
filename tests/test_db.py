from restaurant_menu.models.database import *
from sqlalchemy import text
import pytest


client = [
    Client(chat_id=743509842, name="Valentin"),
    Client(chat_id=196569076, name="Oleg"),
    Client(chat_id=987656842, name="Vadim"),
    Client(chat_id=357907532, name="Sergay"),
    Client(chat_id=987654347, name="Feofil")
]


restaurant = [
    Restaurant(name="Istanbul Han Halal")
]


feedback = [
    Feedback(author=1, feedback="Супер рестик", stars=5, restaurant_id=1),
    Feedback(author=2, feedback="Хуйня, а не рестик", stars=1, restaurant_id=1),
    Feedback(author=3, feedback="Норм рестик", stars=3, restaurant_id=1)
]


dish = [
    Dish(name="Шавуха", cost=149.99, type="Основное", description="Песдатая шавуха", restaurant_id=1),
    Dish(name="Чай", cost=49.99, type="Напиток", description="Песдатый чай", restaurant_id=1),
    Dish(name="Борщ", cost=99.50, type="Суп", description="Охуенный Истамбуловский борщец", restaurant_id=1),
    Dish(name="Пахлава", cost=25.49, type="Десерт", description="Жопа слипнется", restaurant_id=1),
    Dish(name="Цезарь", cost=50, type="Салат", description="Со вкусом ножа в спину", restaurant_id=1),
    Dish(name="Плов", cost=201.99, type="Основное", description="Охапка дров и плов готов", restaurant_id=1),
    Dish(name="Кофе", cost=9.99, type="Напиток", description="Крепкий как жопа той телки", restaurant_id=1),
    Dish(name="Уха", cost=20.99, type="Суп", description="Супец из ухуенной рыбки", restaurant_id=1),
    Dish(name="Мороженое", cost=27.99, type="Десерт", description="Мясо", restaurant_id=1),
    Dish(name="Греческий", cost=15.99, type="Салат", description="Со вкусом гнета Османской Империи", restaurant_id=1)
]


def add_line(a):
    with SessionLocal() as session:
        n = 0
        for i in a:
            n = n + 1
            session.add(i)
            session.commit()
    return n


def create_order(id_client, order_dish):
    with SessionLocal() as session:
        order = Order(client_id=id_client)
        session.add(order)
        session.commit()
        for i in order_dish:
            a = Dish_Order(order_id=order.id, dish_id=i)
            session.add(a)
            session.commit()


def number_of_lines(a):
    with SessionLocal() as session:
        n = session.query(a).count()
    return n


def clear_db():
    a = [Feedback, Dish_Order, Order, Client, Dish, Restaurant]
    b = ['Feedback', 'Client', 'Dish', 'Restaurant']
    with SessionLocal() as session:
        for i in a:
            session.query(i).delete()
        for i in b:
            session.execute(text(f"ALTER SEQUENCE {i}_id_seq RESTART"))
        session.commit()


def test_1():
    clear_db()
    add_line(client)
    add_line(restaurant)
    add_line(feedback)
    add_line(dish)


def test_2():
    pass
