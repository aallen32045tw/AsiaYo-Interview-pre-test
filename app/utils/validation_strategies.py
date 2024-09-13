from abc import ABC, abstractmethod
import re

class ValidationStrategy(ABC):
    @abstractmethod
    def validate(self, data):
        pass

class NameValidationStrategy(ValidationStrategy):
    def validate(self, name):
        errors = []
        if re.search(r'[^a-zA-Z]', name.replace(' ', '')):
            errors.append("Name contains non-English characters")
        if not name.istitle():
            errors.append("Name is not capitalized")
        return errors

class PriceValidationStrategy(ValidationStrategy):
    def validate(self, price):
        try:
            price_value = float(price)
            if price_value > 2000:
                return ["Price is over 2000"]
            return []
        except ValueError:
            return ["Price is not a valid number"]

class CurrencyValidationStrategy(ValidationStrategy):
    def validate(self, currency):
        if currency not in ['TWD', 'USD']:
            return ["Currency format is wrong"]
        return []