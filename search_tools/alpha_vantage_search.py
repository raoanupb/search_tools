"""
Alpha Vantage Search Tool

Provides advanced financial data, technical indicators, and fundamental data
using the Alpha Vantage API.

API Documentation: https://www.alphavantage.co/documentation/

Free API key available at: https://www.alphavantage.co/support/#api-key
Rate limit: 5 API calls per minute, 500 calls per day (free tier)
"""

import requests
from typing import List, Dict, Optional
import time


class AlphaVantageSearch:
    """
    Search tool for Alpha Vantage financial data.

    Uses the free Alpha Vantage API for stock data, technical indicators,
    fundamental data, and more.

    Free API key required (get at https://www.alphavantage.co/support/#api-key)
    Rate limits: 5 calls/minute, 500 calls/day (free tier)
    """

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key: str):
        """
        Initialize the Alpha Vantage search tool.

        Args:
            api_key: Alpha Vantage API key (get free at https://www.alphavantage.co/support/#api-key)
        """
        if not api_key:
            raise ValueError("Alpha Vantage API key is required")

        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SearchTools/0.1.0 (Language Agent Search Tool)'
        })

    def search_symbols(self, keywords: str) -> List[Dict]:
        """
        Search for stock symbols by company name or keywords.

        Args:
            keywords: Search keywords (company name, ticker symbol, etc.)

        Returns:
            List of matching symbols with details

        Example:
            >>> av = AlphaVantageSearch(api_key="your-key")
            >>> results = av.search_symbols("Apple")
            >>> for match in results:
            ...     print(f"{match['symbol']}: {match['name']}")
        """
        params = {
            'function': 'SYMBOL_SEARCH',
            'keywords': keywords,
            'apikey': self.api_key
        }

        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            if 'bestMatches' in data:
                results = []
                for match in data['bestMatches']:
                    results.append({
                        'symbol': match.get('1. symbol'),
                        'name': match.get('2. name'),
                        'type': match.get('3. type'),
                        'region': match.get('4. region'),
                        'market_open': match.get('5. marketOpen'),
                        'market_close': match.get('6. marketClose'),
                        'timezone': match.get('7. timezone'),
                        'currency': match.get('8. currency'),
                        'match_score': float(match.get('9. matchScore', 0))
                    })
                return results

            return []

        except requests.RequestException as e:
            raise Exception(f"Alpha Vantage symbol search failed: {str(e)}")
        finally:
            time.sleep(12)  # Rate limiting: 5 calls per minute

    def get_quote(self, symbol: str) -> Optional[Dict]:
        """
        Get real-time quote for a stock symbol.

        Args:
            symbol: Stock ticker symbol

        Returns:
            Dictionary containing quote information

        Example:
            >>> av = AlphaVantageSearch(api_key="your-key")
            >>> quote = av.get_quote("AAPL")
            >>> print(f"${quote['price']} ({quote['change_percent']})")
        """
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': self.api_key
        }

        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            if 'Global Quote' in data and data['Global Quote']:
                quote = data['Global Quote']
                return {
                    'symbol': quote.get('01. symbol'),
                    'price': float(quote.get('05. price', 0)),
                    'volume': int(quote.get('06. volume', 0)),
                    'latest_trading_day': quote.get('07. latest trading day'),
                    'previous_close': float(quote.get('08. previous close', 0)),
                    'change': float(quote.get('09. change', 0)),
                    'change_percent': quote.get('10. change percent', '0%').rstrip('%'),
                    'open': float(quote.get('02. open', 0)),
                    'high': float(quote.get('03. high', 0)),
                    'low': float(quote.get('04. low', 0))
                }

            return None

        except requests.RequestException as e:
            raise Exception(f"Alpha Vantage quote request failed: {str(e)}")
        finally:
            time.sleep(12)

    def get_intraday_data(
        self,
        symbol: str,
        interval: str = "5min",
        outputsize: str = "compact"
    ) -> List[Dict]:
        """
        Get intraday time series data.

        Args:
            symbol: Stock ticker symbol
            interval: Time interval ('1min', '5min', '15min', '30min', '60min')
            outputsize: 'compact' (last 100 data points) or 'full' (full history)

        Returns:
            List of intraday data points

        Example:
            >>> av = AlphaVantageSearch(api_key="your-key")
            >>> data = av.get_intraday_data("AAPL", interval="5min")
        """
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': symbol,
            'interval': interval,
            'outputsize': outputsize,
            'apikey': self.api_key
        }

        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            time_series_key = f'Time Series ({interval})'

            if time_series_key in data:
                results = []
                for timestamp, values in list(data[time_series_key].items())[:100]:
                    results.append({
                        'timestamp': timestamp,
                        'open': float(values.get('1. open', 0)),
                        'high': float(values.get('2. high', 0)),
                        'low': float(values.get('3. low', 0)),
                        'close': float(values.get('4. close', 0)),
                        'volume': int(values.get('5. volume', 0))
                    })
                return results

            return []

        except requests.RequestException as e:
            raise Exception(f"Alpha Vantage intraday data request failed: {str(e)}")
        finally:
            time.sleep(12)

    def get_daily_data(
        self,
        symbol: str,
        outputsize: str = "compact"
    ) -> List[Dict]:
        """
        Get daily time series data.

        Args:
            symbol: Stock ticker symbol
            outputsize: 'compact' (last 100 days) or 'full' (20+ years)

        Returns:
            List of daily data points
        """
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'outputsize': outputsize,
            'apikey': self.api_key
        }

        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            if 'Time Series (Daily)' in data:
                results = []
                for date, values in list(data['Time Series (Daily)'].items())[:100]:
                    results.append({
                        'date': date,
                        'open': float(values.get('1. open', 0)),
                        'high': float(values.get('2. high', 0)),
                        'low': float(values.get('3. low', 0)),
                        'close': float(values.get('4. close', 0)),
                        'volume': int(values.get('5. volume', 0))
                    })
                return results

            return []

        except requests.RequestException as e:
            raise Exception(f"Alpha Vantage daily data request failed: {str(e)}")
        finally:
            time.sleep(12)

    def get_sma(
        self,
        symbol: str,
        interval: str = "daily",
        time_period: int = 20,
        series_type: str = "close"
    ) -> List[Dict]:
        """
        Get Simple Moving Average (SMA) indicator.

        Args:
            symbol: Stock ticker symbol
            interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly')
            time_period: Number of data points for average
            series_type: Price type ('close', 'open', 'high', 'low')

        Returns:
            List of SMA data points
        """
        params = {
            'function': 'SMA',
            'symbol': symbol,
            'interval': interval,
            'time_period': time_period,
            'series_type': series_type,
            'apikey': self.api_key
        }

        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            if 'Technical Analysis: SMA' in data:
                results = []
                for date, values in list(data['Technical Analysis: SMA'].items())[:100]:
                    results.append({
                        'date': date,
                        'sma': float(values.get('SMA', 0))
                    })
                return results

            return []

        except requests.RequestException as e:
            raise Exception(f"Alpha Vantage SMA request failed: {str(e)}")
        finally:
            time.sleep(12)

    def get_rsi(
        self,
        symbol: str,
        interval: str = "daily",
        time_period: int = 14,
        series_type: str = "close"
    ) -> List[Dict]:
        """
        Get Relative Strength Index (RSI) indicator.

        Args:
            symbol: Stock ticker symbol
            interval: Time interval
            time_period: Number of data points for RSI
            series_type: Price type

        Returns:
            List of RSI data points
        """
        params = {
            'function': 'RSI',
            'symbol': symbol,
            'interval': interval,
            'time_period': time_period,
            'series_type': series_type,
            'apikey': self.api_key
        }

        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            if 'Technical Analysis: RSI' in data:
                results = []
                for date, values in list(data['Technical Analysis: RSI'].items())[:100]:
                    results.append({
                        'date': date,
                        'rsi': float(values.get('RSI', 0))
                    })
                return results

            return []

        except requests.RequestException as e:
            raise Exception(f"Alpha Vantage RSI request failed: {str(e)}")
        finally:
            time.sleep(12)

    def get_company_overview(self, symbol: str) -> Optional[Dict]:
        """
        Get fundamental company data and financial ratios.

        Args:
            symbol: Stock ticker symbol

        Returns:
            Dictionary containing company overview and fundamentals

        Example:
            >>> av = AlphaVantageSearch(api_key="your-key")
            >>> overview = av.get_company_overview("AAPL")
            >>> print(f"{overview['name']} - {overview['sector']}")
            >>> print(f"PE Ratio: {overview['pe_ratio']}")
        """
        params = {
            'function': 'OVERVIEW',
            'symbol': symbol,
            'apikey': self.api_key
        }

        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            if data and 'Symbol' in data:
                return {
                    'symbol': data.get('Symbol'),
                    'name': data.get('Name'),
                    'description': data.get('Description'),
                    'exchange': data.get('Exchange'),
                    'currency': data.get('Currency'),
                    'country': data.get('Country'),
                    'sector': data.get('Sector'),
                    'industry': data.get('Industry'),
                    'market_cap': int(data.get('MarketCapitalization', 0)) if data.get('MarketCapitalization') else None,
                    'pe_ratio': float(data.get('PERatio', 0)) if data.get('PERatio') and data.get('PERatio') != 'None' else None,
                    'peg_ratio': float(data.get('PEGRatio', 0)) if data.get('PEGRatio') and data.get('PEGRatio') != 'None' else None,
                    'book_value': float(data.get('BookValue', 0)) if data.get('BookValue') else None,
                    'dividend_per_share': float(data.get('DividendPerShare', 0)) if data.get('DividendPerShare') else None,
                    'dividend_yield': float(data.get('DividendYield', 0)) if data.get('DividendYield') else None,
                    'eps': float(data.get('EPS', 0)) if data.get('EPS') else None,
                    'revenue_per_share': float(data.get('RevenuePerShareTTM', 0)) if data.get('RevenuePerShareTTM') else None,
                    'profit_margin': float(data.get('ProfitMargin', 0)) if data.get('ProfitMargin') else None,
                    'operating_margin': float(data.get('OperatingMarginTTM', 0)) if data.get('OperatingMarginTTM') else None,
                    'return_on_assets': float(data.get('ReturnOnAssetsTTM', 0)) if data.get('ReturnOnAssetsTTM') else None,
                    'return_on_equity': float(data.get('ReturnOnEquityTTM', 0)) if data.get('ReturnOnEquityTTM') else None,
                    '52_week_high': float(data.get('52WeekHigh', 0)) if data.get('52WeekHigh') else None,
                    '52_week_low': float(data.get('52WeekLow', 0)) if data.get('52WeekLow') else None,
                    '50_day_ma': float(data.get('50DayMovingAverage', 0)) if data.get('50DayMovingAverage') else None,
                    '200_day_ma': float(data.get('200DayMovingAverage', 0)) if data.get('200DayMovingAverage') else None,
                    'shares_outstanding': int(data.get('SharesOutstanding', 0)) if data.get('SharesOutstanding') else None,
                    'analyst_target_price': float(data.get('AnalystTargetPrice', 0)) if data.get('AnalystTargetPrice') else None
                }

            return None

        except requests.RequestException as e:
            raise Exception(f"Alpha Vantage company overview request failed: {str(e)}")
        finally:
            time.sleep(12)

    def get_earnings(self, symbol: str) -> Dict:
        """
        Get earnings data (annual and quarterly).

        Args:
            symbol: Stock ticker symbol

        Returns:
            Dictionary containing annual and quarterly earnings

        Example:
            >>> av = AlphaVantageSearch(api_key="your-key")
            >>> earnings = av.get_earnings("AAPL")
            >>> for q in earnings['quarterly'][:4]:
            ...     print(f"Q{q['fiscal_quarter']} {q['fiscal_year']}: ${q['reported_eps']}")
        """
        params = {
            'function': 'EARNINGS',
            'symbol': symbol,
            'apikey': self.api_key
        }

        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            result = {
                'annual': [],
                'quarterly': []
            }

            if 'annualEarnings' in data:
                for item in data['annualEarnings']:
                    result['annual'].append({
                        'fiscal_year': item.get('fiscalDateEnding'),
                        'reported_eps': float(item.get('reportedEPS', 0))
                    })

            if 'quarterlyEarnings' in data:
                for item in data['quarterlyEarnings']:
                    result['quarterly'].append({
                        'fiscal_quarter': item.get('fiscalDateEnding'),
                        'reported_date': item.get('reportedDate'),
                        'reported_eps': float(item.get('reportedEPS', 0)) if item.get('reportedEPS') and item.get('reportedEPS') != 'None' else None,
                        'estimated_eps': float(item.get('estimatedEPS', 0)) if item.get('estimatedEPS') and item.get('estimatedEPS') != 'None' else None,
                        'surprise': float(item.get('surprise', 0)) if item.get('surprise') and item.get('surprise') != 'None' else None,
                        'surprise_percentage': float(item.get('surprisePercentage', 0)) if item.get('surprisePercentage') and item.get('surprisePercentage') != 'None' else None
                    })

            return result

        except requests.RequestException as e:
            raise Exception(f"Alpha Vantage earnings request failed: {str(e)}")
        finally:
            time.sleep(12)

    def get_news_sentiment(self, tickers: Optional[str] = None, topics: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """
        Get news and sentiment data for stocks.

        Args:
            tickers: Comma-separated stock symbols (e.g., "AAPL,MSFT")
            topics: News topics (e.g., "technology", "finance")
            limit: Number of results (max 1000)

        Returns:
            List of news articles with sentiment scores

        Example:
            >>> av = AlphaVantageSearch(api_key="your-key")
            >>> news = av.get_news_sentiment(tickers="AAPL")
            >>> for article in news[:5]:
            ...     print(f"{article['title']} - Sentiment: {article['sentiment']}")
        """
        params = {
            'function': 'NEWS_SENTIMENT',
            'apikey': self.api_key,
            'limit': limit
        }

        if tickers:
            params['tickers'] = tickers
        if topics:
            params['topics'] = topics

        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            if 'feed' in data:
                results = []
                for article in data['feed']:
                    results.append({
                        'title': article.get('title'),
                        'url': article.get('url'),
                        'time_published': article.get('time_published'),
                        'authors': article.get('authors', []),
                        'summary': article.get('summary'),
                        'source': article.get('source'),
                        'sentiment': article.get('overall_sentiment_label'),
                        'sentiment_score': float(article.get('overall_sentiment_score', 0)),
                        'topics': [t.get('topic') for t in article.get('topics', [])],
                        'ticker_sentiment': article.get('ticker_sentiment', [])
                    })
                return results

            return []

        except requests.RequestException as e:
            raise Exception(f"Alpha Vantage news sentiment request failed: {str(e)}")
        finally:
            time.sleep(12)
