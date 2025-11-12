"""
Wikipedia Search Tool

Provides search capabilities for Wikipedia using the MediaWiki API.

API Documentation: https://www.mediawiki.org/wiki/API:Main_page
"""

import requests
from typing import List, Dict, Optional
import time


class WikipediaSearch:
    """
    Search tool for Wikipedia.

    Uses the free MediaWiki API to search Wikipedia articles.
    No API key required.
    """

    def __init__(self, language: str = "en"):
        """
        Initialize the Wikipedia search tool.

        Args:
            language: Wikipedia language code (default: "en")
        """
        self.language = language
        self.base_url = f"https://{language}.wikipedia.org/w/api.php"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SearchTools/0.1.0 (Language Agent Search Tool)'
        })

    def search(
        self,
        query: str,
        limit: int = 10,
        search_type: str = "text"
    ) -> List[Dict]:
        """
        Search Wikipedia for articles matching the query.

        Args:
            query: Search query string
            limit: Maximum number of results to return (default: 10, max: 500)
            search_type: Type of search - 'text' (full text) or 'title' (title only)

        Returns:
            List of dictionaries containing article information

        Example:
            >>> wiki = WikipediaSearch()
            >>> results = wiki.search("quantum computing", limit=5)
            >>> for article in results:
            ...     print(f"{article['title']}: {article['snippet']}")
        """
        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': query,
            'srlimit': min(limit, 500),
            'format': 'json',
            'srinfo': 'totalhits',
            'srprop': 'size|wordcount|timestamp|snippet|titlesnippet'
        }

        if search_type == 'title':
            params['srwhat'] = 'title'

        try:
            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            search_results = data.get('query', {}).get('search', [])

            # Enrich results with page URLs
            results = []
            for result in search_results:
                results.append({
                    'pageid': result.get('pageid'),
                    'title': result.get('title', ''),
                    'snippet': self._clean_snippet(result.get('snippet', '')),
                    'size': result.get('size'),
                    'wordcount': result.get('wordcount'),
                    'timestamp': result.get('timestamp'),
                    'url': f"https://{self.language}.wikipedia.org/wiki/{result.get('title', '').replace(' ', '_')}"
                })

            time.sleep(0.1)  # Be respectful with rate limiting

            return results

        except requests.RequestException as e:
            raise Exception(f"Wikipedia search failed: {str(e)}")

    def get_page_content(
        self,
        title: str,
        extract_format: str = "plain"
    ) -> Optional[Dict]:
        """
        Get the content of a Wikipedia page by title.

        Args:
            title: Page title
            extract_format: Format of extract - 'plain' or 'html'

        Returns:
            Dictionary containing page content, or None if not found

        Example:
            >>> wiki = WikipediaSearch()
            >>> page = wiki.get_page_content("Python (programming language)")
            >>> print(page['extract'][:200])
        """
        params = {
            'action': 'query',
            'titles': title,
            'prop': 'extracts|info|pageprops',
            'exintro': True,  # Only get intro section
            'explaintext': extract_format == 'plain',
            'inprop': 'url',
            'format': 'json'
        }

        try:
            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            pages = data.get('query', {}).get('pages', {})

            if not pages:
                return None

            # Get the first (and only) page
            page_id = list(pages.keys())[0]
            if page_id == '-1':  # Page not found
                return None

            page = pages[page_id]
            time.sleep(0.1)

            return {
                'pageid': page.get('pageid'),
                'title': page.get('title'),
                'extract': page.get('extract', ''),
                'url': page.get('fullurl', ''),
                'categories': page.get('pageprops', {})
            }

        except requests.RequestException as e:
            raise Exception(f"Wikipedia page fetch failed: {str(e)}")

    def get_page_summary(self, title: str) -> Optional[Dict]:
        """
        Get a summary of a Wikipedia page.

        Args:
            title: Page title

        Returns:
            Dictionary containing page summary, or None if not found
        """
        params = {
            'action': 'query',
            'titles': title,
            'prop': 'extracts|pageimages|info',
            'exintro': True,
            'explaintext': True,
            'exsentences': 3,  # First 3 sentences
            'inprop': 'url',
            'piprop': 'original',
            'format': 'json'
        }

        try:
            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            pages = data.get('query', {}).get('pages', {})

            if not pages:
                return None

            page_id = list(pages.keys())[0]
            if page_id == '-1':
                return None

            page = pages[page_id]
            time.sleep(0.1)

            result = {
                'pageid': page.get('pageid'),
                'title': page.get('title'),
                'summary': page.get('extract', ''),
                'url': page.get('fullurl', '')
            }

            # Add image if available
            if 'original' in page:
                result['image'] = page['original'].get('source')

            return result

        except requests.RequestException as e:
            raise Exception(f"Wikipedia summary fetch failed: {str(e)}")

    def get_random_pages(self, count: int = 1) -> List[Dict]:
        """
        Get random Wikipedia pages.

        Args:
            count: Number of random pages to retrieve (max: 10)

        Returns:
            List of dictionaries containing page information
        """
        params = {
            'action': 'query',
            'list': 'random',
            'rnlimit': min(count, 10),
            'rnnamespace': 0,  # Main namespace only
            'format': 'json'
        }

        try:
            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            random_pages = data.get('query', {}).get('random', [])

            results = []
            for page in random_pages:
                results.append({
                    'pageid': page.get('id'),
                    'title': page.get('title'),
                    'url': f"https://{self.language}.wikipedia.org/wiki/{page.get('title', '').replace(' ', '_')}"
                })

            time.sleep(0.1)

            return results

        except requests.RequestException as e:
            raise Exception(f"Wikipedia random pages fetch failed: {str(e)}")

    def search_categories(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for Wikipedia categories.

        Args:
            query: Category search query
            limit: Maximum number of results

        Returns:
            List of dictionaries containing category information
        """
        params = {
            'action': 'query',
            'list': 'allcategories',
            'acprefix': query,
            'aclimit': min(limit, 500),
            'format': 'json'
        }

        try:
            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            categories = data.get('query', {}).get('allcategories', [])

            results = []
            for cat in categories:
                cat_title = cat.get('*', '')
                results.append({
                    'category': cat_title,
                    'url': f"https://{self.language}.wikipedia.org/wiki/Category:{cat_title.replace(' ', '_')}"
                })

            time.sleep(0.1)

            return results

        except requests.RequestException as e:
            raise Exception(f"Wikipedia category search failed: {str(e)}")

    def get_pages_in_category(
        self,
        category: str,
        limit: int = 10
    ) -> List[Dict]:
        """
        Get pages in a specific category.

        Args:
            category: Category name (without "Category:" prefix)
            limit: Maximum number of results

        Returns:
            List of dictionaries containing page information
        """
        params = {
            'action': 'query',
            'list': 'categorymembers',
            'cmtitle': f'Category:{category}',
            'cmlimit': min(limit, 500),
            'format': 'json'
        }

        try:
            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            members = data.get('query', {}).get('categorymembers', [])

            results = []
            for member in members:
                results.append({
                    'pageid': member.get('pageid'),
                    'title': member.get('title'),
                    'url': f"https://{self.language}.wikipedia.org/wiki/{member.get('title', '').replace(' ', '_')}"
                })

            time.sleep(0.1)

            return results

        except requests.RequestException as e:
            raise Exception(f"Wikipedia category members fetch failed: {str(e)}")

    @staticmethod
    def _clean_snippet(snippet: str) -> str:
        """Remove HTML tags from snippet."""
        import re
        return re.sub(r'<[^>]+>', '', snippet)
