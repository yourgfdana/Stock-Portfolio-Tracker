
import matplotlib.pyplot as plt
from stock import Stock


class Portfolio:
    
    def __init__(self):
        """Initialize empty portfolio."""
        self.stocks = []
        self.total_value = 0.0
        self.roi = 0.0
    
    def add_stock(self, ticker):
        """Add a stock to portfolio."""
        stock = Stock(ticker)
        self.stocks.append(stock)
        self.analyze()
    
    def remove_stock(self, ticker):
        """Remove a stock from portfolio."""
        self.stocks = [s for s in self.stocks if s.ticker != ticker.upper()]
        self.analyze()
    
    def analyze(self):
        """Calculate total value and ROI."""
        if not self.stocks:
            return
        
        self.total_value = sum(s.current_price for s in self.stocks)
        
        returns = [(s.current_price - s.past_prices.iloc[0]) / s.past_prices.iloc[0] * 100 
                   for s in self.stocks]
        self.roi = sum(returns) / len(returns)
    
    def visualize(self):

        tickers = [s.ticker for s in self.stocks]
        prices = [s.current_price for s in self.stocks]
        
        plt.bar(tickers, prices)
        plt.xlabel('Stock')
        plt.ylabel('Price ($)')
        plt.title('Portfolio')
        plt.show()
    
 
    def __str__(self):
        return f"Portfolio: {len(self.stocks)} stocks, ${self.total_value:.2f}"
