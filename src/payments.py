from abc import ABC, abstractmethod
from .core import*

class Payment(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        """Processes the payment and returns the method name used."""
        pass

class PixPayment(Payment):
    def pay(self, amount: float) -> str:
        print(f"-> Processing Pix payment of {amount:.2f} BRL.")
        return "Pix"

class CreditCardPayment(Payment):
    def pay(self, amount: float) -> str:
        print(f"-> Processing Credit Card payment of {amount:.2f} BRL.")
        return "Credit Card"

class BoletoPayment(Payment):
    def pay(self, amount: float) -> str:
        print(f"-> Processing Boleto payment of {amount:.2f} BRL.")
        return "Boleto"

class MilhasPayment(Payment):
    def pay(self, amount: float) -> str:
        print(f'-> Processing Milhas payment of {amount:.2f} BRL.')
        return 'Milhas'


class PaymentProcessor(ABC):
    
    @abstractmethod
    def create_payment(self) -> Payment:
        """Factory method to be implemented by subclasses."""
        pass

    def process_order(self, order: Order) -> str:
        """Common flow: creates payment and processes the order total."""
        print(f"Starting payment process for order of client: {order.client}")
        
        # Instantiation is delegated to the concrete subclass
        payment_mechanism = self.create_payment()
        
        # Common flow executes without knowing the concrete class
        processed_method = payment_mechanism.pay(order.total())
        
        return processed_method

class PixProcessor(PaymentProcessor):
    def create_payment(self) -> Payment:
        return PixPayment()

class CreditCardProcessor(PaymentProcessor):
    def create_payment(self) -> Payment:
        return CreditCardPayment()

class BoletoProcessor(PaymentProcessor):
    def create_payment(self) -> Payment:
        return BoletoPayment()

class MilhasProcessor(PaymentProcessor):
    def create_payment(self) -> Payment:
        return MilhasPayment()
