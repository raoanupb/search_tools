# Search Tools for Language Agents

A comprehensive collection of search tools designed for language agents, providing free access to various search engines and academic databases.

## Features

- **Academic Search**: Arxiv, Semantic Scholar, PubMed, CrossRef
- **Code Search**: GitHub (with popularity ranking)
- **Financial/Stock Market**: Yahoo Finance, Alpha Vantage, Financial News
- **General Search**: Google, Wikipedia, DuckDuckGo
- **Free APIs**: All tools use free APIs or web scraping (no paid subscriptions required)
- **Easy Integration**: Simple Python interface for each search tool
- **Rich Metadata**: Detailed results including titles, abstracts, citations, financial metrics, and more
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
- **GitHub**: Get a personal access token at https://github.com/settings/tokens (recommended for higher rate limits)
- **Alpha Vantage**: Get a free API key at https://www.alphavantage.co/support/#api-key (required for Alpha Vantage)
- **NewsAPI**: Get a free API key at https://newsapi.org/register (optional for financial news)

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

### GitHub Search

Search for code, repositories, issues, and users on GitHub with popularity ranking.

```python
from search_tools import GitHubSearch

# Initialize (optionally with token for higher rate limits)
github = GitHubSearch()
# With token: github = GitHubSearch(token="your-github-token")

# Search repositories (ranked by stars by default)
results = github.search_repositories(
    "machine learning",
    language="python",
    min_stars=1000,
    sort="stars",
    per_page=10
)

for repo in results['items']:
    print(f"{repo['full_name']} - ⭐ {repo['stars']:,}")
    print(f"  {repo['description']}")
    print(f"  Language: {repo['language']}, Forks: {repo['forks']:,}")
    print(f"  {repo['url']}")
    print()

# Search code
code_results = github.search_code(
    "def transformer",
    language="python",
    extension="py"
)

for item in code_results['items']:
    repo = item['repository']
    print(f"{repo['full_name']}/{item['path']}")
    print(f"  Stars: {repo['stars']:,}, Language: {repo['language']}")
    print(f"  {item['url']}")

# Get trending repositories
trending = github.get_trending_repositories(language="python", since="weekly")

for repo in trending[:5]:
    print(f"{repo['full_name']} - ⭐ {repo['stars']:,}")

# Search issues (great for finding "good first issue" tasks)
issues = github.search_issues(
    "bug",
    state="open",
    labels=["good first issue"],
    sort="created"
)

for issue in issues['items']:
    print(f"#{issue['number']}: {issue['title']}")
    print(f"  Labels: {', '.join(issue['labels'])}")
    print(f"  {issue['url']}")

# Search users
users = github.search_users("machine learning", min_followers=1000)

for user in users['items']:
    print(f"{user['login']} - {user['followers']:,} followers")
    print(f"  {user['url']}")

# Get specific repository details
repo_details = github.get_repository("huggingface", "transformers")
print(f"Stars: {repo_details['stars']:,}")
print(f"Forks: {repo_details['forks']:,}")
print(f"Topics: {', '.join(repo_details['topics'])}")

# Check rate limit
rate_limit = github.get_rate_limit()
print(f"Remaining: {rate_limit['resources']['search']['remaining']}")
```

**Rate Limits:**
- Unauthenticated: 60 requests/hour
- Authenticated: 5000 requests/hour
- Code search: 10 requests/minute (regardless of authentication)

**Popularity Ranking**: All search methods support sorting by stars, forks, and other metrics to find the most popular results.

### Yahoo Finance Search

Search for stock market data, company information, and financial metrics.

```python
from search_tools import YahooFinanceSearch

yf = YahooFinanceSearch()

# Get real-time stock quote
quote = yf.get_quote("AAPL")
print(f"${quote['current_price']} ({quote['change_percent']:+.2f}%)")
print(f"Volume: {quote['volume']:,}")
print(f"Market Cap: ${quote['market_cap']:,}")

# Get historical data
history = yf.get_historical_data("AAPL", period="1mo")
for day in history[-5:]:
    print(f"{day['date']}: ${day['close']}")

# Get detailed company information
info = yf.get_company_info("AAPL")
print(f"{info['name']} - {info['sector']}")
print(f"P/E Ratio: {info['pe_ratio']}")
print(f"Dividend Yield: {info['dividend_yield']}")
print(f"Description: {info['description'][:200]}...")

# Get financial statements
financials = yf.get_financial_statements("AAPL")
# Returns income statement, balance sheet, cash flow

# Get analyst recommendations
recommendations = yf.get_recommendations("AAPL")
for rec in recommendations[-5:]:
    print(f"{rec['date']}: {rec['firm']} - {rec['to_grade']}")

# Compare multiple stocks
comparison = yf.compare_stocks(['AAPL', 'MSFT', 'GOOGL'])
for stock in comparison:
    print(f"{stock['symbol']}: ${stock['current_price']} (PE: {stock['pe_ratio']})")

# Get trending/most active stocks
trending = yf.get_trending_stocks()
for stock in trending[:10]:
    print(f"{stock['symbol']}: ${stock['current_price']} - Vol: {stock['volume']:,}")
```

**No API key required** - Uses free Yahoo Finance data via yfinance library.

### Alpha Vantage Search

Advanced financial data, technical indicators, and fundamental analysis.

```python
from search_tools import AlphaVantageSearch

# Initialize with API key (get free at https://www.alphavantage.co/support/#api-key)
av = AlphaVantageSearch(api_key="your-api-key")

# Search for stock symbols
results = av.search_symbols("Tesla")
for match in results:
    print(f"{match['symbol']}: {match['name']} ({match['region']})")

# Get real-time quote
quote = av.get_quote("TSLA")
print(f"${quote['price']} ({quote['change_percent']}%)")

# Get intraday data (5-minute intervals)
intraday = av.get_intraday_data("TSLA", interval="5min")
for datapoint in intraday[:10]:
    print(f"{datapoint['timestamp']}: ${datapoint['close']}")

# Get daily historical data
daily = av.get_daily_data("TSLA", outputsize="compact")

# Technical indicators - Simple Moving Average (SMA)
sma = av.get_sma("TSLA", interval="daily", time_period=20)
print(f"20-day SMA: ${sma[0]['sma']}")

# Technical indicators - RSI
rsi = av.get_rsi("TSLA", interval="daily", time_period=14)
print(f"RSI: {rsi[0]['rsi']}")

# Company overview and fundamentals
overview = av.get_company_overview("TSLA")
print(f"{overview['name']} - {overview['sector']}")
print(f"Market Cap: ${overview['market_cap']:,}")
print(f"P/E Ratio: {overview['pe_ratio']}")
print(f"EPS: ${overview['eps']}")
print(f"Profit Margin: {overview['profit_margin']}")

# Earnings data
earnings = av.get_earnings("TSLA")
for q in earnings['quarterly'][:4]:
    print(f"Q{q['fiscal_quarter']}: EPS ${q['reported_eps']}")

# News and sentiment analysis
news = av.get_news_sentiment(tickers="TSLA", limit=10)
for article in news:
    print(f"{article['title']}")
    print(f"  Sentiment: {article['sentiment']} ({article['sentiment_score']})")
    print(f"  Source: {article['source']}")
```

**Free API key required** - 5 calls/minute, 500 calls/day on free tier.

### Financial News Search

Search financial news from multiple sources.

```python
from search_tools import FinancialNewsSearch

# Initialize with NewsAPI key (optional but recommended)
news = FinancialNewsSearch(newsapi_key="your-newsapi-key")

# Search for company-specific news
apple_news = news.search_company_news("Apple Inc", days=7)
for article in apple_news:
    print(f"{article['title']}")
    print(f"  Source: {article['source']}")
    print(f"  Published: {article['published_at']}")
    print(f"  {article['url']}")

# Get top business headlines
headlines = news.get_top_headlines(category="business")
for article in headlines:
    print(f"{article['title']} - {article['source']}")

# Search market news
market_news = news.search_market_news("stock market", days=1)

# Search earnings news
earnings_news = news.search_earnings_news(days=7)

# Search cryptocurrency news
crypto_news = news.search_crypto_news("Bitcoin", days=3)

# Search by specific source
reuters = news.search_by_source("Reuters", query="tech stocks", days=7)

# Get list of financial news sources
sources = news.get_financial_sources()
print(f"Available sources: {', '.join(sources)}")

# General news search with filters
results = news.search_news(
    query="Federal Reserve interest rates",
    from_date="2024-01-01",
    sort_by="publishedAt",
    page_size=20
)
```

**Optional API key** - NewsAPI free tier: 100 requests/day.

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
- **GitHub**: 60 requests/hour without token, 5000/hour with token; code search limited to 10/min
- **Yahoo Finance**: No strict API limit (uses yfinance library)
- **Alpha Vantage**: 5 requests per minute, 500 requests per day (free tier)
- **Financial News (NewsAPI)**: 100 requests per day (free tier)
- **Wikipedia**: No strict limit, but be reasonable
- **DuckDuckGo**: No strict limit, but may encounter rate limiting
- **Google**: Subject to detection and CAPTCHAs; use sparingly

## LLM Formatters - Convert Results to Markdown

All search tools include corresponding formatters to convert search results into LLM-friendly markdown format. This makes it easy to inject search results into prompts for context-aware AI responses.

### Quick Start with Formatters

```python
from search_tools import ArxivSearch, ArxivFormatter

# Search for papers
arxiv = ArxivSearch()
results = arxiv.search("large language models", max_results=5)

# Convert to markdown for LLM prompts
markdown = ArxivFormatter.format_results(results, query="large language models")

# Use in LLM prompt
llm_prompt = f"""Based on the following research papers:

{markdown}

Summarize the key findings about large language models."""
```

### Available Formatters

All formatters convert search results to well-structured markdown:

- **ArxivFormatter** - Academic papers with authors, abstracts, categories
- **SemanticScholarFormatter** - Papers with citation counts
- **PubMedFormatter** - Medical articles with abstracts and keywords
- **CrossRefFormatter** - Publications with DOIs
- **GitHubFormatter** - Repositories and code with star rankings
- **YahooFinanceFormatter** - Stock quotes, company info, comparisons
- **AlphaVantageFormatter** - Financial data and news sentiment
- **FinancialNewsFormatter** - News articles with sources
- **WikipediaFormatter** - Articles and summaries
- **DuckDuckGoFormatter** - Search results
- **GoogleFormatter** - Search results

### Formatter Examples

```python
from search_tools import (
    GitHubSearch,
    GitHubFormatter,
    YahooFinanceSearch,
    YahooFinanceFormatter,
)

# GitHub repositories
github = GitHubSearch()
repos = github.search_repositories("machine learning", language="python", per_page=5)
markdown = GitHubFormatter.format_repository_results(repos)

# Stock market data
yf = YahooFinanceSearch()
quote = yf.get_quote("AAPL")
markdown = YahooFinanceFormatter.format_quote(quote)

# Company comparison
comparison = yf.compare_stocks(['AAPL', 'MSFT', 'GOOGL'])
markdown = YahooFinanceFormatter.format_comparison(comparison)
```

### Convenience Functions

Quick access functions for common formatters:

```python
from search_tools import (
    format_arxiv_results,
    format_github_repos,
    format_stock_quote,
    format_news,
)

# Use convenience functions
papers_md = format_arxiv_results(papers, query="AI")
repos_md = format_github_repos(repo_results, query="ML")
quote_md = format_stock_quote(stock_quote)
news_md = format_news(articles, query="tech")
```

### Multi-Source Agent Workflow

Combine multiple sources for comprehensive LLM context:

```python
from search_tools import (
    ArxivSearch, ArxivFormatter,
    GitHubSearch, GitHubFormatter,
    WikipediaSearch, WikipediaFormatter,
)

topic = "quantum computing"

# Gather from multiple sources
arxiv = ArxivSearch()
github = GitHubSearch()
wiki = WikipediaSearch()

papers = arxiv.search(topic, max_results=3)
repos = github.search_repositories(topic, language="python", per_page=3)
articles = wiki.search(topic, limit=2)

# Format everything
papers_md = ArxivFormatter.format_results(papers, query=topic)
repos_md = GitHubFormatter.format_repository_results(repos, query=topic)
wiki_md = WikipediaFormatter.format_results(articles, query=topic)

# Create comprehensive prompt
llm_prompt = f"""# Research on {topic}

## Academic Papers
{papers_md}

## Code Repositories
{repos_md}

## Background Knowledge
{wiki_md}

Based on this information, provide a comprehensive overview of {topic}."""
```

See `examples/llm_formatter_examples.py` for more detailed examples.

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
