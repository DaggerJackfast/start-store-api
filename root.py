import json
from flask import Blueprint, jsonify, request
from app import db
from models import Shipping
from serializers import ShippingSerializer

orders = []

root = Blueprint('root', __name__)


@root.route('/')
def index():
    return jsonify({'status': 'OK', 'message': 'API is ready...'})


@root.route('/shipping')
def get_shipping():
    shipping = db.session.query(Shipping).all()
    return json.dumps(shipping, cls=ShippingSerializer)


@root.route('/order/checkout', methods=['POST'])
def order_checkout():
    data = request.get_json()
    print('data: ', data)
    orders.append(data)
    print('orders: ', orders)
    return jsonify({'status': 'success', 'message': 'The order successfully checked.'})


@root.route('/orders')
def get_orders():
    return jsonify(orders)
