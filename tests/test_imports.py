"""
Test basic imports and initialization of all search tools.
"""

import pytest


def test_arxiv_import():
    """Test that ArxivSearch can be imported and initialized."""
    from search_tools import ArxivSearch
    arxiv = ArxivSearch()
    assert arxiv is not None


def test_semantic_scholar_import():
    """Test that SemanticScholarSearch can be imported and initialized."""
    from search_tools import SemanticScholarSearch
    ss = SemanticScholarSearch()
    assert ss is not None


def test_pubmed_import():
    """Test that PubMedSearch can be imported and initialized."""
    from search_tools import PubMedSearch
    pubmed = PubMedSearch()
    assert pubmed is not None


def test_crossref_import():
    """Test that CrossRefSearch can be imported and initialized."""
    from search_tools import CrossRefSearch
    crossref = CrossRefSearch()
    assert crossref is not None


def test_wikipedia_import():
    """Test that WikipediaSearch can be imported and initialized."""
    from search_tools import WikipediaSearch
    wiki = WikipediaSearch()
    assert wiki is not None


def test_duckduckgo_import():
    """Test that DuckDuckGoSearch can be imported and initialized."""
    try:
        from search_tools import DuckDuckGoSearch
        ddg = DuckDuckGoSearch()
        assert ddg is not None
    except ImportError:
        pytest.skip("duckduckgo_search library not installed")


def test_google_import():
    """Test that GoogleSearch can be imported."""
    from search_tools import GoogleSearch
    # Don't initialize browser in tests
    assert GoogleSearch is not None


def test_package_version():
    """Test that package version is defined."""
    import search_tools
    assert hasattr(search_tools, '__version__')
    assert search_tools.__version__ == '0.1.0'


def test_all_exports():
    """Test that __all__ exports are correct."""
    import search_tools
    expected_exports = [
        'ArxivSearch',
        'SemanticScholarSearch',
        'PubMedSearch',
        'CrossRefSearch',
        'GoogleSearch',
        'WikipediaSearch',
        'DuckDuckGoSearch',
    ]
    assert hasattr(search_tools, '__all__')
    assert set(search_tools.__all__) == set(expected_exports)
