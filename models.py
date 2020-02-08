from app import db


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
