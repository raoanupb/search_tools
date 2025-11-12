"""
Semantic Scholar Search Tool

Provides search capabilities for Semantic Scholar, a free, AI-powered research tool
for scientific literature.

API Documentation: https://api.semanticscholar.org/
"""

import requests
from typing import List, Dict, Optional
import time


class SemanticScholarSearch:
    """
    Search tool for Semantic Scholar.

    Uses the free Semantic Scholar API to search for academic papers.
    No API key required (though rate limits apply).
    """

    BASE_URL = "https://api.semanticscholar.org/graph/v1"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Semantic Scholar search tool.

        Args:
            api_key: Optional API key for higher rate limits
        """
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SearchTools/0.1.0 (Language Agent Search Tool)'
        })
        if api_key:
            self.session.headers.update({'x-api-key': api_key})

    def search(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0,
        fields: Optional[List[str]] = None,
        year: Optional[str] = None,
        venue: Optional[str] = None,
        fields_of_study: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Search Semantic Scholar for papers matching the query.

        Args:
            query: Search query string
            limit: Maximum number of results to return (default: 10, max: 100)
            offset: Starting index for pagination (default: 0)
            fields: List of fields to include in response (e.g., ['title', 'authors', 'abstract'])
            year: Filter by publication year (e.g., '2020', '2019-2021')
            venue: Filter by publication venue
            fields_of_study: Filter by field of study (e.g., ['Computer Science', 'Medicine'])

        Returns:
            List of dictionaries containing paper information

        Example:
            >>> ss = SemanticScholarSearch()
            >>> results = ss.search("transformer neural networks", limit=5)
            >>> for paper in results:
            ...     print(f"{paper['title']}")
        """
        if fields is None:
            fields = [
                'paperId', 'title', 'abstract', 'year', 'authors',
                'citationCount', 'referenceCount', 'venue', 'publicationVenue',
                'fieldsOfStudy', 'url', 'openAccessPdf'
            ]

        params = {
            'query': query,
            'limit': min(limit, 100),  # API max is 100
            'offset': offset,
            'fields': ','.join(fields)
        }

        if year:
            params['year'] = year
        if venue:
            params['venue'] = venue
        if fields_of_study:
            params['fieldsOfStudy'] = ','.join(fields_of_study)

        try:
            response = self.session.get(
                f"{self.BASE_URL}/paper/search",
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()

            # Be respectful with rate limiting (public API: 1 request per second)
            time.sleep(1)

            return data.get('data', [])

        except requests.RequestException as e:
            raise Exception(f"Semantic Scholar API request failed: {str(e)}")

    def get_paper(self, paper_id: str, fields: Optional[List[str]] = None) -> Optional[Dict]:
        """
        Get details of a specific paper by ID.

        Args:
            paper_id: Semantic Scholar paper ID, DOI, arXiv ID, or other identifier
            fields: List of fields to include in response

        Returns:
            Dictionary containing paper information, or None if not found

        Example:
            >>> ss = SemanticScholarSearch()
            >>> paper = ss.get_paper('DOI:10.1038/nature14539')
        """
        if fields is None:
            fields = [
                'paperId', 'title', 'abstract', 'year', 'authors',
                'citationCount', 'referenceCount', 'venue', 'publicationVenue',
                'fieldsOfStudy', 'url', 'openAccessPdf', 'citations', 'references'
            ]

        params = {'fields': ','.join(fields)}

        try:
            response = self.session.get(
                f"{self.BASE_URL}/paper/{paper_id}",
                params=params,
                timeout=30
            )
            response.raise_for_status()

            time.sleep(1)

            return response.json()

        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise Exception(f"Semantic Scholar API request failed: {str(e)}")
        except requests.RequestException as e:
            raise Exception(f"Semantic Scholar API request failed: {str(e)}")

    def get_author(self, author_id: str, fields: Optional[List[str]] = None) -> Optional[Dict]:
        """
        Get details of a specific author by ID.

        Args:
            author_id: Semantic Scholar author ID
            fields: List of fields to include in response

        Returns:
            Dictionary containing author information, or None if not found
        """
        if fields is None:
            fields = [
                'authorId', 'name', 'url', 'affiliations',
                'homepage', 'paperCount', 'citationCount', 'hIndex'
            ]

        params = {'fields': ','.join(fields)}

        try:
            response = self.session.get(
                f"{self.BASE_URL}/author/{author_id}",
                params=params,
                timeout=30
            )
            response.raise_for_status()

            time.sleep(1)

            return response.json()

        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise Exception(f"Semantic Scholar API request failed: {str(e)}")
        except requests.RequestException as e:
            raise Exception(f"Semantic Scholar API request failed: {str(e)}")

    def search_authors(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for authors by name.

        Args:
            query: Author name query
            limit: Maximum number of results to return

        Returns:
            List of dictionaries containing author information
        """
        params = {
            'query': query,
            'limit': min(limit, 100)
        }

        try:
            response = self.session.get(
                f"{self.BASE_URL}/author/search",
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            time.sleep(1)

            return data.get('data', [])

        except requests.RequestException as e:
            raise Exception(f"Semantic Scholar API request failed: {str(e)}")

    def get_paper_citations(
        self,
        paper_id: str,
        limit: int = 10,
        offset: int = 0
    ) -> List[Dict]:
        """
        Get papers that cite the specified paper.

        Args:
            paper_id: Semantic Scholar paper ID
            limit: Maximum number of results to return
            offset: Starting index for pagination

        Returns:
            List of dictionaries containing citation information
        """
        params = {
            'limit': min(limit, 100),
            'offset': offset,
            'fields': 'paperId,title,year,authors,citationCount'
        }

        try:
            response = self.session.get(
                f"{self.BASE_URL}/paper/{paper_id}/citations",
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            time.sleep(1)

            return data.get('data', [])

        except requests.RequestException as e:
            raise Exception(f"Semantic Scholar API request failed: {str(e)}")

    def get_paper_references(
        self,
        paper_id: str,
        limit: int = 10,
        offset: int = 0
    ) -> List[Dict]:
        """
        Get papers referenced by the specified paper.

        Args:
            paper_id: Semantic Scholar paper ID
            limit: Maximum number of results to return
            offset: Starting index for pagination

        Returns:
            List of dictionaries containing reference information
        """
        params = {
            'limit': min(limit, 100),
            'offset': offset,
            'fields': 'paperId,title,year,authors,citationCount'
        }

        try:
            response = self.session.get(
                f"{self.BASE_URL}/paper/{paper_id}/references",
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            time.sleep(1)

            return data.get('data', [])

        except requests.RequestException as e:
            raise Exception(f"Semantic Scholar API request failed: {str(e)}")
