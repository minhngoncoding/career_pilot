from typing import Optional, List, Dict
from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import time
import logging

logger = logging.getLogger(__name__)


@dataclass
class JobPosting:
    """Job posting data structure."""

    job_title: str
    company: str
    location: str
    description: str
    requirements: List[str] = None
    salary: Optional[str] = None
    benefits: List[str] = None
    source_url: str = ""


class JobScraper:
    """Web scraper for job descriptions."""

    def __init__(self, rate_limit_delay: float = 1.0):
        self.rate_limit_delay = rate_limit_delay
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def scrape_jd(self, url: str) -> Optional[JobPosting]:
        """Scrape a single job description from URL."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "lxml")

            # Try different extraction strategies based on common job sites
            jd = self._extract_jd(soup, url)
            if jd:
                jd.source_url = url
                return jd

            return None

        except requests.RequestException as e:
            logger.error(f"Failed to scrape {url}: {e}")
            return None

    def _extract_jd(self, soup: BeautifulSoup, url: str) -> Optional[JobPosting]:
        """Extract job posting data from HTML."""
        # Common selectors for job sites
        selectors = {
            "title": [
                "h1.job-title",
                "h1.title",
                "h1[data-testid='job-title']",
                ".job-header h1",
                "h1",
            ],
            "company": [
                ".company-name",
                ".company",
                "[data-testid='company-name']",
                ".job-header .company",
            ],
            "location": [
                ".location",
                ".job-location",
                "[data-testid='job-location']",
                ".job-header .location",
            ],
            "description": [
                ".job-description",
                "#job-description",
                ".jd",
                "[data-testid='job-description']",
                "div.description",
            ],
        }

        def find_element(soup, selectors_list):
            for sel in selectors_list:
                el = soup.select_one(sel)
                if el:
                    return el.get_text(strip=True)
            return ""

        title = find_element(soup, selectors["title"])
        company = find_element(soup, selectors["company"])
        location = find_element(soup, selectors["location"])
        description = find_element(soup, selectors["description"])

        if not title and not description:
            return None

        return JobPosting(
            job_title=title or "Unknown",
            company=company or "Unknown",
            location=location or "N/A",
            description=description or "",
        )

    def scrape_search_results(
        self,
        query: str,
        location: str = "",
        max_results: int = 10,
    ) -> List[JobPosting]:
        """Scrape job search results (basic Indeed/LinkedIn simulation)."""
        # Note: Actual implementation would need site-specific logic
        # or use APIs (Indeed API, LinkedIn API)

        # For now, return empty list - requires site-specific implementation
        logger.warning(
            "Generic search not implemented. Use scrape_jd() for specific URLs."
        )
        return []

    def to_vector_format(self, job: JobPosting) -> tuple:
        """Convert JobPosting to vector store format (text, metadata)."""
        text = f"""
Job Title: {job.job_title}
Company: {job.company}
Location: {job.location}
Description: {job.description}
"""

        metadata = {
            "job_title": job.job_title,
            "company": job.company,
            "location": job.location,
            "source_url": job.source_url,
        }

        return text, metadata


def get_scraper() -> JobScraper:
    return JobScraper()
