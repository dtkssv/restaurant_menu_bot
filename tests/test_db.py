import pytest

from pytest_lazyfixture import lazy_fixture
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from .conftest import session_factory
from restaurant_menu.models.database import (
    Client, Dish, Feedback, Order, Restaurant)


@pytest.mark.usefixtures("prepare_db_creating")
class TestDbCreating:
    @pytest.mark.parametrize(
        "model, objects_list, model_attr",
        (
            (Restaurant, lazy_fixture("restaurants"), "name"),
            (Client, lazy_fixture("clients"), "name"),
            (Feedback, lazy_fixture("feedbacks"), "feedback"),
            (Dish, lazy_fixture("dishes"), "name"),
            (Order, lazy_fixture("orders"), "comment"),
        )
    )
    def test_model_create(self, model, objects_list, model_attr):
        with session_factory() as session:
            session.add_all(objects_list)
            session.commit()
            query = select(func.count()).select_from(model)
            objects_in_model_count = session.execute(query)
            assert objects_in_model_count.scalar_one() == len(objects_list)
            query_all = select(model)
            res = session.execute(query_all)
            objects_db = [
                row.__dict__[model_attr] for row in res.scalars().all()
            ]
            objects_sent = [
                restaurant.__dict__[model_attr] for restaurant in objects_list
            ]
            assert objects_db == objects_sent


@pytest.mark.usefixtures("prepare_db_relation")
class TestDbManyToOne:
    @pytest.mark.parametrize(
        ("model, join_model, objects_list, model_attr, join_model_attr, "
         "filter_id"),
        (
            (
                Dish,
                Restaurant,
                lazy_fixture("dishes"),
                "name",
                "restaurant_dishes",
                "restaurant_id",
            ),
            (
                Feedback,
                Client,
                lazy_fixture("feedbacks"),
                "feedback",
                "feedbacks",
                "author_id",
            ),
            (
                Feedback,
                Restaurant,
                lazy_fixture("feedbacks"),
                "feedback",
                "feedbacks",
                "restaurant_id",
            ),
            (
                Order,
                Client,
                lazy_fixture("orders"),
                "comment",
                "orders",
                "client_id",
            ),
        )
    )
    def test_many_to_one_relationship(
        self, model, join_model, objects_list, model_attr,
            join_model_attr, filter_id, restaurants, clients):
        with session_factory() as session:
            session.add_all(restaurants)
            session.add_all(clients)
            session.add_all(objects_list)
            session.commit()
            query = (select(model)
                     .join_from(
                        join_model, join_model.__dict__[join_model_attr]
                    )
                     .where(join_model.id == 1))
            res = session.execute(query)
            objects_sent = [
                row.__dict__[model_attr] for row in objects_list if (
                    row.__dict__[filter_id] == 1)
            ]
            objects_db = [
                row.__dict__[model_attr] for row in res.scalars().all()
            ]
            assert objects_db == objects_sent


@pytest.mark.usefixtures("prepare_db_relation")
class TestDbManyToMany:
    @pytest.mark.parametrize(
        ("model, join_model, objects_list, model_attr, join_model_attr, "
         "fixture"),
        (
            (
             Order,
             Dish,
             lazy_fixture("dishes"),
             "dishes",
             "name",
             lazy_fixture("orders"),
            ),
        )
    )
    def test_many_to_many_relationship(
        self, model, join_model, objects_list, model_attr, join_model_attr,
        fixture, restaurants, clients
    ):
        with session_factory() as session:
            session.add_all(restaurants)
            session.add_all(clients)
            session.add_all(objects_list)
            session.add_all(fixture)
            session.commit()
            get_order = (select(model)
                         .options(selectinload(model.__dict__[model_attr]))
                         .filter_by(id=1))
            order_1 = (session.execute(get_order)).scalar_one()
            for dish in objects_list:
                order_1.__dict__[model_attr].append(dish)
            session.commit()
            query = (select(model)
                     .options(selectinload(model.__dict__[model_attr])
                     .load_only(join_model.__dict__[join_model_attr])))
            res = session.execute(query)
            result = res.unique().scalar_one()
            assert result.__dict__[model_attr] == objects_list


@pytest.mark.usefixtures("prepare_db_relation")
class TestDbLogic:
    def test_order_cost(
        self, restaurants, clients, dishes, orders
    ):
        with session_factory() as session:
            session.add_all(restaurants)
            session.add_all(clients)
            session.add_all(dishes)
            session.add_all(orders)
            session.commit()
            get_order = (select(Order)
                         .options(selectinload(Order.dishes))
                         .filter_by(id=1))
            order_1 = (session.execute(get_order)).scalar_one()
            for dish in dishes:
                order_1.dishes.append(dish)
            session.commit()
            query = (select(Order)
                     .options(selectinload(Order.dishes))
                     .filter_by(id=1))
            res = session.execute(query)
            result = res.unique().scalar_one()
            orders_dishes = sum(dish.cost for dish in result.dishes)
            sent_dishes = sum(dish.cost for dish in dishes)
            assert orders_dishes == sent_dishes
