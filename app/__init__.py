from flask import Flask
from flask_restful import Api
from .controllers.order_controller import OrderController

def create_app():
    app = Flask(__name__)
    api = Api(app)
    
    api.add_resource(OrderController, '/api/orders')
    
    return app