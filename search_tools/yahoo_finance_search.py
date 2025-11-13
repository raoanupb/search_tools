"""
Yahoo Finance Search Tool

Provides stock market data, company information, and financial metrics using
Yahoo Finance.

Uses the yfinance library which provides free access to Yahoo Finance data.
No API key required.
"""

import requests
from typing import List, Dict, Optional, Union
from datetime import datetime, timedelta
import time

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("Warning: yfinance library not available. Install with: pip install yfinance")


class YahooFinanceSearch:
    """
    Search tool for Yahoo Finance stock market data.

    Uses the free yfinance library to access stock prices, company information,
    financial statements, and more. No API key required.
    """

    def __init__(self):
        """Initialize the Yahoo Finance search tool."""
        if not YFINANCE_AVAILABLE:
            raise ImportError(
                "yfinance library is required. "
                "Install it with: pip install yfinance"
            )

    def search_ticker(self, query: str) -> List[Dict]:
        """
        Search for stock tickers by company name or symbol.

        Args:
            query: Company name or ticker symbol

        Returns:
            List of matching tickers with basic information

        Example:
            >>> yf_search = YahooFinanceSearch()
            >>> results = yf_search.search_ticker("Apple")
        """
        # Note: yfinance doesn't have a direct search API
        # This is a simple implementation that tries the query as a ticker
        try:
            ticker = yf.Ticker(query.upper())
            info = ticker.info

            if info and 'symbol' in info:
                return [{
                    'symbol': info.get('symbol'),
                    'name': info.get('longName', info.get('shortName', 'N/A')),
                    'exchange': info.get('exchange', 'N/A'),
                    'currency': info.get('currency', 'N/A'),
                    'quote_type': info.get('quoteType', 'N/A')
                }]
            return []
        except Exception as e:
            return []

    def get_quote(self, symbol: str) -> Optional[Dict]:
        """
        Get current quote for a stock symbol.

        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')

        Returns:
            Dictionary containing current quote information

        Example:
            >>> yf_search = YahooFinanceSearch()
            >>> quote = yf_search.get_quote("AAPL")
            >>> print(f"${quote['current_price']} ({quote['change_percent']}%)")
        """
        try:
            ticker = yf.Ticker(symbol.upper())
            info = ticker.info

            # Get latest price data
            hist = ticker.history(period="2d")

            if hist.empty:
                return None

            current_price = hist['Close'].iloc[-1]
            previous_close = info.get('previousClose', hist['Close'].iloc[-2] if len(hist) > 1 else current_price)

            change = current_price - previous_close
            change_percent = (change / previous_close) * 100 if previous_close else 0

            return {
                'symbol': symbol.upper(),
                'name': info.get('longName', info.get('shortName', 'N/A')),
                'current_price': round(current_price, 2),
                'previous_close': round(previous_close, 2),
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'volume': hist['Volume'].iloc[-1],
                'market_cap': info.get('marketCap'),
                'currency': info.get('currency', 'USD'),
                'exchange': info.get('exchange', 'N/A')
            }

        except Exception as e:
            raise Exception(f"Failed to get quote for {symbol}: {str(e)}")

    def get_historical_data(
        self,
        symbol: str,
        period: str = "1mo",
        interval: str = "1d",
        start: Optional[str] = None,
        end: Optional[str] = None
    ) -> List[Dict]:
        """
        Get historical price data for a stock.

        Args:
            symbol: Stock ticker symbol
            period: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
            interval: Data interval ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1d', '5d', '1wk', '1mo', '3mo')
            start: Start date (YYYY-MM-DD) - overrides period
            end: End date (YYYY-MM-DD)

        Returns:
            List of dictionaries containing historical data

        Example:
            >>> yf_search = YahooFinanceSearch()
            >>> history = yf_search.get_historical_data("AAPL", period="1mo")
            >>> for day in history[-5:]:
            ...     print(f"{day['date']}: ${day['close']}")
        """
        try:
            ticker = yf.Ticker(symbol.upper())

            if start and end:
                hist = ticker.history(start=start, end=end, interval=interval)
            else:
                hist = ticker.history(period=period, interval=interval)

            if hist.empty:
                return []

            results = []
            for date, row in hist.iterrows():
                results.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': round(row['Open'], 2),
                    'high': round(row['High'], 2),
                    'low': round(row['Low'], 2),
                    'close': round(row['Close'], 2),
                    'volume': int(row['Volume'])
                })

            return results

        except Exception as e:
            raise Exception(f"Failed to get historical data for {symbol}: {str(e)}")

    def get_company_info(self, symbol: str) -> Optional[Dict]:
        """
        Get detailed company information.

        Args:
            symbol: Stock ticker symbol

        Returns:
            Dictionary containing company information

        Example:
            >>> yf_search = YahooFinanceSearch()
            >>> info = yf_search.get_company_info("AAPL")
            >>> print(f"{info['name']} - {info['sector']}")
            >>> print(f"Market Cap: ${info['market_cap']:,}")
        """
        try:
            ticker = yf.Ticker(symbol.upper())
            info = ticker.info

            return {
                'symbol': symbol.upper(),
                'name': info.get('longName', info.get('shortName', 'N/A')),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'description': info.get('longBusinessSummary', 'N/A'),
                'website': info.get('website', 'N/A'),
                'employees': info.get('fullTimeEmployees', 'N/A'),
                'headquarters': f"{info.get('city', '')}, {info.get('state', '')}, {info.get('country', '')}".strip(', '),
                'market_cap': info.get('marketCap'),
                'enterprise_value': info.get('enterpriseValue'),
                'pe_ratio': info.get('trailingPE'),
                'forward_pe': info.get('forwardPE'),
                'peg_ratio': info.get('pegRatio'),
                'price_to_book': info.get('priceToBook'),
                'dividend_yield': info.get('dividendYield'),
                'beta': info.get('beta'),
                '52_week_high': info.get('fiftyTwoWeekHigh'),
                '52_week_low': info.get('fiftyTwoWeekLow'),
                'average_volume': info.get('averageVolume'),
                'shares_outstanding': info.get('sharesOutstanding')
            }

        except Exception as e:
            raise Exception(f"Failed to get company info for {symbol}: {str(e)}")

    def get_financial_statements(self, symbol: str) -> Dict:
        """
        Get financial statements (income statement, balance sheet, cash flow).

        Args:
            symbol: Stock ticker symbol

        Returns:
            Dictionary containing financial statements

        Example:
            >>> yf_search = YahooFinanceSearch()
            >>> financials = yf_search.get_financial_statements("AAPL")
            >>> print(financials['income_statement'].head())
        """
        try:
            ticker = yf.Ticker(symbol.upper())

            return {
                'income_statement': ticker.financials.to_dict() if not ticker.financials.empty else {},
                'balance_sheet': ticker.balance_sheet.to_dict() if not ticker.balance_sheet.empty else {},
                'cash_flow': ticker.cashflow.to_dict() if not ticker.cashflow.empty else {},
                'quarterly_income_statement': ticker.quarterly_financials.to_dict() if not ticker.quarterly_financials.empty else {},
                'quarterly_balance_sheet': ticker.quarterly_balance_sheet.to_dict() if not ticker.quarterly_balance_sheet.empty else {},
                'quarterly_cash_flow': ticker.quarterly_cashflow.to_dict() if not ticker.quarterly_cashflow.empty else {}
            }

        except Exception as e:
            raise Exception(f"Failed to get financial statements for {symbol}: {str(e)}")

    def get_recommendations(self, symbol: str) -> List[Dict]:
        """
        Get analyst recommendations.

        Args:
            symbol: Stock ticker symbol

        Returns:
            List of analyst recommendations
        """
        try:
            ticker = yf.Ticker(symbol.upper())
            recommendations = ticker.recommendations

            if recommendations is None or recommendations.empty:
                return []

            results = []
            for date, row in recommendations.tail(10).iterrows():
                results.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'firm': row.get('Firm', 'N/A'),
                    'to_grade': row.get('To Grade', 'N/A'),
                    'from_grade': row.get('From Grade', 'N/A'),
                    'action': row.get('Action', 'N/A')
                })

            return results

        except Exception as e:
            raise Exception(f"Failed to get recommendations for {symbol}: {str(e)}")

    def get_earnings_calendar(self, symbol: str) -> Optional[Dict]:
        """
        Get earnings calendar information.

        Args:
            symbol: Stock ticker symbol

        Returns:
            Dictionary containing earnings information
        """
        try:
            ticker = yf.Ticker(symbol.upper())
            calendar = ticker.calendar

            if calendar is None or calendar.empty:
                return None

            return {
                'earnings_date': calendar.get('Earnings Date', ['N/A'])[0] if isinstance(calendar.get('Earnings Date'), list) else calendar.get('Earnings Date', 'N/A'),
                'earnings_average': calendar.get('Earnings Average'),
                'earnings_low': calendar.get('Earnings Low'),
                'earnings_high': calendar.get('Earnings High'),
                'revenue_average': calendar.get('Revenue Average'),
                'revenue_low': calendar.get('Revenue Low'),
                'revenue_high': calendar.get('Revenue High')
            }

        except Exception as e:
            return None

    def get_trending_stocks(self, region: str = "US") -> List[Dict]:
        """
        Get trending stocks (most active).

        Args:
            region: Region code ('US', 'GB', 'IN', etc.)

        Returns:
            List of trending stocks

        Note: This uses a workaround as yfinance doesn't have direct trending API
        """
        # This is a basic implementation - in practice, you'd want to use
        # a more comprehensive source for trending stocks
        try:
            # Get some popular tickers as a proxy for trending
            popular_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM', 'V', 'WMT']

            results = []
            for symbol in popular_tickers:
                try:
                    quote = self.get_quote(symbol)
                    if quote:
                        results.append(quote)
                    time.sleep(0.1)  # Be respectful
                except:
                    continue

            # Sort by volume (most active)
            results.sort(key=lambda x: x.get('volume', 0), reverse=True)
            return results[:10]

        except Exception as e:
            raise Exception(f"Failed to get trending stocks: {str(e)}")

    def compare_stocks(self, symbols: List[str]) -> List[Dict]:
        """
        Compare multiple stocks side by side.

        Args:
            symbols: List of stock ticker symbols

        Returns:
            List of dictionaries with comparison data

        Example:
            >>> yf_search = YahooFinanceSearch()
            >>> comparison = yf_search.compare_stocks(['AAPL', 'MSFT', 'GOOGL'])
            >>> for stock in comparison:
            ...     print(f"{stock['symbol']}: ${stock['current_price']} (PE: {stock['pe_ratio']})")
        """
        results = []

        for symbol in symbols:
            try:
                quote = self.get_quote(symbol)
                info = self.get_company_info(symbol)

                if quote and info:
                    results.append({
                        'symbol': symbol.upper(),
                        'name': info['name'],
                        'current_price': quote['current_price'],
                        'change_percent': quote['change_percent'],
                        'market_cap': info['market_cap'],
                        'pe_ratio': info['pe_ratio'],
                        'dividend_yield': info['dividend_yield'],
                        'beta': info['beta'],
                        '52_week_high': info['52_week_high'],
                        '52_week_low': info['52_week_low']
                    })

                time.sleep(0.2)  # Rate limiting

            except Exception as e:
                continue

        return results
