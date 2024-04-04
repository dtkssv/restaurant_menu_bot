from restaurant_menu.models.database import *
from sqlalchemy import text
# import pytest


def number_of_lines(model):
    with SessionLocal() as session:
        n = session.query(model).count()
    return n


def add_line_list(model):
    with SessionLocal() as session:
        for i in model:
            session.add(i)
            session.commit()


def create_order(id_client, list_id_dish, comment):
    with SessionLocal() as session:
        order = Order(
            client_id=id_client,
            comment=comment
        )
        session.add(order)
        session.commit()
        order_cost = 0
        for i in list_id_dish:
            a = Dish_Order(
                order_id=order.id,
                dish_id=i
            )
            dish = session.query(Dish).filter(Dish.id == i).first()
            order_cost = order_cost + dish.cost
            session.add(a)
            session.commit()
        print(order_cost)


def clear_all_db():
    list_db_model = [Feedback, Dish_Order, Order, Client, Dish, Restaurant]
    list_str_db_model = ['Feedback', 'Client', 'Dish', 'Restaurant', 'order']
    with SessionLocal() as session:
        for i in list_db_model:
            session.query(i).delete()
        for i in list_str_db_model:
            session.execute(text(f"ALTER SEQUENCE {i}_id_seq RESTART"))
        session.commit()


def test_clear_db():
    clear_all_db()
    assert number_of_lines(Restaurant) == 0
    assert number_of_lines(Client) == 0
    assert number_of_lines(Dish) == 0
    assert number_of_lines(Feedback) == 0
    assert number_of_lines(Order) == 0
    assert number_of_lines(Dish_Order) == 0


def test_create_restaurant():
    restaurant = [
        Restaurant(name="Istanbul Han Halal")
    ]
    add_line_list(restaurant)
    assert number_of_lines(Restaurant) == 1


def test_create_client():
    client = [
        Client(chat_id=8656453, name="Valentin"),
        Client(chat_id=6543456, name="Oleg"),
        Client(chat_id=8765346, name="Vadim"),
        Client(chat_id=2345776, name="Sergay"),
        Client(chat_id=1467964, name="Feofil")
    ]
    add_line_list(client)
    assert number_of_lines(Client) == 5


def test_create_dish():
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
    add_line_list(dish)
    assert number_of_lines(Dish) == 10


def test_create_order():
    create_order(2, [1, 7, 10], "Шаурма без капусты")
    # assert number_of_lines(Order) == 1
    # assert number_of_lines(Dish_Order) == 2


def test_create_feedback():
    feedback = [
        Feedback(author=1, feedback="Супер рестик", stars=5, restaurant_id=1),
        Feedback(author=2, feedback="Хуйня, а не рестик", stars=1, restaurant_id=1),
        Feedback(author=3, feedback="Норм рестик", stars=3, restaurant_id=1)
    ]
    add_line_list(feedback)
    assert number_of_lines(Feedback) == 3
