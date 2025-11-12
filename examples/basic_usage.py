"""
Basic usage examples for all search tools.

This script demonstrates the basic functionality of each search tool.
"""

from search_tools import (
    ArxivSearch,
    SemanticScholarSearch,
    PubMedSearch,
    CrossRefSearch,
    GoogleSearch,
    WikipediaSearch,
    DuckDuckGoSearch
)


def demo_arxiv():
    """Demonstrate Arxiv search."""
    print("=" * 80)
    print("ARXIV SEARCH DEMO")
    print("=" * 80)

    arxiv = ArxivSearch()

    # Basic search
    print("\nSearching for 'transformer neural networks'...")
    results = arxiv.search("transformer neural networks", max_results=3)

    for i, paper in enumerate(results, 1):
        print(f"\n{i}. {paper['title']}")
        print(f"   Authors: {', '.join(paper['authors'][:3])}")
        if len(paper['authors']) > 3:
            print(f"   ... and {len(paper['authors']) - 3} more")
        print(f"   Published: {paper['published']}")
        print(f"   Categories: {', '.join(paper['categories'][:3])}")
        print(f"   URL: {paper['id']}")


def demo_semantic_scholar():
    """Demonstrate Semantic Scholar search."""
    print("\n" + "=" * 80)
    print("SEMANTIC SCHOLAR SEARCH DEMO")
    print("=" * 80)

    ss = SemanticScholarSearch()

    # Basic search
    print("\nSearching for 'deep learning'...")
    results = ss.search("deep learning", limit=3)

    for i, paper in enumerate(results, 1):
        print(f"\n{i}. {paper.get('title', 'N/A')}")
        authors = paper.get('authors', [])
        if authors:
            author_names = [a.get('name', 'Unknown') for a in authors[:3]]
            print(f"   Authors: {', '.join(author_names)}")
        print(f"   Year: {paper.get('year', 'N/A')}")
        print(f"   Citations: {paper.get('citationCount', 0)}")
        print(f"   URL: {paper.get('url', 'N/A')}")


def demo_pubmed():
    """Demonstrate PubMed search."""
    print("\n" + "=" * 80)
    print("PUBMED SEARCH DEMO")
    print("=" * 80)

    pubmed = PubMedSearch()

    # Basic search
    print("\nSearching for 'COVID-19 treatment'...")
    results = pubmed.search("COVID-19 treatment", max_results=3)

    for i, article in enumerate(results, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Authors: {', '.join(article['authors'][:3])}")
        if len(article['authors']) > 3:
            print(f"   ... and {len(article['authors']) - 3} more")
        print(f"   Journal: {article['journal']}")
        print(f"   Published: {article['publication_date']}")
        print(f"   PMID: {article['pmid']}")
        print(f"   URL: {article['url']}")


def demo_crossref():
    """Demonstrate CrossRef search."""
    print("\n" + "=" * 80)
    print("CROSSREF SEARCH DEMO")
    print("=" * 80)

    crossref = CrossRefSearch()

    # Basic search
    print("\nSearching for 'climate change'...")
    results = crossref.search("climate change", rows=3)

    for i, pub in enumerate(results, 1):
        title = pub.get('title', ['N/A'])[0] if pub.get('title') else 'N/A'
        authors = pub.get('author', [])
        year = pub.get('published-print', pub.get('published-online', {}))
        year = year.get('date-parts', [['']])[0][0] if year else 'N/A'

        print(f"\n{i}. {title}")
        if authors:
            author_names = [f"{a.get('given', '')} {a.get('family', '')}" for a in authors[:3]]
            print(f"   Authors: {', '.join(author_names)}")
        print(f"   Year: {year}")
        print(f"   DOI: {pub.get('DOI', 'N/A')}")


def demo_wikipedia():
    """Demonstrate Wikipedia search."""
    print("\n" + "=" * 80)
    print("WIKIPEDIA SEARCH DEMO")
    print("=" * 80)

    wiki = WikipediaSearch()

    # Basic search
    print("\nSearching for 'artificial intelligence'...")
    results = wiki.search("artificial intelligence", limit=3)

    for i, article in enumerate(results, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Snippet: {article['snippet'][:200]}...")
        print(f"   URL: {article['url']}")

    # Get page summary
    print("\nGetting summary for 'Machine Learning'...")
    summary = wiki.get_page_summary("Machine Learning")
    if summary:
        print(f"\n{summary['title']}")
        print(f"{summary['summary'][:300]}...")
        print(f"URL: {summary['url']}")


def demo_duckduckgo():
    """Demonstrate DuckDuckGo search."""
    print("\n" + "=" * 80)
    print("DUCKDUCKGO SEARCH DEMO")
    print("=" * 80)

    ddg = DuckDuckGoSearch()

    # Basic search
    print("\nSearching for 'Python programming'...")
    results = ddg.search("Python programming", max_results=3)

    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   Snippet: {result['snippet'][:200]}...")

    # Instant answer
    print("\nGetting instant answer for 'what is the speed of light'...")
    answer = ddg.instant_answer("what is the speed of light")
    if answer:
        print(f"\n{answer['answer']}")


def demo_google():
    """Demonstrate Google search."""
    print("\n" + "=" * 80)
    print("GOOGLE SEARCH DEMO")
    print("=" * 80)
    print("\nNote: Google search uses web scraping and may take longer.")
    print("It may also encounter rate limits or CAPTCHAs.\n")

    try:
        with GoogleSearch(headless=True) as google:
            # Basic search
            print("Searching for 'Python programming'...")
            results = google.search("Python programming", num_results=3)

            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['title']}")
                print(f"   URL: {result['url']}")
                print(f"   Snippet: {result['snippet'][:200]}...")
    except Exception as e:
        print(f"Google search failed: {str(e)}")
        print("This is expected if you're rate limited or encounter a CAPTCHA.")


def main():
    """Run all demos."""
    print("\n")
    print("*" * 80)
    print("SEARCH TOOLS DEMONSTRATION")
    print("*" * 80)
    print("\nThis script demonstrates basic usage of all search tools.")
    print("Some searches may take a few seconds due to rate limiting.\n")

    # Run demos (comment out any you don't want to run)
    demo_arxiv()
    demo_semantic_scholar()
    demo_pubmed()
    demo_crossref()
    demo_wikipedia()
    demo_duckduckgo()
    demo_google()  # May fail due to rate limiting

    print("\n" + "=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
