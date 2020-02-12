import os
import json
import logging
from flask import Flask, Blueprint, render_template, request, jsonify
from flask_security import SQLAlchemyUserDatastore, Security
from flask_socketio import SocketIO, send, emit
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_cors import CORS
from config import config, basedir
from serializers import ProductSerializer, ShippingSerializer

migrate = Migrate()
db = SQLAlchemy()
admin = Admin(name='start-store', template_mode="bootstrap3")
socketio = SocketIO(
    cors_allowed_origins=os.environ.get('CORS_ALLOWED_ORIGINS', '*'),
    logger=True,
    engineio_logger=True
)
security = Security()


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[os.environ.get('ENV', 'DEVELOPMENT')])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)
    import events
    socketio.init_app(app)
    from models import User, Role
    user_data_store = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_data_store, register_blueprint=False)
    from root import root
    from products import products
    from users import users
    app.register_blueprint(root)
    app.register_blueprint(products)
    app.register_blueprint(users)
    return app


if __name__ == '__main__':
    socketio.run(create_app(), host="0.0.0.0", port=5000, debug=True)
