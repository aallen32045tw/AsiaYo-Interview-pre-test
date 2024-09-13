from ..interfaces.order_service_interface import OrderServiceInterface
from ..utils.order_transformer import OrderTransformer

class OrderService(OrderServiceInterface):
    def __init__(self):
        self.transformer = OrderTransformer()

    def process_order(self, order_data):
        transformed_order, errors = self.transformer.transform(order_data)
        
        if errors:
            return {'error': errors}, 400

        return {'message': 'Order processed successfully', 'order': transformed_order}, 201