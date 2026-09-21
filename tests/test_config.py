from src.config import *

def run_tests():
    print("--- Starting Singleton (AppConfig) Tests ---\n")
    
    # Obtaining two references
    config1 = AppConfig()
    config2 = AppConfig()
    
    # Demonstrate that two references represent the same object
    print("Test 1: Do both references point to the same object?")
    print(f"ID of config1: {id(config1)}")
    print(f"ID of config2: {id(config2)}")
    assert config1 is config2
    print("Success: config1 and config2 point to the exact same memory location.\n")
    
    # Demonstrate that a change in one reference is observed by the other
    print("Test 2: Are changes reflected across references?")
    config1.environment = "development"
    config1.debug = True
    print(f"config1 environment: {config1.environment}")
    print(f"config2 environment: {config2.environment}")
    assert config2.environment == "development"
    assert config2.debug is True
    print("Success: The change made via config1 was correctly observed in config2.\n")
    
    # Demonstrate that a subsequent call does not restore initial values
    print("Test 3: Does a new call prevent __init__ from resetting values?")
    config3 = AppConfig()
    print(f"Current values in config3: environment={config3.environment}, debug={config3.debug}")
    assert config3.environment == "development"
    assert config3.currency == "BRL"
    print("Success: Previous state was maintained. The __init__ method did not reset the attributes.\n")


if __name__ == "__main__":
    run_tests()