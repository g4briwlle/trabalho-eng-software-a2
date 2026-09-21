from src.payments import *


def run_tests():
    print("--- Starting Factory Method Tests ---\n")
    
    # Setup two different orders with different requested payment methods
    builder1 = OrderBuilder()
    order1 = (builder1
              .set_client("Gabi")
              .add_product(Product("Monitor", 1200.0))
              .set_payment_method("Pix")
              .build())

    builder2 = OrderBuilder()
    order2 = (builder2
              .set_client("Henrique coelho")
              .add_product(Product("Keyboard", 350.0))
              .set_payment_method("Credit Card")
              .build())

    builder3 = OrderBuilder()
    order3 = (builder3
              .set_client("Henrique gasparelo")
              .add_product(Product("mouse", 100.0))
              .set_payment_method("Milhas")
              .build())
    
    # Setup corresponding processors based on the order
    processors = {
        "Pix": PixFactory(),
        "Credit Card": CreditCardFactory(),
        "Boleto": BoletoFactory(),
        'Milhas' : MilhasFactory()
    }
    
    # Test 1 & 2: Process orders using two different methods and verify mapping
    print(f"Test 1: Processing order 1 (Expected: {order1.payment_method})")
    processor1 = processors[order1.payment_method]
    method_used_1 = processor1.process_order(order1)
    
    assert method_used_1 == order1.payment_method
    print(f"Success: The processed method ({method_used_1}) matches the order's requested method ({order1.payment_method}).\n")
    
    print(f"Test 2: Processing order 2 (Expected: {order2.payment_method})")
    processor2 = processors[order2.payment_method]
    method_used_2 = processor2.process_order(order2)
    
    assert method_used_2 == order2.payment_method
    print(f"Success: The processed method ({method_used_2}) matches the order's requested method ({order2.payment_method}).\n")
    
    print(f"Test 3: Processing order 3 (Expected: {order3.payment_method})")
    processor3 = processors[order3.payment_method]
    method_used_3 = processor3.process_order(order3)
    
    assert method_used_3 == order3.payment_method
    print(f"Success: The processed method ({method_used_3}) matches the order's requested method ({order3.payment_method}).\n")

if __name__ == "__main__":
    run_tests()