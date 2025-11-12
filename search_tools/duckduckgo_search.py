"""
DuckDuckGo Search Tool

Provides search capabilities for DuckDuckGo, a privacy-focused search engine.

This implementation uses the duckduckgo_search library which provides a simple
interface to DuckDuckGo's search functionality.
"""

from typing import List, Dict, Optional
try:
    from duckduckgo_search import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False
    print("Warning: duckduckgo_search library not available. Install with: pip install duckduckgo-search")


class DuckDuckGoSearch:
    """
    Search tool for DuckDuckGo.

    Uses the duckduckgo_search library for privacy-focused web searches.
    No API key required.
    """

    def __init__(self):
        """Initialize the DuckDuckGo search tool."""
        if not DDGS_AVAILABLE:
            raise ImportError(
                "duckduckgo_search library is required. "
                "Install it with: pip install duckduckgo-search"
            )

    def search(
        self,
        query: str,
        max_results: int = 10,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: Optional[str] = None
    ) -> List[Dict]:
        """
        Search DuckDuckGo for web results.

        Args:
            query: Search query string
            max_results: Maximum number of results to return (default: 10)
            region: Region code (default: "wt-wt" for worldwide)
            safesearch: Safe search setting - "on", "moderate", or "off"
            timelimit: Time limit for results - "d" (day), "w" (week), "m" (month), "y" (year)

        Returns:
            List of dictionaries containing search result information

        Example:
            >>> ddg = DuckDuckGoSearch()
            >>> results = ddg.search("python programming", max_results=5)
            >>> for result in results:
            ...     print(f"{result['title']}: {result['url']}")
        """
        try:
            with DDGS() as ddgs:
                results = []

                search_params = {
                    'keywords': query,
                    'region': region,
                    'safesearch': safesearch,
                    'max_results': max_results
                }

                if timelimit:
                    search_params['timelimit'] = timelimit

                for i, result in enumerate(ddgs.text(**search_params), start=1):
                    results.append({
                        'title': result.get('title', ''),
                        'url': result.get('href', ''),
                        'snippet': result.get('body', ''),
                        'position': i
                    })

                    if len(results) >= max_results:
                        break

                return results

        except Exception as e:
            raise Exception(f"DuckDuckGo search failed: {str(e)}")

    def search_news(
        self,
        query: str,
        max_results: int = 10,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: Optional[str] = None
    ) -> List[Dict]:
        """
        Search DuckDuckGo for news results.

        Args:
            query: Search query string
            max_results: Maximum number of results to return
            region: Region code
            safesearch: Safe search setting
            timelimit: Time limit for results

        Returns:
            List of dictionaries containing news result information
        """
        try:
            with DDGS() as ddgs:
                results = []

                search_params = {
                    'keywords': query,
                    'region': region,
                    'safesearch': safesearch,
                    'max_results': max_results
                }

                if timelimit:
                    search_params['timelimit'] = timelimit

                for i, result in enumerate(ddgs.news(**search_params), start=1):
                    results.append({
                        'title': result.get('title', ''),
                        'url': result.get('url', ''),
                        'snippet': result.get('body', ''),
                        'source': result.get('source', ''),
                        'date': result.get('date', ''),
                        'image': result.get('image', ''),
                        'position': i
                    })

                    if len(results) >= max_results:
                        break

                return results

        except Exception as e:
            raise Exception(f"DuckDuckGo news search failed: {str(e)}")

    def search_images(
        self,
        query: str,
        max_results: int = 10,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        size: Optional[str] = None,
        color: Optional[str] = None,
        type_image: Optional[str] = None,
        layout: Optional[str] = None
    ) -> List[Dict]:
        """
        Search DuckDuckGo for images.

        Args:
            query: Search query string
            max_results: Maximum number of results to return
            region: Region code
            safesearch: Safe search setting
            size: Image size - "Small", "Medium", "Large", "Wallpaper"
            color: Image color - "color", "Monochrome", "Red", "Orange", "Yellow", etc.
            type_image: Image type - "photo", "clipart", "gif", "transparent", "line"
            layout: Image layout - "Square", "Tall", "Wide"

        Returns:
            List of dictionaries containing image result information
        """
        try:
            with DDGS() as ddgs:
                results = []

                search_params = {
                    'keywords': query,
                    'region': region,
                    'safesearch': safesearch,
                    'max_results': max_results
                }

                if size:
                    search_params['size'] = size
                if color:
                    search_params['color'] = color
                if type_image:
                    search_params['type_image'] = type_image
                if layout:
                    search_params['layout'] = layout

                for i, result in enumerate(ddgs.images(**search_params), start=1):
                    results.append({
                        'title': result.get('title', ''),
                        'image_url': result.get('image', ''),
                        'thumbnail_url': result.get('thumbnail', ''),
                        'source_url': result.get('url', ''),
                        'height': result.get('height'),
                        'width': result.get('width'),
                        'source': result.get('source', ''),
                        'position': i
                    })

                    if len(results) >= max_results:
                        break

                return results

        except Exception as e:
            raise Exception(f"DuckDuckGo image search failed: {str(e)}")

    def search_videos(
        self,
        query: str,
        max_results: int = 10,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: Optional[str] = None,
        resolution: Optional[str] = None,
        duration: Optional[str] = None
    ) -> List[Dict]:
        """
        Search DuckDuckGo for videos.

        Args:
            query: Search query string
            max_results: Maximum number of results to return
            region: Region code
            safesearch: Safe search setting
            timelimit: Time limit for results
            resolution: Video resolution - "high", "standard"
            duration: Video duration - "short", "medium", "long"

        Returns:
            List of dictionaries containing video result information
        """
        try:
            with DDGS() as ddgs:
                results = []

                search_params = {
                    'keywords': query,
                    'region': region,
                    'safesearch': safesearch,
                    'max_results': max_results
                }

                if timelimit:
                    search_params['timelimit'] = timelimit
                if resolution:
                    search_params['resolution'] = resolution
                if duration:
                    search_params['duration'] = duration

                for i, result in enumerate(ddgs.videos(**search_params), start=1):
                    results.append({
                        'title': result.get('title', ''),
                        'url': result.get('content', ''),
                        'description': result.get('description', ''),
                        'duration': result.get('duration', ''),
                        'published': result.get('published', ''),
                        'publisher': result.get('publisher', ''),
                        'thumbnail': result.get('images', {}).get('large', ''),
                        'position': i
                    })

                    if len(results) >= max_results:
                        break

                return results

        except Exception as e:
            raise Exception(f"DuckDuckGo video search failed: {str(e)}")

    def instant_answer(self, query: str) -> Optional[Dict]:
        """
        Get DuckDuckGo instant answer for a query.

        Args:
            query: Search query string

        Returns:
            Dictionary containing instant answer information, or None if not available

        Example:
            >>> ddg = DuckDuckGoSearch()
            >>> answer = ddg.instant_answer("what is the capital of France")
            >>> if answer:
            ...     print(answer['answer'])
        """
        try:
            with DDGS() as ddgs:
                results = list(ddgs.answers(query))

                if results:
                    result = results[0]
                    return {
                        'answer': result.get('text', ''),
                        'url': result.get('url', ''),
                        'topic': result.get('topic', '')
                    }

                return None

        except Exception as e:
            raise Exception(f"DuckDuckGo instant answer failed: {str(e)}")

    def suggestions(self, query: str, region: str = "wt-wt") -> List[str]:
        """
        Get search suggestions from DuckDuckGo.

        Args:
            query: Partial search query
            region: Region code

        Returns:
            List of search suggestions

        Example:
            >>> ddg = DuckDuckGoSearch()
            >>> suggestions = ddg.suggestions("python prog")
            >>> print(suggestions)
            ['python programming', 'python program', 'python projects', ...]
        """
        try:
            with DDGS() as ddgs:
                results = ddgs.suggestions(query, region=region)
                return [s.get('phrase', '') for s in results if 'phrase' in s]

        except Exception as e:
            raise Exception(f"DuckDuckGo suggestions failed: {str(e)}")
