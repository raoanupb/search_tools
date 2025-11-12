"""
CrossRef Search Tool

Provides search capabilities for CrossRef, a DOI registration agency for scholarly
content. CrossRef provides metadata for millions of academic papers, books, and datasets.

API Documentation: https://api.crossref.org/swagger-ui/index.html
"""

import requests
from typing import List, Dict, Optional
import time


class CrossRefSearch:
    """
    Search tool for CrossRef metadata.

    Uses the free CrossRef REST API to search for academic publications.
    No API key required, but polite pool usage is recommended (provide email).
    """

    BASE_URL = "https://api.crossref.org"

    def __init__(self, email: Optional[str] = None):
        """
        Initialize the CrossRef search tool.

        Args:
            email: Optional email for polite pool (faster response times)
        """
        self.session = requests.Session()
        user_agent = 'SearchTools/0.1.0 (Language Agent Search Tool'
        if email:
            user_agent += f'; mailto:{email}'
        user_agent += ')'

        self.session.headers.update({
            'User-Agent': user_agent
        })

    def search(
        self,
        query: str,
        rows: int = 10,
        offset: int = 0,
        sort: str = "relevance",
        order: str = "desc",
        filter_params: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search CrossRef for publications matching the query.

        Args:
            query: Search query string
            rows: Number of results to return (default: 10, max: 1000)
            offset: Starting index for pagination (default: 0)
            sort: Sort field - 'relevance', 'score', 'updated', 'deposited', 'indexed', 'published'
            order: Sort order - 'asc' or 'desc'
            filter_params: Optional filters (e.g., {'type': 'journal-article', 'from-pub-date': '2020'})

        Returns:
            List of dictionaries containing publication information

        Example:
            >>> crossref = CrossRefSearch(email="your@email.com")
            >>> results = crossref.search("machine learning", rows=5)
            >>> for pub in results:
            ...     print(f"{pub['title'][0]} ({pub.get('published-print', {}).get('date-parts', [['']])[0][0]})")

        Common filters:
            - type: 'journal-article', 'book', 'proceedings-article', etc.
            - from-pub-date, until-pub-date: publication date range (YYYY-MM-DD)
            - has-abstract: 'true' or 'false'
            - has-full-text: 'true' or 'false'
        """
        params = {
            'query': query,
            'rows': min(rows, 1000),
            'offset': offset,
            'sort': sort,
            'order': order
        }

        # Add filters
        if filter_params:
            filter_str = ','.join([f"{k}:{v}" for k, v in filter_params.items()])
            params['filter'] = filter_str

        try:
            response = self.session.get(
                f"{self.BASE_URL}/works",
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            items = data.get('message', {}).get('items', [])

            # Be polite - rate limit to ~50 requests per second max
            time.sleep(0.02)

            return items

        except requests.RequestException as e:
            raise Exception(f"CrossRef API request failed: {str(e)}")

    def get_by_doi(self, doi: str) -> Optional[Dict]:
        """
        Get publication metadata by DOI.

        Args:
            doi: Digital Object Identifier

        Returns:
            Dictionary containing publication information, or None if not found

        Example:
            >>> crossref = CrossRefSearch()
            >>> pub = crossref.get_by_doi("10.1038/nature12373")
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/works/{doi}",
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            time.sleep(0.02)

            return data.get('message')

        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise Exception(f"CrossRef API request failed: {str(e)}")
        except requests.RequestException as e:
            raise Exception(f"CrossRef API request failed: {str(e)}")

    def search_by_author(self, author: str, rows: int = 10) -> List[Dict]:
        """
        Search for publications by author name.

        Args:
            author: Author name
            rows: Number of results to return

        Returns:
            List of dictionaries containing publication information
        """
        params = {
            'query.author': author,
            'rows': min(rows, 1000)
        }

        try:
            response = self.session.get(
                f"{self.BASE_URL}/works",
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            items = data.get('message', {}).get('items', [])

            time.sleep(0.02)

            return items

        except requests.RequestException as e:
            raise Exception(f"CrossRef API request failed: {str(e)}")

    def search_by_title(self, title: str, rows: int = 10) -> List[Dict]:
        """
        Search for publications by title.

        Args:
            title: Publication title
            rows: Number of results to return

        Returns:
            List of dictionaries containing publication information
        """
        params = {
            'query.title': title,
            'rows': min(rows, 1000)
        }

        try:
            response = self.session.get(
                f"{self.BASE_URL}/works",
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            items = data.get('message', {}).get('items', [])

            time.sleep(0.02)

            return items

        except requests.RequestException as e:
            raise Exception(f"CrossRef API request failed: {str(e)}")

    def search_journal(
        self,
        query: str,
        rows: int = 10
    ) -> List[Dict]:
        """
        Search for journals by name.

        Args:
            query: Journal name query
            rows: Number of results to return

        Returns:
            List of dictionaries containing journal information
        """
        params = {
            'query': query,
            'rows': min(rows, 1000)
        }

        try:
            response = self.session.get(
                f"{self.BASE_URL}/journals",
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            items = data.get('message', {}).get('items', [])

            time.sleep(0.02)

            return items

        except requests.RequestException as e:
            raise Exception(f"CrossRef API request failed: {str(e)}")

    def get_journal_works(
        self,
        issn: str,
        rows: int = 10,
        offset: int = 0
    ) -> List[Dict]:
        """
        Get publications from a specific journal by ISSN.

        Args:
            issn: Journal ISSN
            rows: Number of results to return
            offset: Starting index for pagination

        Returns:
            List of dictionaries containing publication information
        """
        params = {
            'rows': min(rows, 1000),
            'offset': offset
        }

        try:
            response = self.session.get(
                f"{self.BASE_URL}/journals/{issn}/works",
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            items = data.get('message', {}).get('items', [])

            time.sleep(0.02)

            return items

        except requests.RequestException as e:
            raise Exception(f"CrossRef API request failed: {str(e)}")

    def search_recent(
        self,
        query: str,
        days: int = 30,
        rows: int = 10
    ) -> List[Dict]:
        """
        Search for recent publications.

        Args:
            query: Search query
            days: Number of days to look back
            rows: Number of results to return

        Returns:
            List of dictionaries containing publication information
        """
        from datetime import datetime, timedelta

        date_threshold = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        filter_params = {
            'from-pub-date': date_threshold
        }

        return self.search(
            query,
            rows=rows,
            sort='published',
            order='desc',
            filter_params=filter_params
        )
