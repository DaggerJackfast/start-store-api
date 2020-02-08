import factory
from app import db
from models import Product, Shipping
session = db.session


class ProductFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Product
        sqlalchemy_session = session
    id = factory.Sequence(lambda n: n)
    name = factory.Faker('company')
    description = factory.Faker('text')
    price = factory.Faker('random_int', min=0, max=1000)
    enabled = True


class ShippingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Shipping
        sqlalchemy_session = session

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('first_name')
    price = factory.Faker('random_int', min=0, max=100)


def get_next_id(model) -> int:
    last = session.query(model).order_by(model.id.desc()).first()

    return last.id + 1 if last else 0


def create_list(factory, number: int):
    model = factory._meta.get_model_class()
    factory.reset_sequence(get_next_id(model))
    factory.create_batch(number)
    session.commit()
    return session.query(model).all()


def run_seed():
    create_list(ProductFactory, 10)
    create_list(ShippingFactory, 5)


if __name__ == "__main__":
    run_seed()
