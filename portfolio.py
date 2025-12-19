import matplotlib.pyplot as plt
from stock import Stock


class Portfolio:
    
    def __init__(self, name="MyPortfolio"):
        #Initialize empty portfolio.
        self.name = name
        self.stocks = []
        self.weights = {} 
        self.total_value = 0.0
        self.roi = 0.0
        
    #Add a stock to the portfolio with a given weight
    def add_stock(self, ticker, weight = 1.0): 
        try:
            if weight <= 0:
                raise ValueError("Weight needs to be positive")

            s = Stock(ticker)
            self.stocks.append(s)
            self.weights[s.ticker] = float(weight)
            self._normalize_weights()
            self.analyze()

        except ValueError as e:
            print(f"Couldn't add stock: {e}")

        except Exception as e:
            print(f"Something unexpected happened: {e}")
    
    #Remove a stock from the portfolio
    def remove_stock(self, ticker): 
        t = ticker.upper()
        self.stocks = [s for s in self.stocks if s.ticker != t]
        self.weights.pop(t, None)

        if self.weights:
            self._normalize_weights()
        self.analyze()

    #Make sure all the weights add up to 1
    def _normalize_weights(self): 
        total = sum(self.weights.values())
        if total == 0:
            raise ValueError("Weights can't all be zero")
        self.weights = {t: w / total for t, w in self.weights.items()}

    #Calculate the total value and average return across all holdings
    def analyze(self):
        if not self.stocks:
            self.total_value = 0.0
            self.roi = 0.0
            return
        
        total = 0.0
        returns = []

        for s in self.stocks:
            total += float(s.current_price)
             #Calculate return from first price to current
            first = float(s.past_prices.iloc[0])
            cur = float(s.current_price)
            if first != 0:
                returns.append((cur - first) / first * 100)
        self.total_value = total
        self.roi = sum(returns) / len(returns) if returns else 0.0
    
    #Show a bar chart of current stock prices
    def visualize(self):        
        if not self.stocks:
            print("Nothing to show - portfolio is empty.")
            return
        tickers = [s.ticker for s in self.stocks]
        prices = [float(s.current_price) for s in self.stocks]
        plt.bar(tickers, prices)
        plt.xlabel("Stock")
        plt.ylabel("Price ($)")
        plt.title(f"{self.name} - Current Prices")
        plt.show()
    
    def daily_portfolio_returns(self):
        #Generator that yields the weighted daily return of the entire portfolio
        if not self.stocks:
            return
        #Get daily returns for each stock
        returns_by_ticker = {}
        for s in self.stocks:
            r = s.past_prices.astype(float).pct_change().dropna()
            returns_by_ticker[s.ticker] = r
        #Find dates where we have data for all stocks
        common_idx = None
        for t in returns_by_ticker:
            if common_idx is None:
                common_idx = returns_by_ticker[t].index
            else:
                common_idx = common_idx.intersection(returns_by_ticker[t].index)
        if common_idx is None or len(common_idx) == 0:
            return
        #Yield weighted return for each day
        for idx in common_idx:
            day_ret = 0.0
            for t, series in returns_by_ticker.items():
                day_ret += self.weights.get(t, 0.0) * float(series.loc[idx])
            yield day_ret

    def __add__(self, other):
        #Combine two portfolios into one
        merged = Portfolio(name=f"{self.name}+{other.name}")

        #Add stocks from first portfolio
        for s in self.stocks:
            merged.stocks.append(s)
            merged.weights[s.ticker] = merged.weights.get(s.ticker, 0.0) + self.weights.get(s.ticker, 0.0)

        #Add stocks from second portfolio
        for s in other.stocks:
            if s.ticker not in merged.weights:
                merged.stocks.append(s)
            merged.weights[s.ticker] = merged.weights.get(s.ticker, 0.0) + other.weights.get(s.ticker, 0.0)

        if merged.weights:
            merged._normalize_weights()

        merged.analyze()
        return merged

    def run_menu(self):
        #Interactive menu for managing the portfolio
        while True:
            print("\n1) Add Stock  2) Remove Stock  3) Analyze  4) Plot  5) Quit")
            choice = input("Choose: ").strip()

            if choice == "1":
                t = input("Ticker: ").strip()
                w = input("Weight (like 0.5): ").strip()
                try:
                    self.add_stock(t, float(w))
                except ValueError:
                    print("Weight needs to be a number.")
            elif choice == "2":
                t = input("Ticker to remove: ").strip()
                self.remove_stock(t)
            elif choice == "3":
                self.analyze()
                print(self)
            elif choice == "4":
                self.visualize()
            elif choice == "5":
                break
            else:
                print("That's not a valid option.")

    def __str__(self):
        return f"{self.name}: {len(self.stocks)} stocks, total=${self.total_value:.2f}, ROI={self.roi:.2f}%"
