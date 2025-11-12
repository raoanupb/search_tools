"""
Search Tools - A collection of search tools for language agents.

This package provides various search capabilities including:
- Arxiv: Academic papers in physics, mathematics, computer science
- Semantic Scholar: Multi-disciplinary academic search
- PubMed: Biomedical and life sciences literature
- CrossRef: DOI-based academic paper search
- GitHub: Code and repository search
- Google: General web search
- Wikipedia: Encyclopedia search
- DuckDuckGo: Privacy-focused web search
"""

# Import core tools (no optional dependencies)
from .arxiv_search import ArxivSearch
from .semantic_scholar_search import SemanticScholarSearch
from .pubmed_search import PubMedSearch
from .crossref_search import CrossRefSearch
from .wikipedia_search import WikipediaSearch
from .github_search import GitHubSearch

# Import tools with optional dependencies
__all__ = [
    'ArxivSearch',
    'SemanticScholarSearch',
    'PubMedSearch',
    'CrossRefSearch',
    'WikipediaSearch',
    'GitHubSearch',
]

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
