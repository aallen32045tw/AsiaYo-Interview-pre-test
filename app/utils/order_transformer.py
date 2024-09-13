from app.utils.validation_strategies import CurrencyValidationStrategy, NameValidationStrategy, PriceValidationStrategy

class OrderTransformer:
    def __init__(self):
        self.strategies = {
            'name': NameValidationStrategy(),
            'price': PriceValidationStrategy(),
            'currency': CurrencyValidationStrategy()
        }

    def transform(self, order_data):
        transformed_order = order_data.copy()
        errors = []

        for field, strategy in self.strategies.items():
            field_errors = strategy.validate(order_data[field])
            errors.extend(field_errors)

        if order_data['currency'] == 'USD':
            transformed_order['price'] = '{:.2f}'.format(float(order_data['price']) * 31)
            transformed_order['currency'] = 'TWD'

        return transformed_order, errors