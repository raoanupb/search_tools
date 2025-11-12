"""
Google Search Tool

Provides search capabilities for Google using Playwright for web scraping.

Note: This tool uses web scraping which may be subject to rate limiting and
CAPTCHA challenges. For production use, consider using Google Custom Search API
or other official APIs.
"""

from typing import List, Dict, Optional
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time


class GoogleSearch:
    """
    Search tool for Google using Playwright.

    This tool performs web scraping of Google search results.
    Use responsibly and be aware of rate limits.
    """

    def __init__(self, headless: bool = True, slow_mo: int = 0):
        """
        Initialize the Google search tool.

        Args:
            headless: Run browser in headless mode (default: True)
            slow_mo: Slow down operations by specified milliseconds (default: 0)
        """
        self.headless = headless
        self.slow_mo = slow_mo
        self.playwright = None
        self.browser = None

    def __enter__(self):
        """Context manager entry."""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def search(
        self,
        query: str,
        num_results: int = 10,
        lang: str = "en",
        time_range: Optional[str] = None
    ) -> List[Dict]:
        """
        Search Google and extract results.

        Args:
            query: Search query string
            num_results: Number of results to extract (default: 10)
            lang: Language code (default: "en")
            time_range: Optional time range filter - 'h' (hour), 'd' (day), 'w' (week),
                       'm' (month), 'y' (year)

        Returns:
            List of dictionaries containing search result information

        Example:
            >>> with GoogleSearch() as google:
            ...     results = google.search("python programming", num_results=5)
            ...     for result in results:
            ...         print(f"{result['title']}: {result['url']}")
        """
        if not self.browser:
            raise RuntimeError("GoogleSearch must be used as a context manager")

        context = self.browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()

        results = []

        try:
            # Build URL
            url = f"https://www.google.com/search?q={query}&hl={lang}"
            if time_range:
                url += f"&tbs=qdr:{time_range}"

            # Navigate to Google
            page.goto(url, wait_until="networkidle", timeout=30000)

            # Wait for search results
            try:
                page.wait_for_selector('div#search', timeout=10000)
            except PlaywrightTimeout:
                # Check if we hit a CAPTCHA
                if page.locator('form[action*="sorry"]').count() > 0:
                    raise Exception("Google CAPTCHA detected. Try again later or use a different IP.")
                raise

            # Extract search results
            result_count = 0
            result_selectors = [
                'div.g',  # Standard result
                'div[data-sokoban-container]',  # Alternative structure
            ]

            for selector in result_selectors:
                search_results = page.locator(selector).all()

                for result in search_results:
                    if result_count >= num_results:
                        break

                    try:
                        # Extract title and URL
                        title_elem = result.locator('h3').first
                        if title_elem.count() == 0:
                            continue

                        title = title_elem.text_content()

                        # Try to find the link
                        link_elem = result.locator('a[href]').first
                        if link_elem.count() == 0:
                            continue

                        url = link_elem.get_attribute('href')

                        # Skip non-http links and Google internal links
                        if not url or not url.startswith('http') or 'google.com' in url:
                            continue

                        # Extract snippet/description
                        snippet = ""
                        snippet_selectors = [
                            'div[data-sncf="1"]',  # Common snippet location
                            'div.VwiC3b',  # Alternative snippet
                            'span.aCOpRe',  # Another alternative
                        ]

                        for snip_sel in snippet_selectors:
                            snip_elem = result.locator(snip_sel).first
                            if snip_elem.count() > 0:
                                snippet = snip_elem.text_content()
                                break

                        results.append({
                            'title': title.strip() if title else "",
                            'url': url,
                            'snippet': snippet.strip() if snippet else "",
                            'position': result_count + 1
                        })

                        result_count += 1

                    except Exception as e:
                        # Skip problematic results
                        continue

                if result_count >= num_results:
                    break

            # Be respectful - add delay
            time.sleep(1)

        except PlaywrightTimeout:
            raise Exception("Timeout while loading Google search results")
        except Exception as e:
            raise Exception(f"Google search failed: {str(e)}")
        finally:
            context.close()

        return results

    def search_news(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        Search Google News.

        Args:
            query: Search query string
            num_results: Number of results to extract

        Returns:
            List of dictionaries containing news result information
        """
        if not self.browser:
            raise RuntimeError("GoogleSearch must be used as a context manager")

        context = self.browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()

        results = []

        try:
            # Navigate to Google News search
            url = f"https://www.google.com/search?q={query}&tbm=nws"
            page.goto(url, wait_until="networkidle", timeout=30000)

            # Wait for results
            page.wait_for_selector('div#search', timeout=10000)

            # Extract news results
            news_results = page.locator('div.SoaBEf').all()

            for i, result in enumerate(news_results[:num_results]):
                try:
                    title_elem = result.locator('div[role="heading"]').first
                    title = title_elem.text_content() if title_elem.count() > 0 else ""

                    link_elem = result.locator('a[href]').first
                    url = link_elem.get_attribute('href') if link_elem.count() > 0 else ""

                    snippet_elem = result.locator('div.GI74Re').first
                    snippet = snippet_elem.text_content() if snippet_elem.count() > 0 else ""

                    source_elem = result.locator('div.MgUUmf').first
                    source = source_elem.text_content() if source_elem.count() > 0 else ""

                    if title and url:
                        results.append({
                            'title': title.strip(),
                            'url': url,
                            'snippet': snippet.strip(),
                            'source': source.strip(),
                            'position': i + 1
                        })
                except Exception:
                    continue

            time.sleep(1)

        except Exception as e:
            raise Exception(f"Google News search failed: {str(e)}")
        finally:
            context.close()

        return results

    def search_images(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        Search Google Images.

        Args:
            query: Search query string
            num_results: Number of results to extract

        Returns:
            List of dictionaries containing image result information
        """
        if not self.browser:
            raise RuntimeError("GoogleSearch must be used as a context manager")

        context = self.browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()

        results = []

        try:
            # Navigate to Google Images
            url = f"https://www.google.com/search?q={query}&tbm=isch"
            page.goto(url, wait_until="networkidle", timeout=30000)

            # Wait for images to load
            page.wait_for_selector('div#search', timeout=10000)

            # Extract image results
            image_containers = page.locator('div.isv-r').all()

            for i, container in enumerate(image_containers[:num_results]):
                try:
                    # Get thumbnail
                    img_elem = container.locator('img').first
                    thumbnail = img_elem.get_attribute('src') if img_elem.count() > 0 else ""

                    # Get link
                    link_elem = container.locator('a').first
                    link = link_elem.get_attribute('href') if link_elem.count() > 0 else ""

                    # Try to get title from alt text
                    title = img_elem.get_attribute('alt') if img_elem.count() > 0 else ""

                    if thumbnail:
                        results.append({
                            'title': title.strip() if title else f"Image {i+1}",
                            'thumbnail_url': thumbnail,
                            'link': f"https://www.google.com{link}" if link else "",
                            'position': i + 1
                        })
                except Exception:
                    continue

            time.sleep(1)

        except Exception as e:
            raise Exception(f"Google Images search failed: {str(e)}")
        finally:
            context.close()

        return results
