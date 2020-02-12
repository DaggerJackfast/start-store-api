import json
from flask import Blueprint
from models import Product
from serializers import ProductSerializer


products = Blueprint('products', __name__, url_prefix='/products')

@products.route('/')
def get_products():
    products = Product.query.all()
    return json.dumps(products, cls=ProductSerializer)


@products.route('/<product_id>')
def get_product(product_id):
    product = Product.query.get(product_id)
    return json.dumps(product, cls=ProductSerializer)
