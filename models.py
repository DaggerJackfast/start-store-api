from app import db
from flask_security import UserMixin, RoleMixin


class Updatable(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), server_default=db.func.now(), server_onupdate=db.func.now())


class Product(Updatable):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String())
    price = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    enabled = db.Column(db.Boolean())


class Shipping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    price = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))


class Order(Updatable):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    address = db.Column(db.String(), nullable=False, unique=True)
    # products = db.relationship('Product', secondary='OrderItem', backref=db.backref("orders"), lazy='subquery')


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(Updatable, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(Updatable, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

