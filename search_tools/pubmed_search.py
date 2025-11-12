"""
PubMed Search Tool

Provides search capabilities for PubMed, a free resource supporting the search
and retrieval of biomedical and life sciences literature.

API Documentation: https://www.ncbi.nlm.nih.gov/books/NBK25500/
"""

import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
import time


class PubMedSearch:
    """
    Search tool for PubMed/NCBI literature.

    Uses the free E-utilities API from NCBI.
    No API key required (but recommended for higher rate limits).
    """

    ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

    def __init__(self, api_key: Optional[str] = None, email: Optional[str] = None):
        """
        Initialize the PubMed search tool.

        Args:
            api_key: Optional NCBI API key for higher rate limits (10 req/sec vs 3 req/sec)
            email: Optional email (NCBI requests this for tracking)
        """
        self.api_key = api_key
        self.email = email
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SearchTools/0.1.0 (Language Agent Search Tool)'
        })

    def search(
        self,
        query: str,
        max_results: int = 10,
        sort: str = "relevance",
        min_date: Optional[str] = None,
        max_date: Optional[str] = None
    ) -> List[Dict]:
        """
        Search PubMed for articles matching the query.

        Args:
            query: Search query string (supports PubMed query syntax)
            max_results: Maximum number of results to return (default: 10)
            sort: Sort order - 'relevance', 'pub_date', or 'title'
            min_date: Minimum publication date (format: YYYY/MM/DD)
            max_date: Maximum publication date (format: YYYY/MM/DD)

        Returns:
            List of dictionaries containing article information

        Example:
            >>> pubmed = PubMedSearch()
            >>> results = pubmed.search("CRISPR gene editing", max_results=5)
            >>> for article in results:
            ...     print(f"{article['title']}")

        Query examples:
            - "cancer AND treatment"
            - "diabetes[Title/Abstract]"
            - "2020/01/01:2020/12/31[pdat]"  # date range
        """
        # Step 1: Search for PMIDs
        pmids = self._search_pmids(query, max_results, sort, min_date, max_date)

        if not pmids:
            return []

        # Step 2: Fetch details for the PMIDs
        articles = self._fetch_details(pmids)

        return articles

    def _search_pmids(
        self,
        query: str,
        max_results: int,
        sort: str,
        min_date: Optional[str],
        max_date: Optional[str]
    ) -> List[str]:
        """Search for PubMed IDs matching the query."""
        params = {
            'db': 'pubmed',
            'term': query,
            'retmax': max_results,
            'retmode': 'json',
            'sort': sort
        }

        if self.api_key:
            params['api_key'] = self.api_key
        if self.email:
            params['email'] = self.email
        if min_date:
            params['mindate'] = min_date
        if max_date:
            params['maxdate'] = max_date

        try:
            response = self.session.get(self.ESEARCH_URL, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            pmids = data.get('esearchresult', {}).get('idlist', [])

            # Rate limiting: 3 req/sec without key, 10 req/sec with key
            time.sleep(0.34 if not self.api_key else 0.11)

            return pmids

        except requests.RequestException as e:
            raise Exception(f"PubMed search request failed: {str(e)}")

    def _fetch_details(self, pmids: List[str]) -> List[Dict]:
        """Fetch detailed information for a list of PMIDs."""
        if not pmids:
            return []

        params = {
            'db': 'pubmed',
            'id': ','.join(pmids),
            'retmode': 'xml'
        }

        if self.api_key:
            params['api_key'] = self.api_key
        if self.email:
            params['email'] = self.email

        try:
            response = self.session.get(self.EFETCH_URL, params=params, timeout=30)
            response.raise_for_status()

            articles = self._parse_articles(response.text)

            time.sleep(0.34 if not self.api_key else 0.11)

            return articles

        except requests.RequestException as e:
            raise Exception(f"PubMed fetch request failed: {str(e)}")

    def _parse_articles(self, xml_text: str) -> List[Dict]:
        """Parse XML response containing article details."""
        root = ET.fromstring(xml_text)
        articles = []

        for article_elem in root.findall('.//PubmedArticle'):
            article = {}

            # PMID
            pmid_elem = article_elem.find('.//PMID')
            article['pmid'] = pmid_elem.text if pmid_elem is not None else None

            # Title
            title_elem = article_elem.find('.//ArticleTitle')
            article['title'] = title_elem.text if title_elem is not None else ""

            # Abstract
            abstract_texts = article_elem.findall('.//AbstractText')
            if abstract_texts:
                abstract_parts = []
                for abs_text in abstract_texts:
                    label = abs_text.get('Label', '')
                    text = abs_text.text or ""
                    if label:
                        abstract_parts.append(f"{label}: {text}")
                    else:
                        abstract_parts.append(text)
                article['abstract'] = " ".join(abstract_parts)
            else:
                article['abstract'] = ""

            # Authors
            authors = []
            for author in article_elem.findall('.//Author'):
                last_name = author.find('LastName')
                fore_name = author.find('ForeName')
                if last_name is not None and fore_name is not None:
                    authors.append(f"{fore_name.text} {last_name.text}")
                elif last_name is not None:
                    authors.append(last_name.text)
            article['authors'] = authors

            # Journal
            journal_elem = article_elem.find('.//Journal/Title')
            article['journal'] = journal_elem.text if journal_elem is not None else ""

            # Publication date
            pub_date = article_elem.find('.//PubDate')
            if pub_date is not None:
                year = pub_date.find('Year')
                month = pub_date.find('Month')
                day = pub_date.find('Day')
                date_parts = []
                if year is not None:
                    date_parts.append(year.text)
                if month is not None:
                    date_parts.append(month.text)
                if day is not None:
                    date_parts.append(day.text)
                article['publication_date'] = " ".join(date_parts)
            else:
                article['publication_date'] = ""

            # DOI
            doi_elem = article_elem.find('.//ArticleId[@IdType="doi"]')
            article['doi'] = doi_elem.text if doi_elem is not None else None

            # PubMed URL
            if article['pmid']:
                article['url'] = f"https://pubmed.ncbi.nlm.nih.gov/{article['pmid']}/"

            # Keywords
            keywords = []
            for keyword in article_elem.findall('.//Keyword'):
                if keyword.text:
                    keywords.append(keyword.text)
            article['keywords'] = keywords

            # MeSH terms
            mesh_terms = []
            for mesh in article_elem.findall('.//MeshHeading/DescriptorName'):
                if mesh.text:
                    mesh_terms.append(mesh.text)
            article['mesh_terms'] = mesh_terms

            articles.append(article)

        return articles

    def get_article_by_pmid(self, pmid: str) -> Optional[Dict]:
        """
        Get a specific article by its PubMed ID.

        Args:
            pmid: PubMed ID

        Returns:
            Dictionary containing article information, or None if not found
        """
        articles = self._fetch_details([pmid])
        return articles[0] if articles else None

    def search_by_author(self, author: str, max_results: int = 10) -> List[Dict]:
        """
        Search for articles by author name.

        Args:
            author: Author name
            max_results: Maximum number of results to return

        Returns:
            List of dictionaries containing article information
        """
        query = f"{author}[Author]"
        return self.search(query, max_results=max_results)

    def search_recent(
        self,
        query: str,
        days: int = 30,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Search for recent articles (within specified number of days).

        Args:
            query: Search query
            days: Number of days to look back (default: 30)
            max_results: Maximum number of results

        Returns:
            List of dictionaries containing article information
        """
        query_with_date = f"{query} AND {days}[pdat]"
        return self.search(query_with_date, max_results=max_results, sort="pub_date")
