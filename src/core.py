"""Module with Order, Product, and OrderBuilder implementations"""

class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


class Order:
    def __init__(self, client: str, products: list, address: str = None, 
                 coupon: str = None, payment_method: str = None, observation: str = None):
        self.client = client
        self.products = products
        self.address = address
        self.coupon = coupon
        self.payment_method = payment_method
        self.observation = observation

    def total(self) -> float:
        """Returns the sum of the prices of all products in the order."""
        return sum(product.price for product in self.products)


class OrderBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._client = None
        self._products = []
        self._address = None
        self._coupon = None
        self._payment_method = None
        self._observation = None

    def set_client(self, client: str):
        self._client = client
        return self  # Enables method chaining

    def add_product(self, product: Product):
        self._products.append(product)
        return self

    def set_address(self, address: str):
        self._address = address
        return self

    def set_coupon(self, coupon: str):
        self._coupon = coupon
        return self

    def set_payment_method(self, payment_method: str):
        self._payment_method = payment_method
        return self

    def set_observation(self, observation: str):
        self._observation = observation
        return self

    def build(self) -> Order:
        # Rejects the construction if there is no client
        if not self._client:
            raise ValueError("Cannot build an order without a client.")

        # Creates instance with orders list copy
        order = Order(
            client=self._client,
            products=self._products.copy(), 
            address=self._address,
            coupon=self._coupon,
            payment_method=self._payment_method,
            observation=self._observation
        )
        
        self.reset()  # cleans builder for future use
        return order