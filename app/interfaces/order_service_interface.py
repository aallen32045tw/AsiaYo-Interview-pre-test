from abc import ABC, abstractmethod

class OrderServiceInterface(ABC):
    
    @abstractmethod
    def process_order(self, order_data):
        pass