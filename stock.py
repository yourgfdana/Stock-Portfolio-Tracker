import pandas as pd
import yfinance as yf


class Stock:
    # Handles stock data and basic metrics

    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.current_price = 0.0
        self.past_prices = pd.Series(dtype=float)
        self.volatility = 0.0
        self.moving_averages = {}
        self.fetch()

    def fetch(self):
        # Download historical prices
        try:
            data = yf.download(self.ticker, period="1y", progress=False)
            if data.empty:
                raise ValueError(f"No data found for {self.ticker}")

            self.past_prices = data["Close"]
            self.current_price = float(self.past_prices.iloc[-1])
            self.compute_metrics()

        except Exception as e:
            raise ValueError(f"Error fetching {self.ticker}: {e}")

    def compute_metrics(self):
        # Daily returns
        returns = self.past_prices.pct_change().dropna()

        # Annualized volatility
        if len(returns) > 1:
            self.volatility = float(returns.std(ddof=1) * (252 ** 0.5))
        else:
            self.volatility = 0.0

        # Moving averages
        self.moving_averages = {
            "MA_20": float(self.past_prices.tail(20).mean()),
            "MA_50": float(self.past_prices.tail(50).mean()),
        }

    def predict_change(self):
        # Simple trend prediction
        ma20 = self.moving_averages.get("MA_20", 0)
        ma50 = self.moving_averages.get("MA_50", 0)

        if ma20 > ma50:
            return "^"
        elif ma20 < ma50:
            return "⌄"
        else:
            return "-"

    def __str__(self):
        return f"{self.ticker}: ${self.current_price:.2f}"
