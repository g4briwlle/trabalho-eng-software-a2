from src.core import *
from src.payments import PixProcessor, CreditCardProcessor 


def run_tests():
    print("--- Starting Builder (OrderBuilder) Tests ---\n")
    
    # Test 1 & 2: Build an order with >= 2 products and >= 2 optional attributes
    print("Test 1 & 2: Building order with 2 products and 2 optional attributes...")
    try:
        builder = OrderBuilder()
        order = (builder
                 .set_client("John Doe")
                 .add_product(Product("Laptop", 3500.00))
                 .add_product(Product("Wireless Mouse", 150.00))
                 .set_address("123 Main St, Tech City")  # Optional 1
                 .set_payment_method("Credit Card")      # Optional 2
                 .build())
        
        assert order.client == "John Doe"
        assert len(order.products) == 2
        assert order.total() == 3650.00
        assert order.address is not None
        assert order.payment_method is not None
        
        print(f"Success: Order successfully built for '{order.client}'.")
        print(f"Order total: {order.total()} BRL.")
        print(f"Optional attributes used -> Address: '{order.address}', Payment: '{order.payment_method}'.\n")
        
    except Exception as e:
        print(f"Failed: {e}\n")

    # Test 3: Attempt to build an order without a client
    print("Test 3: Attempting to build an order without a client...")
    builder_without_client = OrderBuilder()
    
    try:
        invalid_order = (builder_without_client
                         .add_product(Product("Keyboard", 200.00))
                         .set_coupon("DISCOUNT10")
                         .build())
        print("Failed: The order should not have been built without a client!\n")
    except ValueError as e:
        print(f"Success: Construction correctly rejected. Error message caught: '{e}'\n")

    # Test 4: Verify builder reset (Single instance isolation)
    print("Test 4: Verifying builder reset (no dirty state leak)...")
    try:
        shared_builder = OrderBuilder()
        
        # Constrói o primeiro pedido
        order_a = (shared_builder
                   .set_client("Alice")
                   .add_product(Product("Monitor", 1200.00))
                   .set_address("Rua A, 123")
                   .build())
        
        # Reutiliza A MESMA instância para um segundo pedido
        order_b = (shared_builder
                   .set_client("Bob")
                   .add_product(Product("Mousepad", 50.00))
                   .build())
        
        # Garante que produtos e atributos de 'order_a' não vazaram para 'order_b'
        assert len(order_a.products) == 1
        assert len(order_b.products) == 1
        assert order_b.products[0].name == "Mousepad"
        assert order_b.address is None
        
        print("Success: Builder state was successfully reset between builds.\n")
    except AssertionError:
        print("Failed: State leaked from the first order to the second! Make sure build() calls reset().\n")
    except Exception as e:
        print(f"Failed: {e}\n")

    # Test 5: Payment method matches processor (Q3)
    print("Test 5: Verifying payment method matches the processor (Q3)...")
    try:
        # Pedido 1: PIX
        order_pix = (OrderBuilder()
                     .set_client("Alice")
                     .add_product(Product("Livro", 50.0))
                     .set_payment_method("PIX")
                     .build())
        pix_processor = PixProcessor()
        
        # Pedido 2: Cartão
        order_card = (OrderBuilder()
                      .set_client("Bob")
                      .add_product(Product("Caderno", 20.0))
                      .set_payment_method("CREDIT_CARD")
                      .build())
        card_processor = CreditCardProcessor()

        # Factory Method internal
        payment1 = pix_processor.create_payment()
        payment2 = card_processor.create_payment()

        # Validates correspondance
        assert order_pix.payment_method == "PIX"
        assert type(payment1).__name__ == "PixPayment"
        
        assert order_card.payment_method == "CREDIT_CARD"
        assert type(payment2).__name__ == "CreditCardPayment"
        
        print("Success: Payment method registered in order matches the generated Payment mechanism.\n")
    except Exception as e:
        print(f"Failed: {e}\n")


if __name__ == "__main__":
    run_tests()