
import os
import json
import logging
from flask import Flask, render_template, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from config import config

migrate = Migrate()
admin = Admin(name='start-store', template_mode="bootstrap3")


app = Flask(__name__)

app.config.from_object(config[os.environ.get('ENV', 'DEVELOPMENT')])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# db.init_app(app)
# migrate.init_app(app, db)
admin.init_app(app)

products = []
with open('./fixtures/products.json') as p:
    products = [dict(x, **{'id': i}) for i, x in enumerate(json.loads(p.read()))]

shipping = []
with open('./fixtures/shipping.json') as p:
    shipping = [dict(x, **{'id': i}) for i, x in enumerate(json.loads(p.read()))]


@app.route('/')
def index():
    return jsonify({'status': 'OK', 'message': 'API is ready...'})


@app.route('/products')
def get_products():
    return jsonify(products)


@app.route('/products/<product_id>')
def get_product(product_id):
    return jsonify(products[int(product_id)])


@app.route('/shipping')
def get_shipping():
    return jsonify(shipping)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
