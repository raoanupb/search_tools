"""
Financial News Search Tool

Provides search capabilities for financial news from various sources using
NewsAPI and other free sources.

API Documentation: https://newsapi.org/docs

Free API key available at: https://newsapi.org/register
Rate limit: 100 requests per day (free tier)
"""

import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import time


class FinancialNewsSearch:
    """
    Search tool for financial news.

    Uses NewsAPI and other sources to search for financial news articles,
    market updates, and company-specific news.

    Free API key required for NewsAPI (get at https://newsapi.org/register)
    Rate limit: 100 requests per day (free tier)
    """

    NEWSAPI_URL = "https://newsapi.org/v2"

    def __init__(self, newsapi_key: Optional[str] = None):
        """
        Initialize the Financial News search tool.

        Args:
            newsapi_key: Optional NewsAPI key for enhanced news search
        """
        self.newsapi_key = newsapi_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SearchTools/0.1.0 (Language Agent Search Tool)'
        })

    def search_news(
        self,
        query: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        language: str = "en",
        sort_by: str = "relevancy",
        page_size: int = 20
    ) -> List[Dict]:
        """
        Search for financial news articles.

        Args:
            query: Search query (company name, ticker, topic, etc.)
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            language: Language code (default: 'en')
            sort_by: Sort by 'relevancy', 'popularity', or 'publishedAt'
            page_size: Number of results (max 100)

        Returns:
            List of news articles

        Example:
            >>> news = FinancialNewsSearch(newsapi_key="your-key")
            >>> articles = news.search_news("Apple stock", from_date="2024-01-01")
            >>> for article in articles:
            ...     print(f"{article['title']} - {article['source']}")
        """
        if not self.newsapi_key:
            raise ValueError("NewsAPI key is required for news search")

        # Default to last 7 days if no dates specified
        if not from_date:
            from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

        params = {
            'q': query,
            'from': from_date,
            'language': language,
            'sortBy': sort_by,
            'pageSize': min(page_size, 100),
            'apiKey': self.newsapi_key
        }

        if to_date:
            params['to'] = to_date

        try:
            response = self.session.get(
                f"{self.NEWSAPI_URL}/everything",
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()

            if data.get('status') == 'ok' and 'articles' in data:
                results = []
                for article in data['articles']:
                    results.append({
                        'title': article.get('title'),
                        'description': article.get('description'),
                        'content': article.get('content'),
                        'url': article.get('url'),
                        'source': article.get('source', {}).get('name'),
                        'author': article.get('author'),
                        'published_at': article.get('publishedAt'),
                        'image_url': article.get('urlToImage')
                    })
                return results

            return []

        except requests.RequestException as e:
            raise Exception(f"NewsAPI search failed: {str(e)}")

    def get_top_headlines(
        self,
        category: str = "business",
        country: str = "us",
        page_size: int = 20
    ) -> List[Dict]:
        """
        Get top financial/business headlines.

        Args:
            category: News category ('business', 'technology', etc.)
            country: Country code (e.g., 'us', 'gb', 'in')
            page_size: Number of results (max 100)

        Returns:
            List of top headlines

        Example:
            >>> news = FinancialNewsSearch(newsapi_key="your-key")
            >>> headlines = news.get_top_headlines(category="business")
        """
        if not self.newsapi_key:
            raise ValueError("NewsAPI key is required for top headlines")

        params = {
            'category': category,
            'country': country,
            'pageSize': min(page_size, 100),
            'apiKey': self.newsapi_key
        }

        try:
            response = self.session.get(
                f"{self.NEWSAPI_URL}/top-headlines",
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()

            if data.get('status') == 'ok' and 'articles' in data:
                results = []
                for article in data['articles']:
                    results.append({
                        'title': article.get('title'),
                        'description': article.get('description'),
                        'content': article.get('content'),
                        'url': article.get('url'),
                        'source': article.get('source', {}).get('name'),
                        'author': article.get('author'),
                        'published_at': article.get('publishedAt'),
                        'image_url': article.get('urlToImage')
                    })
                return results

            return []

        except requests.RequestException as e:
            raise Exception(f"NewsAPI top headlines request failed: {str(e)}")

    def search_company_news(
        self,
        company: str,
        days: int = 7,
        page_size: int = 20
    ) -> List[Dict]:
        """
        Search for news about a specific company.

        Args:
            company: Company name or ticker
            days: Number of days to look back
            page_size: Number of results

        Returns:
            List of company-specific news articles

        Example:
            >>> news = FinancialNewsSearch(newsapi_key="your-key")
            >>> apple_news = news.search_company_news("Apple Inc", days=7)
        """
        from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        return self.search_news(
            query=company,
            from_date=from_date,
            sort_by="publishedAt",
            page_size=page_size
        )

    def search_market_news(
        self,
        topic: str = "stock market",
        days: int = 1,
        page_size: int = 20
    ) -> List[Dict]:
        """
        Search for general market news.

        Args:
            topic: Market topic (e.g., "stock market", "forex", "commodities")
            days: Number of days to look back
            page_size: Number of results

        Returns:
            List of market news articles

        Example:
            >>> news = FinancialNewsSearch(newsapi_key="your-key")
            >>> market_news = news.search_market_news("stock market", days=1)
        """
        from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        return self.search_news(
            query=topic,
            from_date=from_date,
            sort_by="publishedAt",
            page_size=page_size
        )

    def search_earnings_news(
        self,
        days: int = 7,
        page_size: int = 20
    ) -> List[Dict]:
        """
        Search for earnings-related news.

        Args:
            days: Number of days to look back
            page_size: Number of results

        Returns:
            List of earnings news articles
        """
        from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        return self.search_news(
            query="earnings OR quarterly results",
            from_date=from_date,
            sort_by="publishedAt",
            page_size=page_size
        )

    def search_crypto_news(
        self,
        crypto: str = "cryptocurrency",
        days: int = 7,
        page_size: int = 20
    ) -> List[Dict]:
        """
        Search for cryptocurrency news.

        Args:
            crypto: Cryptocurrency name or "cryptocurrency" for general news
            days: Number of days to look back
            page_size: Number of results

        Returns:
            List of crypto news articles

        Example:
            >>> news = FinancialNewsSearch(newsapi_key="your-key")
            >>> btc_news = news.search_crypto_news("Bitcoin", days=3)
        """
        from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        return self.search_news(
            query=crypto,
            from_date=from_date,
            sort_by="publishedAt",
            page_size=page_size
        )

    def get_financial_sources(self) -> List[str]:
        """
        Get list of popular financial news sources.

        Returns:
            List of financial news source names
        """
        return [
            "Bloomberg",
            "Reuters",
            "Financial Times",
            "Wall Street Journal",
            "CNBC",
            "MarketWatch",
            "Seeking Alpha",
            "The Motley Fool",
            "Barron's",
            "Investor's Business Daily",
            "Yahoo Finance",
            "Business Insider",
            "Forbes",
            "Fortune"
        ]

    def search_by_source(
        self,
        source: str,
        query: Optional[str] = None,
        days: int = 7,
        page_size: int = 20
    ) -> List[Dict]:
        """
        Search news from a specific financial source.

        Args:
            source: News source name (e.g., "Bloomberg", "Reuters")
            query: Optional search query
            days: Number of days to look back
            page_size: Number of results

        Returns:
            List of articles from the specified source

        Example:
            >>> news = FinancialNewsSearch(newsapi_key="your-key")
            >>> reuters = news.search_by_source("Reuters", query="tech stocks")
        """
        if not self.newsapi_key:
            raise ValueError("NewsAPI key is required")

        from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        params = {
            'sources': source.lower().replace(' ', '-'),
            'from': from_date,
            'pageSize': min(page_size, 100),
            'apiKey': self.newsapi_key,
            'sortBy': 'publishedAt'
        }

        if query:
            params['q'] = query

        try:
            response = self.session.get(
                f"{self.NEWSAPI_URL}/everything",
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()

            if data.get('status') == 'ok' and 'articles' in data:
                results = []
                for article in data['articles']:
                    results.append({
                        'title': article.get('title'),
                        'description': article.get('description'),
                        'content': article.get('content'),
                        'url': article.get('url'),
                        'source': article.get('source', {}).get('name'),
                        'author': article.get('author'),
                        'published_at': article.get('publishedAt'),
                        'image_url': article.get('urlToImage')
                    })
                return results

            return []

        except requests.RequestException as e:
            raise Exception(f"NewsAPI source search failed: {str(e)}")
