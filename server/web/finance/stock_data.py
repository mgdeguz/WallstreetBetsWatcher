from collections import namedtuple

class StockData:
    def __init__(self, ticker=None, sentiment=None, volume_change=None, price_change=None):
        # Checking for types in Python is generally an anti-pattern
        # However, it's far more readable to have named parameters when instantiating the object in reddit.py -- ideally we would use a 
        # 'factory pattern' here but due to the size of the project this might be an overengineered solution.
        assert(any([arg == None for arg in locals()]), False)
        self.ticker = ticker
        self.sentiment = sentiment
        self.volume_change = volume_change
        self.price_change = price_change

