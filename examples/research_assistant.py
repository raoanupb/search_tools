"""
Research Assistant Example

This example demonstrates how to use multiple search tools together
to build a research assistant that gathers information from various sources.
"""

from search_tools import (
    ArxivSearch,
    SemanticScholarSearch,
    WikipediaSearch,
    DuckDuckGoSearch
)
from typing import Dict, List
import json


class ResearchAssistant:
    """A research assistant that combines multiple search tools."""

    def __init__(self):
        """Initialize all search tools."""
        self.arxiv = ArxivSearch()
        self.semantic_scholar = SemanticScholarSearch()
        self.wikipedia = WikipediaSearch()
        self.duckduckgo = DuckDuckGoSearch()

    def research_topic(self, topic: str, num_results: int = 5) -> Dict:
        """
        Gather comprehensive information about a topic from multiple sources.

        Args:
            topic: The topic to research
            num_results: Number of results per source

        Returns:
            Dictionary containing results from all sources
        """
        print(f"Researching topic: {topic}")
        print("=" * 80)

        results = {
            'topic': topic,
            'sources': {}
        }

        # Search academic papers
        print("\nSearching Arxiv...")
        try:
            arxiv_results = self.arxiv.search(topic, max_results=num_results)
            results['sources']['arxiv'] = [
                {
                    'title': paper['title'],
                    'authors': paper['authors'],
                    'published': paper['published'],
                    'url': paper['id'],
                    'summary': paper['summary'][:300] + '...'
                }
                for paper in arxiv_results
            ]
            print(f"  Found {len(arxiv_results)} papers")
        except Exception as e:
            print(f"  Error: {str(e)}")
            results['sources']['arxiv'] = []

        # Search Semantic Scholar
        print("Searching Semantic Scholar...")
        try:
            ss_results = self.semantic_scholar.search(topic, limit=num_results)
            results['sources']['semantic_scholar'] = [
                {
                    'title': paper.get('title', 'N/A'),
                    'year': paper.get('year', 'N/A'),
                    'citations': paper.get('citationCount', 0),
                    'url': paper.get('url', 'N/A')
                }
                for paper in ss_results
            ]
            print(f"  Found {len(ss_results)} papers")
        except Exception as e:
            print(f"  Error: {str(e)}")
            results['sources']['semantic_scholar'] = []

        # Search Wikipedia
        print("Searching Wikipedia...")
        try:
            wiki_results = self.wikipedia.search(topic, limit=num_results)
            results['sources']['wikipedia'] = [
                {
                    'title': article['title'],
                    'snippet': article['snippet'],
                    'url': article['url']
                }
                for article in wiki_results
            ]
            print(f"  Found {len(wiki_results)} articles")
        except Exception as e:
            print(f"  Error: {str(e)}")
            results['sources']['wikipedia'] = []

        # Get Wikipedia summary if exact match exists
        print("Getting Wikipedia summary...")
        try:
            summary = self.wikipedia.get_page_summary(topic)
            if summary:
                results['wikipedia_summary'] = {
                    'title': summary['title'],
                    'summary': summary['summary'],
                    'url': summary['url']
                }
                print("  Found summary")
            else:
                print("  No exact match found")
        except Exception as e:
            print(f"  Error: {str(e)}")

        # Search web
        print("Searching web (DuckDuckGo)...")
        try:
            web_results = self.duckduckgo.search(topic, max_results=num_results)
            results['sources']['web'] = [
                {
                    'title': result['title'],
                    'url': result['url'],
                    'snippet': result['snippet']
                }
                for result in web_results
            ]
            print(f"  Found {len(web_results)} results")
        except Exception as e:
            print(f"  Error: {str(e)}")
            results['sources']['web'] = []

        # Get instant answer
        print("Looking for instant answer...")
        try:
            answer = self.duckduckgo.instant_answer(topic)
            if answer:
                results['instant_answer'] = answer
                print("  Found instant answer")
            else:
                print("  No instant answer available")
        except Exception as e:
            print(f"  Error: {str(e)}")

        return results

    def find_papers_by_author(self, author: str, max_results: int = 10) -> Dict:
        """
        Find papers by a specific author across multiple databases.

        Args:
            author: Author name
            max_results: Maximum results per database

        Returns:
            Dictionary containing papers from all sources
        """
        print(f"Finding papers by: {author}")
        print("=" * 80)

        results = {
            'author': author,
            'papers': {}
        }

        # Search Arxiv
        print("\nSearching Arxiv...")
        try:
            arxiv_papers = self.arxiv.search_by_author(author, max_results=max_results)
            results['papers']['arxiv'] = [
                {
                    'title': paper['title'],
                    'published': paper['published'],
                    'url': paper['id']
                }
                for paper in arxiv_papers
            ]
            print(f"  Found {len(arxiv_papers)} papers")
        except Exception as e:
            print(f"  Error: {str(e)}")
            results['papers']['arxiv'] = []

        return results

    def compare_papers(self, paper_id1: str, paper_id2: str) -> Dict:
        """
        Compare two papers from Semantic Scholar.

        Args:
            paper_id1: First paper ID
            paper_id2: Second paper ID

        Returns:
            Dictionary comparing the two papers
        """
        print(f"Comparing papers: {paper_id1} vs {paper_id2}")
        print("=" * 80)

        paper1 = self.semantic_scholar.get_paper(paper_id1)
        paper2 = self.semantic_scholar.get_paper(paper_id2)

        if not paper1 or not paper2:
            return {'error': 'One or both papers not found'}

        return {
            'paper1': {
                'title': paper1.get('title'),
                'year': paper1.get('year'),
                'citations': paper1.get('citationCount'),
                'references': paper1.get('referenceCount')
            },
            'paper2': {
                'title': paper2.get('title'),
                'year': paper2.get('year'),
                'citations': paper2.get('citationCount'),
                'references': paper2.get('referenceCount')
            }
        }

    def get_trending_topics(self, field: str = "cs.AI") -> List[Dict]:
        """
        Get trending topics by searching recent papers in a field.

        Args:
            field: Arxiv field/category

        Returns:
            List of recent papers
        """
        print(f"Getting trending papers in: {field}")
        print("=" * 80)

        try:
            papers = self.arxiv.search_by_category(field, max_results=10)
            return [
                {
                    'title': paper['title'],
                    'authors': paper['authors'][:3],
                    'published': paper['published'],
                    'url': paper['id']
                }
                for paper in papers
            ]
        except Exception as e:
            print(f"Error: {str(e)}")
            return []


def main():
    """Demonstrate the research assistant."""
    assistant = ResearchAssistant()

    # Example 1: Research a topic
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Research a Topic")
    print("=" * 80)

    results = assistant.research_topic("quantum computing", num_results=3)

    print("\n" + "=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)

    print(f"\nTopic: {results['topic']}")

    if 'instant_answer' in results:
        print(f"\nInstant Answer:")
        print(f"  {results['instant_answer']['answer']}")

    if 'wikipedia_summary' in results:
        print(f"\nWikipedia Summary:")
        print(f"  {results['wikipedia_summary']['summary'][:300]}...")

    for source, items in results['sources'].items():
        print(f"\n{source.upper()} ({len(items)} results):")
        for i, item in enumerate(items[:2], 1):  # Show first 2
            print(f"  {i}. {item.get('title', 'N/A')}")

    # Example 2: Find papers by author
    print("\n\n" + "=" * 80)
    print("EXAMPLE 2: Find Papers by Author")
    print("=" * 80)

    author_results = assistant.find_papers_by_author("LeCun", max_results=5)

    print("\n" + "=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    print(f"\nAuthor: {author_results['author']}")

    for source, papers in author_results['papers'].items():
        print(f"\n{source.upper()} ({len(papers)} papers):")
        for i, paper in enumerate(papers[:3], 1):  # Show first 3
            print(f"  {i}. {paper['title']}")

    # Example 3: Get trending topics
    print("\n\n" + "=" * 80)
    print("EXAMPLE 3: Trending Topics in AI")
    print("=" * 80)

    trending = assistant.get_trending_topics("cs.AI")

    print("\n" + "=" * 80)
    print("RECENT PAPERS")
    print("=" * 80)

    for i, paper in enumerate(trending[:5], 1):
        print(f"\n{i}. {paper['title']}")
        print(f"   Authors: {', '.join(paper['authors'])}")
        print(f"   Published: {paper['published']}")

    print("\n" + "=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
