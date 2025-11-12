# Search Tools for Language Agents

A comprehensive collection of search tools designed for language agents, providing free access to various search engines and academic databases.

## Features

- **Multiple Search Engines**: Arxiv, Semantic Scholar, PubMed, CrossRef, Google, Wikipedia, DuckDuckGo
- **Free APIs**: All tools use free APIs or web scraping (no paid subscriptions required)
- **Easy Integration**: Simple Python interface for each search tool
- **Rich Metadata**: Detailed results including titles, abstracts, citations, and more
- **Rate Limiting**: Built-in respect for API rate limits

## Installation

### Prerequisites

Python 3.8 or higher is required.

### Basic Installation

```bash
# Clone the repository
git clone <repository-url>
cd search_tools

# Install dependencies
pip install -r requirements.txt

# For Playwright (Google Search), install browsers
playwright install chromium
```

### Optional: API Keys

While all tools work without API keys, some offer higher rate limits with authentication:

- **Semantic Scholar**: Get an API key at https://www.semanticscholar.org/product/api
- **PubMed/NCBI**: Get an API key at https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/

## Quick Start

### Arxiv Search

Search for academic papers in physics, mathematics, computer science, and related fields.

```python
from search_tools import ArxivSearch

arxiv = ArxivSearch()

# Search by query
results = arxiv.search("quantum computing", max_results=5)
for paper in results:
    print(f"{paper['title']}")
    print(f"Authors: {', '.join(paper['authors'])}")
    print(f"Published: {paper['published']}")
    print(f"URL: {paper['id']}")
    print()

# Search by category
cs_ai_papers = arxiv.search_by_category("cs.AI", max_results=10)

# Get specific paper
paper = arxiv.get_paper_by_id("1706.03762")  # "Attention Is All You Need"
```

### Semantic Scholar Search

Search across multiple academic disciplines with citation information.

```python
from search_tools import SemanticScholarSearch

ss = SemanticScholarSearch()
# With API key for higher rate limits:
# ss = SemanticScholarSearch(api_key="your-api-key")

# Search for papers
results = ss.search("transformer neural networks", limit=5)
for paper in results:
    print(f"{paper['title']}")
    print(f"Citations: {paper.get('citationCount', 0)}")
    print(f"Year: {paper.get('year', 'N/A')}")
    print()

# Get paper by DOI
paper = ss.get_paper("DOI:10.1038/nature14539")

# Get citations of a paper
citations = ss.get_paper_citations("paper_id", limit=10)
```

### PubMed Search

Search biomedical and life sciences literature.

```python
from search_tools import PubMedSearch

pubmed = PubMedSearch()
# With API key: pubmed = PubMedSearch(api_key="your-key", email="your@email.com")

# Search for articles
results = pubmed.search("CRISPR gene editing", max_results=5)
for article in results:
    print(f"{article['title']}")
    print(f"Journal: {article['journal']}")
    print(f"PMID: {article['pmid']}")
    print()

# Search by author
author_papers = pubmed.search_by_author("Smith J", max_results=10)

# Get specific article
article = pubmed.get_article_by_pmid("12345678")
```

### CrossRef Search

Search for DOI-registered scholarly content.

```python
from search_tools import CrossRefSearch

crossref = CrossRefSearch(email="your@email.com")  # Email optional but recommended

# Search for publications
results = crossref.search("machine learning", rows=5)
for pub in results:
    title = pub.get('title', [''])[0]
    year = pub.get('published-print', {}).get('date-parts', [['']])[0][0]
    print(f"{title} ({year})")

# Get by DOI
pub = crossref.get_by_doi("10.1038/nature12373")

# Search by author
author_pubs = crossref.search_by_author("Einstein", rows=10)
```

### Google Search

General web search using Playwright (web scraping).

```python
from search_tools import GoogleSearch

# Use as context manager
with GoogleSearch() as google:
    # Regular search
    results = google.search("python programming", num_results=5)
    for result in results:
        print(f"{result['title']}")
        print(f"{result['url']}")
        print(f"{result['snippet']}")
        print()

    # News search
    news = google.search_news("artificial intelligence", num_results=5)

    # Image search
    images = google.search_images("quantum computer", num_results=10)
```

**Note**: Google search uses web scraping and may encounter rate limits or CAPTCHAs. Use responsibly.

### Wikipedia Search

Search Wikipedia articles and get content.

```python
from search_tools import WikipediaSearch

wiki = WikipediaSearch()
# For other languages: wiki = WikipediaSearch(language="fr")

# Search for articles
results = wiki.search("quantum computing", limit=5)
for article in results:
    print(f"{article['title']}")
    print(f"{article['snippet']}")
    print(f"{article['url']}")
    print()

# Get page content
page = wiki.get_page_content("Python (programming language)")
print(page['extract'])

# Get page summary
summary = wiki.get_page_summary("Machine learning")

# Get random pages
random_pages = wiki.get_random_pages(count=5)
```

### DuckDuckGo Search

Privacy-focused web search.

```python
from search_tools import DuckDuckGoSearch

ddg = DuckDuckGoSearch()

# Web search
results = ddg.search("python tutorials", max_results=5)
for result in results:
    print(f"{result['title']}")
    print(f"{result['url']}")
    print(f"{result['snippet']}")
    print()

# News search
news = ddg.search_news("climate change", max_results=5)

# Image search
images = ddg.search_images("mountains", max_results=10)

# Video search
videos = ddg.search_videos("python tutorial", max_results=5)

# Instant answer
answer = ddg.instant_answer("what is the capital of France")
if answer:
    print(answer['answer'])

# Search suggestions
suggestions = ddg.suggestions("python prog")
```

## Advanced Usage

### Pagination

Most tools support pagination for retrieving more results:

```python
# Arxiv
page1 = arxiv.search("quantum computing", max_results=10, start=0)
page2 = arxiv.search("quantum computing", max_results=10, start=10)

# Semantic Scholar
page1 = ss.search("AI", limit=10, offset=0)
page2 = ss.search("AI", limit=10, offset=10)

# CrossRef
page1 = crossref.search("machine learning", rows=10, offset=0)
page2 = crossref.search("machine learning", rows=10, offset=10)
```

### Filtering

Many tools support advanced filtering:

```python
# Semantic Scholar - filter by year and field
results = ss.search(
    "neural networks",
    limit=10,
    year="2020-2023",
    fields_of_study=["Computer Science"]
)

# PubMed - search with date range
results = pubmed.search(
    "cancer treatment",
    max_results=10,
    min_date="2020/01/01",
    max_date="2023/12/31"
)

# CrossRef - filter by type and date
results = crossref.search(
    "climate change",
    rows=10,
    filter_params={
        'type': 'journal-article',
        'from-pub-date': '2020-01-01',
        'has-abstract': 'true'
    }
)

# DuckDuckGo - time-limited search
results = ddg.search("AI news", max_results=10, timelimit="d")  # Last day
```

### Error Handling

All tools raise exceptions on errors. Use try-except blocks:

```python
from search_tools import ArxivSearch

arxiv = ArxivSearch()

try:
    results = arxiv.search("quantum computing")
    for paper in results:
        print(paper['title'])
except Exception as e:
    print(f"Search failed: {str(e)}")
```

## API Rate Limits

Be respectful of API rate limits:

- **Arxiv**: 1 request per second (built-in delay)
- **Semantic Scholar**: 1 request per second without API key, 10/sec with key
- **PubMed**: 3 requests per second without API key, 10/sec with key
- **CrossRef**: Up to 50 requests per second (polite pool with email)
- **Wikipedia**: No strict limit, but be reasonable
- **DuckDuckGo**: No strict limit, but may encounter rate limiting
- **Google**: Subject to detection and CAPTCHAs; use sparingly

## Use Cases for Language Agents

### Research Assistant

```python
def research_topic(topic, num_sources=5):
    """Gather information from multiple sources."""
    results = {
        'academic_papers': arxiv.search(topic, max_results=num_sources),
        'scholarly_articles': ss.search(topic, limit=num_sources),
        'encyclopedia': wiki.search(topic, limit=num_sources),
        'web_results': ddg.search(topic, max_results=num_sources)
    }
    return results
```

### Literature Review

```python
def find_papers_on_topic(topic, start_year=2020):
    """Find recent academic papers on a topic."""
    # Search multiple databases
    arxiv_results = arxiv.search(topic, max_results=20)
    ss_results = ss.search(topic, limit=20, year=f"{start_year}-2024")
    pubmed_results = pubmed.search(topic, max_results=20, min_date=f"{start_year}/01/01")

    # Combine and deduplicate
    all_papers = []
    # ... processing logic ...
    return all_papers
```

### Fact Checking

```python
def verify_claim(claim):
    """Verify a claim using multiple sources."""
    # Get instant answer
    answer = ddg.instant_answer(claim)

    # Search Wikipedia
    wiki_results = wiki.search(claim, limit=3)

    # Search academic sources
    academic = ss.search(claim, limit=5)

    return {
        'instant_answer': answer,
        'wikipedia': wiki_results,
        'academic': academic
    }
```

## Testing

Run the test suite:

```bash
pytest tests/
```

Run with coverage:

```bash
pytest --cov=search_tools tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- **Arxiv** for providing free access to scientific papers
- **Semantic Scholar** for AI-powered research tools
- **PubMed/NCBI** for biomedical literature access
- **CrossRef** for DOI metadata services
- **Wikipedia** for open knowledge
- **DuckDuckGo** for privacy-focused search

## Disclaimer

This tool is for educational and research purposes. When using web scraping features (Google Search), be respectful of the service provider's terms of service and rate limits. For production use, consider official APIs where available.

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.
