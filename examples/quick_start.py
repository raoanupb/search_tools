"""
Quick Start Example

A simple script to get you started with search_tools.
"""

from search_tools import ArxivSearch, WikipediaSearch

def main():
    print("Search Tools - Quick Start")
    print("=" * 80)

    # Example 1: Search Arxiv
    print("\n1. Searching Arxiv for 'machine learning'...")
    arxiv = ArxivSearch()
    results = arxiv.search("machine learning", max_results=3)

    for i, paper in enumerate(results, 1):
        print(f"\n   {i}. {paper['title']}")
        print(f"      Authors: {', '.join(paper['authors'][:2])}")
        print(f"      Published: {paper['published'][:10]}")

    # Example 2: Search Wikipedia
    print("\n\n2. Searching Wikipedia for 'artificial intelligence'...")
    wiki = WikipediaSearch()
    results = wiki.search("artificial intelligence", limit=3)

    for i, article in enumerate(results, 1):
        print(f"\n   {i}. {article['title']}")
        print(f"      URL: {article['url']}")

    # Example 3: Get Wikipedia summary
    print("\n\n3. Getting Wikipedia summary for 'Python (programming language)'...")
    summary = wiki.get_page_summary("Python (programming language)")

    if summary:
        print(f"\n   Title: {summary['title']}")
        print(f"   Summary: {summary['summary'][:200]}...")

    print("\n" + "=" * 80)
    print("Quick start complete!")
    print("\nFor more examples, see:")
    print("  - examples/basic_usage.py")
    print("  - examples/research_assistant.py")
    print("\nFor documentation, see README.md")
    print("=" * 80)


if __name__ == "__main__":
    main()
