"""
Arxiv Search Tool

Provides search capabilities for arxiv.org, a repository of electronic preprints
in physics, mathematics, computer science, and related disciplines.

API Documentation: https://arxiv.org/help/api/
"""

import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
from urllib.parse import urlencode
import time


class ArxivSearch:
    """
    Search tool for Arxiv papers.

    Uses the free Arxiv API to search for academic papers.
    No API key required.
    """

    BASE_URL = "http://export.arxiv.org/api/query"

    def __init__(self):
        """Initialize the Arxiv search tool."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SearchTools/0.1.0 (Language Agent Search Tool)'
        })

    def search(
        self,
        query: str,
        max_results: int = 10,
        sort_by: str = "relevance",
        sort_order: str = "descending",
        start: int = 0
    ) -> List[Dict]:
        """
        Search Arxiv for papers matching the query.

        Args:
            query: Search query string (can use AND, OR, ANDNOT operators)
            max_results: Maximum number of results to return (default: 10)
            sort_by: Sort by 'relevance', 'lastUpdatedDate', or 'submittedDate'
            sort_order: 'ascending' or 'descending'
            start: Starting index for pagination (default: 0)

        Returns:
            List of dictionaries containing paper information

        Example:
            >>> arxiv = ArxivSearch()
            >>> results = arxiv.search("quantum computing", max_results=5)
            >>> for paper in results:
            ...     print(f"{paper['title']} by {paper['authors']}")
        """
        params = {
            'search_query': query,
            'start': start,
            'max_results': max_results,
            'sortBy': sort_by,
            'sortOrder': sort_order
        }

        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()

            # Parse the XML response
            results = self._parse_response(response.text)

            # Be respectful with rate limiting
            time.sleep(1)

            return results

        except requests.RequestException as e:
            raise Exception(f"Arxiv API request failed: {str(e)}")

    def search_by_category(
        self,
        category: str,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Search Arxiv papers by category.

        Args:
            category: Arxiv category code (e.g., 'cs.AI', 'math.CO', 'physics.quantum-ph')
            max_results: Maximum number of results to return

        Returns:
            List of dictionaries containing paper information

        Common categories:
            - cs.AI: Artificial Intelligence
            - cs.LG: Machine Learning
            - cs.CL: Computation and Language
            - math.CO: Combinatorics
            - physics.quantum-ph: Quantum Physics
        """
        query = f"cat:{category}"
        return self.search(query, max_results=max_results, sort_by="submittedDate")

    def search_by_author(
        self,
        author: str,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Search Arxiv papers by author name.

        Args:
            author: Author name
            max_results: Maximum number of results to return

        Returns:
            List of dictionaries containing paper information
        """
        query = f"au:{author}"
        return self.search(query, max_results=max_results)

    def get_paper_by_id(self, arxiv_id: str) -> Optional[Dict]:
        """
        Get a specific paper by its Arxiv ID.

        Args:
            arxiv_id: Arxiv paper ID (e.g., '1706.03762')

        Returns:
            Dictionary containing paper information, or None if not found
        """
        query = f"id:{arxiv_id}"
        results = self.search(query, max_results=1)
        return results[0] if results else None

    def _parse_response(self, xml_text: str) -> List[Dict]:
        """
        Parse the XML response from Arxiv API.

        Args:
            xml_text: XML response text

        Returns:
            List of parsed paper dictionaries
        """
        # Define namespaces
        namespaces = {
            'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }

        root = ET.fromstring(xml_text)
        entries = root.findall('atom:entry', namespaces)

        results = []
        for entry in entries:
            # Extract basic fields
            paper = {
                'id': self._get_text(entry, 'atom:id', namespaces),
                'title': self._get_text(entry, 'atom:title', namespaces).strip().replace('\n', ' '),
                'summary': self._get_text(entry, 'atom:summary', namespaces).strip().replace('\n', ' '),
                'published': self._get_text(entry, 'atom:published', namespaces),
                'updated': self._get_text(entry, 'atom:updated', namespaces),
                'authors': [],
                'categories': [],
                'links': {}
            }

            # Extract authors
            for author in entry.findall('atom:author', namespaces):
                name = self._get_text(author, 'atom:name', namespaces)
                if name:
                    paper['authors'].append(name)

            # Extract categories
            for category in entry.findall('atom:category', namespaces):
                term = category.get('term')
                if term:
                    paper['categories'].append(term)

            # Extract links
            for link in entry.findall('atom:link', namespaces):
                title = link.get('title', 'unknown')
                href = link.get('href')
                if href:
                    paper['links'][title] = href

            # Extract Arxiv-specific fields
            comment = entry.find('arxiv:comment', namespaces)
            if comment is not None and comment.text:
                paper['comment'] = comment.text

            primary_category = entry.find('arxiv:primary_category', namespaces)
            if primary_category is not None:
                paper['primary_category'] = primary_category.get('term')

            results.append(paper)

        return results

    def _get_text(self, element, path: str, namespaces: dict) -> str:
        """Helper method to safely extract text from XML element."""
        found = element.find(path, namespaces)
        return found.text if found is not None and found.text else ""
