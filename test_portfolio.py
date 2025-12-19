import pandas as pd
import portfolio


class DummyStock:
    def __init__(self, ticker, current_price, first_price):
        self.ticker = ticker.upper()
        self.current_price = float(current_price)
        self.past_prices = pd.Series([float(first_price), float(current_price)])


def test_portfolio_analyze_total_value_and_roi(monkeypatch):
    """
    Tests Portfolio's total_value and roi calculations
    """
    def stock_factory(ticker):
        """
        Returns a DummyStock with preset prices based on ticker
        """
        if ticker.upper() == "AAA":
            return DummyStock("AAA", current_price=110.0, first_price=100.0)  
        return DummyStock(ticker, current_price=90.0, first_price=100.0)      

    monkeypatch.setattr(portfolio, "Stock", stock_factory)

    p = portfolio.Portfolio()
    p.add_stock("AAA")
    p.add_stock("BBB")

    assert len(p.stocks) == 2
    assert abs(p.total_value - (110.0 + 90.0)) < 1e-9
    assert abs(p.roi - 0.0) < 1e-9


def test_portfolio_remove_stock(monkeypatch):
    """
    Tests adding and removing stocks from Portfolio
    """
    def stock_factory(ticker):
        """
        Returns a DummyStock with preset prices based on ticker
        """
        return DummyStock(ticker, current_price=100.0, first_price=100.0)

    monkeypatch.setattr(portfolio, "Stock", stock_factory)

    p = portfolio.Portfolio()
    p.add_stock("AAA")
    p.add_stock("BBB")
    assert len(p.stocks) == 2

    p.remove_stock("AAA")
    assert len(p.stocks) == 1
    assert p.stocks[0].ticker == "BBB"
