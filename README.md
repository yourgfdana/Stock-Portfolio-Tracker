# Stock-Portfolio-Tracker


Today’s financial markets have slowly become volatile, allowing individual investors to face the challenge of monitoring their portfolios and forecasting future trends across multiple stocks. While financial institutions have access to professional analytical tools, most individual investors rely on fragmented data sources and lack clear insights into performance trends or potential price movements. Highly volatile markets allow investors to become emotional and lead to mishaps in decision-making, resulting in poor trading choices. An automated, data-driven system can remove this bias, which we aim to produce.  

This project aims to design a Python-based stock portfolio tracker and prediction system that allows users to:
Monitor real-time and historical portfolio performance, analyze individual stock metrics such as returns, volatility, and correlations, predict short-term stock trends using machine learning models.

Outcomes:
Provide the user with an easily readable stock prediction service to tell how their stocks will change over time. As well as a way to visualize their portfolios without needing to do it themselves, simple predictive analytics to improve their overall decision-making in stocks, reusable service so that it can be used by multiple clients’ data. 

Group: Leighana Ruiz (lruiz2@stevens.edu, @lruiz-Programs), Johnny Cantos (jcantos@stevens.edu, @jcantos), and Melissa Rich (mrich@stevens.edu, @yourgfdana).

Structure: Program contains tools to help user develop a stock portfolio (portfolio.py) and watch the stock market to inform decisions (stock.py). 

Dependencies and Installation:

Requires Python version 3.12 or 3.13 to run correctly. All required packages must be installed in the same Python environment used to run the Jupyter Notebook.

Required packages:

pandas – used for handling time-series stock data and performing financial calculations.
matplotlib – used for visualizing stock prices and portfolio values.
yfinance – used to retrieve publicly available stock market data from Yahoo Finance.
pytest – used to run unit tests for the Stock and Portfolio classes.
jupyter – used to run the main program notebook (main.ipynb).

To install all required packages, run the following command in the terminal:

python -m pip install pandas matplotlib yfinance pytest jupyter

After installing the packages, restart Jupyter Notebook before running the main notebook to ensure all modules are properly loaded.

For for the tests, make a folder to contian the test files.
