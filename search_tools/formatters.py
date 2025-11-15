"""
LLM Formatters for Search Results

This module provides markdown formatters for all search tools to convert
search results into LLM-friendly format for prompt injection.

All formatters return markdown strings that can be directly injected into
LLM prompts for context-aware responses.
"""

from typing import List, Dict, Optional, Any
from datetime import datetime


class SearchResultFormatter:
    """Base class for search result formatters."""

    @staticmethod
    def truncate(text: str, max_length: int = 500) -> str:
        """Truncate text to max length with ellipsis."""
        if not text or len(text) <= max_length:
            return text
        return text[:max_length].rsplit(' ', 1)[0] + '...'

    @staticmethod
    def format_list(items: List[str], max_items: int = 5) -> str:
        """Format a list of items, showing only first max_items."""
        if not items:
            return "None"
        display_items = items[:max_items]
        result = ', '.join(display_items)
        if len(items) > max_items:
            result += f" (+{len(items) - max_items} more)"
        return result


class ArxivFormatter(SearchResultFormatter):
    """Format Arxiv search results for LLMs."""

    @staticmethod
    def format_results(results: List[Dict], query: Optional[str] = None) -> str:
        """
        Format Arxiv search results as markdown.

        Args:
            results: List of Arxiv paper dictionaries
            query: Optional search query to include in header

        Returns:
            Markdown formatted string
        """
        if not results:
            return "No Arxiv papers found."

        md = "# Arxiv Search Results\n\n"
        if query:
            md += f"**Query:** {query}\n\n"
        md += f"**Total Results:** {len(results)}\n\n"
        md += "---\n\n"

        for i, paper in enumerate(results, 1):
            md += f"## {i}. {paper.get('title', 'N/A')}\n\n"

            authors = paper.get('authors', [])
            md += f"**Authors:** {ArxivFormatter.format_list(authors)}\n\n"

            md += f"**Published:** {paper.get('published', 'N/A')[:10]}\n\n"

            categories = paper.get('categories', [])
            md += f"**Categories:** {ArxivFormatter.format_list(categories)}\n\n"

            md += f"**URL:** {paper.get('id', 'N/A')}\n\n"

            summary = paper.get('summary', '')
            md += f"**Summary:** {ArxivFormatter.truncate(summary, 300)}\n\n"

            md += "---\n\n"

        return md


class SemanticScholarFormatter(SearchResultFormatter):
    """Format Semantic Scholar search results for LLMs."""

    @staticmethod
    def format_results(results: List[Dict], query: Optional[str] = None) -> str:
        """Format Semantic Scholar search results as markdown."""
        if not results:
            return "No Semantic Scholar papers found."

        md = "# Semantic Scholar Search Results\n\n"
        if query:
            md += f"**Query:** {query}\n\n"
        md += f"**Total Results:** {len(results)}\n\n"
        md += "---\n\n"

        for i, paper in enumerate(results, 1):
            md += f"## {i}. {paper.get('title', 'N/A')}\n\n"

            authors = paper.get('authors', [])
            if authors and isinstance(authors[0], dict):
                author_names = [a.get('name', 'Unknown') for a in authors[:5]]
            else:
                author_names = authors[:5] if authors else []
            md += f"**Authors:** {', '.join(author_names)}\n\n"

            md += f"**Year:** {paper.get('year', 'N/A')}\n\n"
            md += f"**Citations:** {paper.get('citationCount', 0):,}\n\n"

            if paper.get('url'):
                md += f"**URL:** {paper['url']}\n\n"

            if paper.get('abstract'):
                md += f"**Abstract:** {SemanticScholarFormatter.truncate(paper['abstract'], 300)}\n\n"

            md += "---\n\n"

        return md


class PubMedFormatter(SearchResultFormatter):
    """Format PubMed search results for LLMs."""

    @staticmethod
    def format_results(results: List[Dict], query: Optional[str] = None) -> str:
        """Format PubMed search results as markdown."""
        if not results:
            return "No PubMed articles found."

        md = "# PubMed Search Results\n\n"
        if query:
            md += f"**Query:** {query}\n\n"
        md += f"**Total Results:** {len(results)}\n\n"
        md += "---\n\n"

        for i, article in enumerate(results, 1):
            md += f"## {i}. {article.get('title', 'N/A')}\n\n"

            authors = article.get('authors', [])
            md += f"**Authors:** {PubMedFormatter.format_list(authors)}\n\n"

            md += f"**Journal:** {article.get('journal', 'N/A')}\n\n"
            md += f"**Published:** {article.get('publication_date', 'N/A')}\n\n"
            md += f"**PMID:** {article.get('pmid', 'N/A')}\n\n"

            if article.get('url'):
                md += f"**URL:** {article['url']}\n\n"

            abstract = article.get('abstract', '')
            if abstract:
                md += f"**Abstract:** {PubMedFormatter.truncate(abstract, 300)}\n\n"

            keywords = article.get('keywords', [])
            if keywords:
                md += f"**Keywords:** {PubMedFormatter.format_list(keywords)}\n\n"

            md += "---\n\n"

        return md


class CrossRefFormatter(SearchResultFormatter):
    """Format CrossRef search results for LLMs."""

    @staticmethod
    def format_results(results: List[Dict], query: Optional[str] = None) -> str:
        """Format CrossRef search results as markdown."""
        if not results:
            return "No CrossRef publications found."

        md = "# CrossRef Search Results\n\n"
        if query:
            md += f"**Query:** {query}\n\n"
        md += f"**Total Results:** {len(results)}\n\n"
        md += "---\n\n"

        for i, pub in enumerate(results, 1):
            title = pub.get('title', ['N/A'])[0] if pub.get('title') else 'N/A'
            md += f"## {i}. {title}\n\n"

            authors = pub.get('author', [])
            if authors:
                author_names = [f"{a.get('given', '')} {a.get('family', '')}" for a in authors[:5]]
                md += f"**Authors:** {', '.join(author_names)}\n\n"

            year = pub.get('published-print', pub.get('published-online', {}))
            year_str = year.get('date-parts', [['']])[0][0] if year else 'N/A'
            md += f"**Year:** {year_str}\n\n"

            if pub.get('DOI'):
                md += f"**DOI:** {pub['DOI']}\n\n"

            if pub.get('container-title'):
                md += f"**Journal:** {pub.get('container-title', ['N/A'])[0]}\n\n"

            md += "---\n\n"

        return md


class GitHubFormatter(SearchResultFormatter):
    """Format GitHub search results for LLMs."""

    @staticmethod
    def format_repository_results(results: Dict, query: Optional[str] = None) -> str:
        """Format GitHub repository search results as markdown."""
        items = results.get('items', [])
        if not items:
            return "No GitHub repositories found."

        md = "# GitHub Repository Search Results\n\n"
        if query:
            md += f"**Query:** {query}\n\n"
        md += f"**Total Results:** {results.get('total_count', 0):,}\n\n"
        md += "---\n\n"

        for i, repo in enumerate(items, 1):
            md += f"## {i}. {repo.get('full_name', 'N/A')}\n\n"

            if repo.get('description'):
                md += f"**Description:** {repo['description']}\n\n"

            md += f"**⭐ Stars:** {repo.get('stars', 0):,} | "
            md += f"**🔀 Forks:** {repo.get('forks', 0):,} | "
            md += f"**Language:** {repo.get('language', 'N/A')}\n\n"

            topics = repo.get('topics', [])
            if topics:
                md += f"**Topics:** {GitHubFormatter.format_list(topics, 10)}\n\n"

            md += f"**URL:** {repo.get('url', 'N/A')}\n\n"

            md += "---\n\n"

        return md

    @staticmethod
    def format_code_results(results: Dict, query: Optional[str] = None) -> str:
        """Format GitHub code search results as markdown."""
        items = results.get('items', [])
        if not items:
            return "No code results found."

        md = "# GitHub Code Search Results\n\n"
        if query:
            md += f"**Query:** {query}\n\n"
        md += f"**Total Results:** {results.get('total_count', 0):,}\n\n"
        md += "---\n\n"

        for i, item in enumerate(items, 1):
            repo = item.get('repository', {})
            md += f"## {i}. {repo.get('full_name', 'N/A')}/{item.get('path', 'N/A')}\n\n"

            md += f"**Repository Stars:** {repo.get('stars', 0):,}\n\n"
            md += f"**Language:** {repo.get('language', 'N/A')}\n\n"
            md += f"**URL:** {item.get('url', 'N/A')}\n\n"

            md += "---\n\n"

        return md


class YahooFinanceFormatter(SearchResultFormatter):
    """Format Yahoo Finance search results for LLMs."""

    @staticmethod
    def format_quote(quote: Dict) -> str:
        """Format a stock quote as markdown."""
        if not quote:
            return "No quote data available."

        md = f"# Stock Quote: {quote.get('symbol', 'N/A')}\n\n"
        md += f"**Company:** {quote.get('name', 'N/A')}\n\n"

        price = quote.get('current_price', 0)
        change = quote.get('change', 0)
        change_pct = quote.get('change_percent', 0)

        md += f"**Price:** ${price:.2f}\n\n"
        md += f"**Change:** ${change:+.2f} ({change_pct:+.2f}%)\n\n"
        md += f"**Volume:** {quote.get('volume', 0):,}\n\n"

        if quote.get('market_cap'):
            md += f"**Market Cap:** ${quote['market_cap']:,}\n\n"

        return md

    @staticmethod
    def format_company_info(info: Dict) -> str:
        """Format company information as markdown."""
        if not info:
            return "No company information available."

        md = f"# Company Information: {info.get('symbol', 'N/A')}\n\n"
        md += f"**Name:** {info.get('name', 'N/A')}\n\n"
        md += f"**Sector:** {info.get('sector', 'N/A')}\n\n"
        md += f"**Industry:** {info.get('industry', 'N/A')}\n\n"

        if info.get('description'):
            md += f"**Description:** {YahooFinanceFormatter.truncate(info['description'], 300)}\n\n"

        md += "## Financial Metrics\n\n"

        if info.get('market_cap'):
            md += f"- **Market Cap:** ${info['market_cap']:,}\n"
        if info.get('pe_ratio'):
            md += f"- **P/E Ratio:** {info['pe_ratio']:.2f}\n"
        if info.get('dividend_yield'):
            md += f"- **Dividend Yield:** {info['dividend_yield']:.2%}\n"
        if info.get('beta'):
            md += f"- **Beta:** {info['beta']:.2f}\n"

        md += "\n"
        return md

    @staticmethod
    def format_comparison(stocks: List[Dict]) -> str:
        """Format stock comparison as markdown."""
        if not stocks:
            return "No comparison data available."

        md = "# Stock Comparison\n\n"
        md += "| Symbol | Price | Change % | P/E Ratio | Market Cap | Dividend Yield |\n"
        md += "|--------|-------|----------|-----------|------------|----------------|\n"

        for stock in stocks:
            symbol = stock.get('symbol', 'N/A')
            price = f"${stock.get('current_price', 0):.2f}"
            change = f"{stock.get('change_percent', 0):+.2f}%"
            pe = f"{stock.get('pe_ratio', 0):.2f}" if stock.get('pe_ratio') else 'N/A'

            market_cap = stock.get('market_cap', 0)
            mc_str = f"${market_cap/1e9:.1f}B" if market_cap else 'N/A'

            div_yield = stock.get('dividend_yield', 0)
            dy_str = f"{div_yield:.2%}" if div_yield else 'N/A'

            md += f"| {symbol} | {price} | {change} | {pe} | {mc_str} | {dy_str} |\n"

        md += "\n"
        return md


class AlphaVantageFormatter(SearchResultFormatter):
    """Format Alpha Vantage search results for LLMs."""

    @staticmethod
    def format_quote(quote: Dict) -> str:
        """Format Alpha Vantage quote as markdown."""
        if not quote:
            return "No quote data available."

        md = f"# Stock Quote: {quote.get('symbol', 'N/A')}\n\n"
        md += f"**Price:** ${quote.get('price', 0):.2f}\n\n"
        md += f"**Change:** ${quote.get('change', 0):+.2f} ({quote.get('change_percent', '0')}%)\n\n"
        md += f"**Volume:** {quote.get('volume', 0):,}\n\n"
        md += f"**Trading Day:** {quote.get('latest_trading_day', 'N/A')}\n\n"

        return md

    @staticmethod
    def format_company_overview(overview: Dict) -> str:
        """Format company overview as markdown."""
        if not overview:
            return "No company overview available."

        md = f"# Company Overview: {overview.get('symbol', 'N/A')}\n\n"
        md += f"**Name:** {overview.get('name', 'N/A')}\n\n"
        md += f"**Sector:** {overview.get('sector', 'N/A')}\n\n"
        md += f"**Industry:** {overview.get('industry', 'N/A')}\n\n"

        if overview.get('description'):
            md += f"**Description:** {AlphaVantageFormatter.truncate(overview['description'], 300)}\n\n"

        md += "## Financial Metrics\n\n"

        metrics = [
            ('Market Cap', 'market_cap', lambda x: f"${x:,}"),
            ('P/E Ratio', 'pe_ratio', lambda x: f"{x:.2f}"),
            ('EPS', 'eps', lambda x: f"${x:.2f}"),
            ('Profit Margin', 'profit_margin', lambda x: f"{x:.2%}"),
            ('ROE', 'return_on_equity', lambda x: f"{x:.2%}"),
        ]

        for label, key, formatter in metrics:
            if overview.get(key):
                md += f"- **{label}:** {formatter(overview[key])}\n"

        md += "\n"
        return md

    @staticmethod
    def format_news_sentiment(news: List[Dict], ticker: Optional[str] = None) -> str:
        """Format news sentiment results as markdown."""
        if not news:
            return "No news articles found."

        md = "# Financial News with Sentiment Analysis\n\n"
        if ticker:
            md += f"**Ticker:** {ticker}\n\n"
        md += f"**Total Articles:** {len(news)}\n\n"
        md += "---\n\n"

        for i, article in enumerate(news, 1):
            sentiment_emoji = {
                "Bullish": "📈",
                "Bearish": "📉",
                "Neutral": "➡️",
                "Positive": "📈",
                "Negative": "📉"
            }.get(article.get('sentiment', ''), "")

            md += f"## {i}. {sentiment_emoji} {article.get('title', 'N/A')}\n\n"
            md += f"**Source:** {article.get('source', 'N/A')}\n\n"
            md += f"**Sentiment:** {article.get('sentiment', 'N/A')} "
            md += f"(Score: {article.get('sentiment_score', 0):.3f})\n\n"
            md += f"**Published:** {article.get('time_published', 'N/A')}\n\n"

            if article.get('summary'):
                md += f"**Summary:** {AlphaVantageFormatter.truncate(article['summary'], 200)}\n\n"

            md += f"**URL:** {article.get('url', 'N/A')}\n\n"
            md += "---\n\n"

        return md


class FinancialNewsFormatter(SearchResultFormatter):
    """Format Financial News search results for LLMs."""

    @staticmethod
    def format_results(articles: List[Dict], query: Optional[str] = None) -> str:
        """Format financial news articles as markdown."""
        if not articles:
            return "No news articles found."

        md = "# Financial News\n\n"
        if query:
            md += f"**Query:** {query}\n\n"
        md += f"**Total Articles:** {len(articles)}\n\n"
        md += "---\n\n"

        for i, article in enumerate(articles, 1):
            md += f"## {i}. {article.get('title', 'N/A')}\n\n"
            md += f"**Source:** {article.get('source', 'N/A')}\n\n"
            md += f"**Published:** {article.get('published_at', 'N/A')}\n\n"

            if article.get('author'):
                md += f"**Author:** {article['author']}\n\n"

            if article.get('description'):
                md += f"**Description:** {article['description']}\n\n"

            md += f"**URL:** {article.get('url', 'N/A')}\n\n"
            md += "---\n\n"

        return md


class WikipediaFormatter(SearchResultFormatter):
    """Format Wikipedia search results for LLMs."""

    @staticmethod
    def format_results(results: List[Dict], query: Optional[str] = None) -> str:
        """Format Wikipedia search results as markdown."""
        if not results:
            return "No Wikipedia articles found."

        md = "# Wikipedia Search Results\n\n"
        if query:
            md += f"**Query:** {query}\n\n"
        md += f"**Total Results:** {len(results)}\n\n"
        md += "---\n\n"

        for i, article in enumerate(results, 1):
            md += f"## {i}. {article.get('title', 'N/A')}\n\n"

            snippet = article.get('snippet', '')
            if snippet:
                # Clean HTML tags from snippet
                import re
                clean_snippet = re.sub(r'<[^>]+>', '', snippet)
                md += f"**Snippet:** {clean_snippet}\n\n"

            md += f"**URL:** {article.get('url', 'N/A')}\n\n"
            md += "---\n\n"

        return md

    @staticmethod
    def format_page_summary(summary: Dict) -> str:
        """Format Wikipedia page summary as markdown."""
        if not summary:
            return "No summary available."

        md = f"# Wikipedia: {summary.get('title', 'N/A')}\n\n"
        md += f"{summary.get('summary', 'No summary available.')}\n\n"
        md += f"**URL:** {summary.get('url', 'N/A')}\n\n"

        return md


class DuckDuckGoFormatter(SearchResultFormatter):
    """Format DuckDuckGo search results for LLMs."""

    @staticmethod
    def format_results(results: List[Dict], query: Optional[str] = None) -> str:
        """Format DuckDuckGo search results as markdown."""
        if not results:
            return "No search results found."

        md = "# DuckDuckGo Search Results\n\n"
        if query:
            md += f"**Query:** {query}\n\n"
        md += f"**Total Results:** {len(results)}\n\n"
        md += "---\n\n"

        for i, result in enumerate(results, 1):
            md += f"## {i}. {result.get('title', 'N/A')}\n\n"

            if result.get('snippet'):
                md += f"{result['snippet']}\n\n"

            md += f"**URL:** {result.get('url', 'N/A')}\n\n"
            md += "---\n\n"

        return md


class GoogleFormatter(SearchResultFormatter):
    """Format Google search results for LLMs."""

    @staticmethod
    def format_results(results: List[Dict], query: Optional[str] = None) -> str:
        """Format Google search results as markdown."""
        if not results:
            return "No search results found."

        md = "# Google Search Results\n\n"
        if query:
            md += f"**Query:** {query}\n\n"
        md += f"**Total Results:** {len(results)}\n\n"
        md += "---\n\n"

        for i, result in enumerate(results, 1):
            md += f"## {i}. {result.get('title', 'N/A')}\n\n"

            if result.get('snippet'):
                md += f"{result['snippet']}\n\n"

            md += f"**URL:** {result.get('url', 'N/A')}\n\n"
            md += "---\n\n"

        return md


# Convenience functions for quick access
def format_arxiv_results(results: List[Dict], query: Optional[str] = None) -> str:
    """Quick access to format Arxiv results."""
    return ArxivFormatter.format_results(results, query)


def format_github_repos(results: Dict, query: Optional[str] = None) -> str:
    """Quick access to format GitHub repository results."""
    return GitHubFormatter.format_repository_results(results, query)


def format_stock_quote(quote: Dict) -> str:
    """Quick access to format stock quote."""
    return YahooFinanceFormatter.format_quote(quote)


def format_news(articles: List[Dict], query: Optional[str] = None) -> str:
    """Quick access to format news articles."""
    return FinancialNewsFormatter.format_results(articles, query)


# Export all formatters
__all__ = [
    'ArxivFormatter',
    'SemanticScholarFormatter',
    'PubMedFormatter',
    'CrossRefFormatter',
    'GitHubFormatter',
    'YahooFinanceFormatter',
    'AlphaVantageFormatter',
    'FinancialNewsFormatter',
    'WikipediaFormatter',
    'DuckDuckGoFormatter',
    'GoogleFormatter',
    'format_arxiv_results',
    'format_github_repos',
    'format_stock_quote',
    'format_news',
]
