
import os
import json
import logging
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send, emit
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_cors import CORS
from config import config, basedir
from serializers import ProductSerializer, ShippingSerializer

migrate = Migrate()
admin = Admin(name='start-store', template_mode="bootstrap3")


app = Flask(__name__)
CORS(app)

app.config.from_object(config[os.environ.get('ENV', 'DEVELOPMENT')])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)
migrate.init_app(app, db)
admin.init_app(app)
socketio = SocketIO(
    app,
    cors_allowed_origins=os.environ.get('CORS_ALLOWED_ORIGINS', '*'),
    logger=True,
    engineio_logger=True
)

from models import *  # noqa: E401, F403, F401


products = []
with open(os.path.join(basedir, 'fixtures/products.json')) as p:
    products = [dict(x, **{'id': i}) for i, x in enumerate(json.loads(p.read()))]

shipping = []
with open(os.path.join(basedir, './fixtures/shipping.json')) as p:
    shipping = [dict(x, **{'id': i}) for i, x in enumerate(json.loads(p.read()))]

orders = []
messages = []


@app.route('/')
def index():
    return jsonify({'status': 'OK', 'message': 'API is ready...'})


@app.route('/products')
def get_products():
    products = db.session.query(Product).all()
    return json.dumps(products, cls=ProductSerializer)


@app.route('/products/<product_id>')
def get_product(product_id):
    product = db.session.query(Product).get(product_id)
    return json.dumps(product, cls=ProductSerializer)


@app.route('/shipping')
def get_shipping():
    shipping = db.session.query(Shipping).all()
    return json.dumps(shipping, cls=ShippingSerializer)


@app.route('/order/checkout', methods=['POST'])
def order_checkout():
    data = request.get_json()
    print('data: ', data)
    orders.append(data)
    print('orders: ', orders)
    return jsonify({'status': 'success', 'message': 'The order successfully checked.'})


@app.route('/orders')
def get_orders():
    return jsonify(orders)


@socketio.on('connect')
def handle_connect():
    emit("messages", messages)


@socketio.on('messages')
def handle_messages():
    emit("messages", messages)


@socketio.on("message")
def handle_message(message: str):
    messages.append(message)
    emit('message', message, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
