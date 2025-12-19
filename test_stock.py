import pandas as pd
import pytest

import stock


def _series(vals):
    """
    deterministic Close series with a simple integer index
    """
    return pd.Series(vals, index=pd.RangeIndex(start=0, stop=len(vals), step=1), name="Close")


def test_compute_metrics_sets_volatility_and_moving_averages():
    """
    Bypasses __init__ and set data directly
    """
    s = stock.Stock.__new__(stock.Stock)
    s.ticker = "TEST"
    s.current_price = 0.0
    s.past_prices = _series(list(range(1, 61)))  
    s.volatility = 0.0
    s.moving_averages = {}

    s.compute_metrics()

    assert "MA_20" in s.moving_averages
    assert "MA_50" in s.moving_averages

    # For 1..60, last 20 are 41..60 => average = (41+60)/2 = 50.5
    assert abs(s.moving_averages["MA_20"] - 50.5) < 1e-9
    # last 50 are 11..60 => average = (11+60)/2 = 35.5
    assert abs(s.moving_averages["MA_50"] - 35.5) < 1e-9

    # volatility should be a finite non-negative float
    assert isinstance(s.volatility, float)
    assert s.volatility >= 0.0


def test_predict_change_returns_expected_symbol():
    """
    Bypasses __init__ and set data directly
    """
    s = stock.Stock.__new__(stock.Stock)
    s.ticker = "TEST"
    s.current_price = 0.0
    s.past_prices = _series([1, 2, 3])
    s.volatility = 0.0

    s.moving_averages = {"MA_20": 10.0, "MA_50": 5.0}
    assert s.predict_change() == "^"

    s.moving_averages = {"MA_20": 5.0, "MA_50": 10.0}
    assert s.predict_change() == "⌄"

    s.moving_averages = {"MA_20": 7.0, "MA_50": 7.0}
    assert s.predict_change() == "-"


def test_fetch_raises_valueerror_on_empty_download(monkeypatch):
    """
    Tests that fetch() raises ValueError when yfinance.download returns empty DataFrame
    """
    def fake_download(*args, **kwargs):
        return pd.DataFrame()

    monkeypatch.setattr(stock.yf, "download", fake_download)

    with pytest.raises(ValueError):
        stock.Stock("NOT_A_REAL_TICKER")
