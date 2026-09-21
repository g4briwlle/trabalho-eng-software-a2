"""Module with AppConfig singleton"""

class AppConfig():
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not type(self)._initialized:
            self.environment = "production"
            self.currency = "BRL"
            self.debug = False
            type(self)._initialized = True

        