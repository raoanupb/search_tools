"""
GitHub Search Tool

Provides search capabilities for GitHub code, repositories, issues, and users.

API Documentation: https://docs.github.com/en/rest/search
"""

import requests
from typing import List, Dict, Optional
import time


class GitHubSearch:
    """
    Search tool for GitHub.

    Uses the free GitHub REST API to search for code, repositories, issues, and users.
    Authentication is optional but recommended for higher rate limits.

    Rate Limits:
    - Unauthenticated: 60 requests/hour
    - Authenticated: 5000 requests/hour
    - Code search: 10 requests/minute (regardless of authentication)
    """

    BASE_URL = "https://api.github.com"

    def __init__(self, token: Optional[str] = None):
        """
        Initialize the GitHub search tool.

        Args:
            token: Optional GitHub personal access token for higher rate limits.
                   Generate at: https://github.com/settings/tokens
        """
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'SearchTools/0.1.0 (Language Agent Search Tool)'
        })

        if token:
            self.session.headers.update({'Authorization': f'token {token}'})

    def search_repositories(
        self,
        query: str,
        sort: str = "stars",
        order: str = "desc",
        per_page: int = 10,
        page: int = 1,
        language: Optional[str] = None,
        min_stars: Optional[int] = None,
        created_after: Optional[str] = None
    ) -> Dict:
        """
        Search GitHub repositories.

        Args:
            query: Search query string
            sort: Sort by 'stars', 'forks', 'help-wanted-issues', 'updated'
            order: Order 'asc' or 'desc'
            per_page: Results per page (max 100)
            page: Page number
            language: Filter by programming language (e.g., 'python', 'javascript')
            min_stars: Minimum number of stars
            created_after: Filter repos created after date (YYYY-MM-DD)

        Returns:
            Dictionary containing search results and metadata

        Example:
            >>> github = GitHubSearch(token="your-token")
            >>> results = github.search_repositories(
            ...     "machine learning",
            ...     language="python",
            ...     min_stars=1000
            ... )
            >>> for repo in results['items']:
            ...     print(f"{repo['full_name']} - ⭐ {repo['stargazers_count']}")
        """
        # Build search query with filters
        search_query = query
        if language:
            search_query += f" language:{language}"
        if min_stars:
            search_query += f" stars:>={min_stars}"
        if created_after:
            search_query += f" created:>{created_after}"

        params = {
            'q': search_query,
            'sort': sort,
            'order': order,
            'per_page': min(per_page, 100),
            'page': page
        }

        try:
            response = self.session.get(
                f"{self.BASE_URL}/search/repositories",
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()

            # Add rate limit info
            rate_limit_info = self._get_rate_limit_info(response)

            # Process results
            results = {
                'total_count': data.get('total_count', 0),
                'incomplete_results': data.get('incomplete_results', False),
                'items': self._process_repositories(data.get('items', [])),
                'rate_limit': rate_limit_info
            }

            time.sleep(1)  # Be respectful with rate limiting

            return results

        except requests.RequestException as e:
            raise Exception(f"GitHub repository search failed: {str(e)}")

    def search_code(
        self,
        query: str,
        sort: str = "indexed",
        order: str = "desc",
        per_page: int = 10,
        page: int = 1,
        language: Optional[str] = None,
        repo: Optional[str] = None,
        path: Optional[str] = None,
        extension: Optional[str] = None
    ) -> Dict:
        """
        Search code on GitHub.

        Args:
            query: Search query string (code content to search for)
            sort: Sort by 'indexed' (recently indexed first)
            order: Order 'asc' or 'desc'
            per_page: Results per page (max 100)
            page: Page number
            language: Filter by programming language
            repo: Search within specific repository (format: owner/repo)
            path: Search in specific path
            extension: Filter by file extension (e.g., 'py', 'js')

        Returns:
            Dictionary containing search results and metadata

        Example:
            >>> github = GitHubSearch(token="your-token")
            >>> results = github.search_code(
            ...     "def neural_network",
            ...     language="python",
            ...     extension="py"
            ... )
            >>> for item in results['items']:
            ...     print(f"{item['repository']['full_name']}/{item['path']}")
        """
        # Build search query with filters
        search_query = query
        if language:
            search_query += f" language:{language}"
        if repo:
            search_query += f" repo:{repo}"
        if path:
            search_query += f" path:{path}"
        if extension:
            search_query += f" extension:{extension}"

        params = {
            'q': search_query,
            'sort': sort,
            'order': order,
            'per_page': min(per_page, 100),
            'page': page
        }

        try:
            response = self.session.get(
                f"{self.BASE_URL}/search/code",
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            rate_limit_info = self._get_rate_limit_info(response)

            results = {
                'total_count': data.get('total_count', 0),
                'incomplete_results': data.get('incomplete_results', False),
                'items': self._process_code_results(data.get('items', [])),
                'rate_limit': rate_limit_info
            }

            # Code search has stricter rate limits (10 req/min)
            time.sleep(6)

            return results

        except requests.RequestException as e:
            raise Exception(f"GitHub code search failed: {str(e)}")

    def search_issues(
        self,
        query: str,
        sort: str = "created",
        order: str = "desc",
        per_page: int = 10,
        page: int = 1,
        state: Optional[str] = None,
        labels: Optional[List[str]] = None,
        language: Optional[str] = None
    ) -> Dict:
        """
        Search GitHub issues and pull requests.

        Args:
            query: Search query string
            sort: Sort by 'created', 'updated', 'comments', 'reactions'
            order: Order 'asc' or 'desc'
            per_page: Results per page (max 100)
            page: Page number
            state: Filter by 'open', 'closed'
            labels: Filter by labels (list of label names)
            language: Filter by repository language

        Returns:
            Dictionary containing search results and metadata

        Example:
            >>> github = GitHubSearch()
            >>> results = github.search_issues(
            ...     "bug",
            ...     state="open",
            ...     labels=["good first issue"]
            ... )
        """
        search_query = query
        if state:
            search_query += f" state:{state}"
        if labels:
            for label in labels:
                search_query += f" label:\"{label}\""
        if language:
            search_query += f" language:{language}"

        params = {
            'q': search_query,
            'sort': sort,
            'order': order,
            'per_page': min(per_page, 100),
            'page': page
        }

        try:
            response = self.session.get(
                f"{self.BASE_URL}/search/issues",
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            rate_limit_info = self._get_rate_limit_info(response)

            results = {
                'total_count': data.get('total_count', 0),
                'incomplete_results': data.get('incomplete_results', False),
                'items': self._process_issues(data.get('items', [])),
                'rate_limit': rate_limit_info
            }

            time.sleep(1)

            return results

        except requests.RequestException as e:
            raise Exception(f"GitHub issues search failed: {str(e)}")

    def search_users(
        self,
        query: str,
        sort: str = "followers",
        order: str = "desc",
        per_page: int = 10,
        page: int = 1,
        location: Optional[str] = None,
        language: Optional[str] = None,
        min_followers: Optional[int] = None
    ) -> Dict:
        """
        Search GitHub users.

        Args:
            query: Search query string (username or name)
            sort: Sort by 'followers', 'repositories', 'joined'
            order: Order 'asc' or 'desc'
            per_page: Results per page (max 100)
            page: Page number
            location: Filter by location
            language: Filter by primary language
            min_followers: Minimum number of followers

        Returns:
            Dictionary containing search results and metadata
        """
        search_query = query
        if location:
            search_query += f" location:{location}"
        if language:
            search_query += f" language:{language}"
        if min_followers:
            search_query += f" followers:>={min_followers}"

        params = {
            'q': search_query,
            'sort': sort,
            'order': order,
            'per_page': min(per_page, 100),
            'page': page
        }

        try:
            response = self.session.get(
                f"{self.BASE_URL}/search/users",
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            rate_limit_info = self._get_rate_limit_info(response)

            results = {
                'total_count': data.get('total_count', 0),
                'incomplete_results': data.get('incomplete_results', False),
                'items': self._process_users(data.get('items', [])),
                'rate_limit': rate_limit_info
            }

            time.sleep(1)

            return results

        except requests.RequestException as e:
            raise Exception(f"GitHub users search failed: {str(e)}")

    def get_trending_repositories(
        self,
        language: Optional[str] = None,
        since: str = "daily"
    ) -> List[Dict]:
        """
        Get trending repositories (via search heuristic).

        Note: GitHub doesn't have an official trending API, so we simulate it
        by searching for recently created/updated repos with high stars.

        Args:
            language: Filter by language
            since: Time period - 'daily', 'weekly', 'monthly'

        Returns:
            List of trending repositories
        """
        from datetime import datetime, timedelta

        # Calculate date based on period
        days = {'daily': 1, 'weekly': 7, 'monthly': 30}.get(since, 7)
        date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        # Search for repos created recently with high stars
        query = f"created:>{date}"
        if language:
            query += f" language:{language}"

        result = self.search_repositories(
            query,
            sort="stars",
            order="desc",
            per_page=30
        )

        return result['items']

    def get_repository(self, owner: str, repo: str) -> Dict:
        """
        Get detailed information about a specific repository.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Dictionary containing repository information
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/repos/{owner}/{repo}",
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            time.sleep(0.5)

            return {
                'full_name': data.get('full_name'),
                'description': data.get('description'),
                'url': data.get('html_url'),
                'stars': data.get('stargazers_count', 0),
                'forks': data.get('forks_count', 0),
                'watchers': data.get('watchers_count', 0),
                'language': data.get('language'),
                'topics': data.get('topics', []),
                'created_at': data.get('created_at'),
                'updated_at': data.get('updated_at'),
                'open_issues': data.get('open_issues_count', 0),
                'license': data.get('license', {}).get('name') if data.get('license') else None,
                'homepage': data.get('homepage'),
                'size': data.get('size'),
                'default_branch': data.get('default_branch')
            }

        except requests.RequestException as e:
            raise Exception(f"GitHub repository fetch failed: {str(e)}")

    def get_rate_limit(self) -> Dict:
        """
        Get current rate limit status.

        Returns:
            Dictionary containing rate limit information
        """
        try:
            response = self.session.get(f"{self.BASE_URL}/rate_limit", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to get rate limit: {str(e)}")

    def _process_repositories(self, items: List[Dict]) -> List[Dict]:
        """Process repository search results."""
        return [
            {
                'full_name': item.get('full_name'),
                'description': item.get('description'),
                'url': item.get('html_url'),
                'stars': item.get('stargazers_count', 0),
                'forks': item.get('forks_count', 0),
                'watchers': item.get('watchers_count', 0),
                'language': item.get('language'),
                'topics': item.get('topics', []),
                'created_at': item.get('created_at'),
                'updated_at': item.get('updated_at'),
                'open_issues': item.get('open_issues_count', 0),
                'license': item.get('license', {}).get('name') if item.get('license') else None,
                'owner': {
                    'login': item.get('owner', {}).get('login'),
                    'url': item.get('owner', {}).get('html_url'),
                    'avatar': item.get('owner', {}).get('avatar_url')
                }
            }
            for item in items
        ]

    def _process_code_results(self, items: List[Dict]) -> List[Dict]:
        """Process code search results."""
        return [
            {
                'name': item.get('name'),
                'path': item.get('path'),
                'url': item.get('html_url'),
                'repository': {
                    'full_name': item.get('repository', {}).get('full_name'),
                    'description': item.get('repository', {}).get('description'),
                    'url': item.get('repository', {}).get('html_url'),
                    'stars': item.get('repository', {}).get('stargazers_count', 0),
                    'language': item.get('repository', {}).get('language')
                },
                'score': item.get('score', 0)
            }
            for item in items
        ]

    def _process_issues(self, items: List[Dict]) -> List[Dict]:
        """Process issue/PR search results."""
        return [
            {
                'title': item.get('title'),
                'number': item.get('number'),
                'state': item.get('state'),
                'url': item.get('html_url'),
                'created_at': item.get('created_at'),
                'updated_at': item.get('updated_at'),
                'comments': item.get('comments', 0),
                'labels': [label.get('name') for label in item.get('labels', [])],
                'user': {
                    'login': item.get('user', {}).get('login'),
                    'url': item.get('user', {}).get('html_url')
                },
                'repository_url': item.get('repository_url'),
                'is_pull_request': 'pull_request' in item
            }
            for item in items
        ]

    def _process_users(self, items: List[Dict]) -> List[Dict]:
        """Process user search results."""
        return [
            {
                'login': item.get('login'),
                'name': item.get('name'),
                'url': item.get('html_url'),
                'avatar': item.get('avatar_url'),
                'type': item.get('type'),
                'bio': item.get('bio'),
                'location': item.get('location'),
                'email': item.get('email'),
                'followers': item.get('followers', 0),
                'public_repos': item.get('public_repos', 0),
                'score': item.get('score', 0)
            }
            for item in items
        ]

    def _get_rate_limit_info(self, response) -> Dict:
        """Extract rate limit information from response headers."""
        return {
            'limit': int(response.headers.get('X-RateLimit-Limit', 0)),
            'remaining': int(response.headers.get('X-RateLimit-Remaining', 0)),
            'reset': int(response.headers.get('X-RateLimit-Reset', 0))
        }
