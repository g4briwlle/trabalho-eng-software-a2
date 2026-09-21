from src.core import *


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

if __name__ == "__main__":
    run_tests()