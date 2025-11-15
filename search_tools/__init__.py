"""
Search Tools - A collection of search tools for language agents.

This package provides various search capabilities including:
- Arxiv: Academic papers in physics, mathematics, computer science
- Semantic Scholar: Multi-disciplinary academic search
- PubMed: Biomedical and life sciences literature
- CrossRef: DOI-based academic paper search
- GitHub: Code and repository search
- Yahoo Finance: Stock market data and company information
- Alpha Vantage: Advanced financial data and technical indicators
- Financial News: Financial news from multiple sources
- Google: General web search
- Wikipedia: Encyclopedia search
- DuckDuckGo: Privacy-focused web search

Also includes LLM formatters to convert search results to markdown for prompt injection.
"""

# Import core tools (no optional dependencies)
from .arxiv_search import ArxivSearch
from .semantic_scholar_search import SemanticScholarSearch
from .pubmed_search import PubMedSearch
from .crossref_search import CrossRefSearch
from .wikipedia_search import WikipediaSearch
from .github_search import GitHubSearch
from .alpha_vantage_search import AlphaVantageSearch
from .financial_news_search import FinancialNewsSearch

# Import formatters
from .formatters import (
    ArxivFormatter,
    SemanticScholarFormatter,
    PubMedFormatter,
    CrossRefFormatter,
    GitHubFormatter,
    YahooFinanceFormatter,
    AlphaVantageFormatter,
    FinancialNewsFormatter,
    WikipediaFormatter,
    DuckDuckGoFormatter,
    GoogleFormatter,
    format_arxiv_results,
    format_github_repos,
    format_stock_quote,
    format_news,
)

# Import tools with optional dependencies
__all__ = [
    # Search tools
    'ArxivSearch',
    'SemanticScholarSearch',
    'PubMedSearch',
    'CrossRefSearch',
    'WikipediaSearch',
    'GitHubSearch',
    'AlphaVantageSearch',
    'FinancialNewsSearch',
    # Formatters
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
    # Convenience functions
    'format_arxiv_results',
    'format_github_repos',
    'format_stock_quote',
    'format_news',
]

# Try to import YahooFinanceSearch (requires yfinance)
try:
    from .yahoo_finance_search import YahooFinanceSearch
    __all__.append('YahooFinanceSearch')
except ImportError:
    pass

# Try to import GoogleSearch (requires playwright)
try:
    from .google_search import GoogleSearch
    __all__.append('GoogleSearch')
except ImportError:
    pass

# Try to import DuckDuckGoSearch (requires duckduckgo-search)
try:
    from .duckduckgo_search import DuckDuckGoSearch
    __all__.append('DuckDuckGoSearch')
except ImportError:
    pass

__version__ = '0.1.0'
