from restaurant_menu.models.database import *
from sqlalchemy import text
# import pytest


# client = [
#     Client(chat_id=743509842, name="Valentin"),
#     Client(chat_id=196569076, name="Oleg"),
#     Client(chat_id=987656842, name="Vadim"),
#     Client(chat_id=357907532, name="Sergay"),
#     Client(chat_id=987654347, name="Feofil")
# ]


# restaurant = [
#     Restaurant(name="Istanbul Han Halal")
# ]


# feedback = [
#     Feedback(author=1, feedback="Супер рестик", stars=5, restaurant_id=1),
#     Feedback(author=2, feedback="Хуйня, а не рестик", stars=1, restaurant_id=1),
#     Feedback(author=3, feedback="Норм рестик", stars=3, restaurant_id=1)
# ]


# dish = [
#     Dish(name="Шавуха", cost=149.99, type="Основное", description="Песдатая шавуха", restaurant_id=1),
#     Dish(name="Чай", cost=49.99, type="Напиток", description="Песдатый чай", restaurant_id=1),
#     Dish(name="Борщ", cost=99.50, type="Суп", description="Охуенный Истамбуловский борщец", restaurant_id=1),
#     Dish(name="Пахлава", cost=25.49, type="Десерт", description="Жопа слипнется", restaurant_id=1),
#     Dish(name="Цезарь", cost=50, type="Салат", description="Со вкусом ножа в спину", restaurant_id=1),
#     Dish(name="Плов", cost=201.99, type="Основное", description="Охапка дров и плов готов", restaurant_id=1),
#     Dish(name="Кофе", cost=9.99, type="Напиток", description="Крепкий как жопа той телки", restaurant_id=1),
#     Dish(name="Уха", cost=20.99, type="Суп", description="Супец из ухуенной рыбки", restaurant_id=1),
#     Dish(name="Мороженое", cost=27.99, type="Десерт", description="Мясо", restaurant_id=1),
#     Dish(name="Греческий", cost=15.99, type="Салат", description="Со вкусом гнета Османской Империи", restaurant_id=1)
# ]


def number_of_lines(model):
    with SessionLocal() as session:
        n = session.query(model).count()
    return n


def add_line(model):
    with SessionLocal() as session:
        for i in model:
            session.add(i)
            session.commit()


def create_restaurant(name):
    restaurant = Restaurant(
        name=name
    )
    with SessionLocal as session:
        session.add(restaurant)
        session.commit()


def create_dish(dish_name, dish_cost, dish_type, dish_description, id_restaurant):
    with SessionLocal() as session:
        dish = Dish(
            name=dish_name,
            cost=dish_cost,
            type=dish_type,
            description=dish_description,
            restaurant_id=id_restaurant
        )
        session.add(dish)
        session.commit()


def create_client(chat_id, name):
    client = Client(
        chat_id=chat_id,
        name=name
    )
    with SessionLocal as session:
        session.add(client)
        session.commit()


def create_order(id_client, id_dish, comment):
    with SessionLocal() as session:
        order = Order(
            client_id=id_client,
            comment=comment
        )
        session.add(order)
        session.commit()
        for i in id_dish:
            a = Dish_Order(
                order_id=order.id,
                dish_id=i
            )
            session.add(a)
            session.commit()


def create_feedback(id_client, feedback, stars, id_restaurant):
    with SessionLocal() as session:
        feedback = Feedback(
            author=id_client,
            feedback=feedback,
            stars=stars,
            restaurant_id=id_restaurant
        )
        session.add(feedback)
        session.commit()


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
    create_restaurant("Istanbul Han Halal")


def test_create_client():
    create_client(7634562, "Valentin")


def test_create_dish():
    create_dish("Сырники", 147.43, "Основное", "из творога", 1)


def test_create_order():
    create_order(1, [1, 7], "Шаурма без капусты")


def test_create_feedback():
    create_feedback(1, "хуйня", stars=1, id_restaurant=1)
