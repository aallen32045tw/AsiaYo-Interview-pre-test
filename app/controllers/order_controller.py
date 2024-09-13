from flask_restful import Resource, reqparse
from ..services.order_service import OrderService
from ..interfaces.order_service_interface import OrderServiceInterface


class OrderController(Resource):
    def __init__(self, order_service: OrderServiceInterface = None):
        self.order_service = order_service or OrderService()
        self.parser = self._create_parser()

    def _create_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True)
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('address', type=dict, required=True)
        parser.add_argument('price', type=str, required=True)
        parser.add_argument('currency', type=str, required=True)
        return parser

    def _validate_order(self, order_data):
        if not all(key in order_data['address'] for key in ['city', 'district', 'street']):
            return False
        return True

    def post(self):
        try:
            args = self.parser.parse_args()
            if not self._validate_order(args):
                return {'error': 'Invalid order data'}, 400
            
            result, status_code = self.order_service.process_order(args)
            return result, status_code
        except Exception as e:
            return {'error': 'Invalid form data'}, 400