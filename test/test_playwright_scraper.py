import pytest
from career_pilot.tools.playwright_scraper import (
    scrape_sync,
    scrape,
    _extract_jd,
    SELECTORS,
)
from bs4 import BeautifulSoup


class TestPlaywrightScraper:
    """Test Playwright scraper functionality."""

    def test_selectors_defined(self):
        """Test that selectors are defined."""
        assert "topcv.vn" in SELECTORS
        assert "default" in SELECTORS
        assert "title" in SELECTORS["topcv.vn"]
        assert "description" in SELECTORS["topcv.vn"]

    def test_extract_jd_with_sample_html(self):
        """Test extraction from sample HTML."""
        html = """
        <html>
            <body>
                <h1 class="title">Senior Python Developer</h1>
                <div class="company-name">TechCorp Vietnam</div>
                <div class="location">Ho Chi Minh City</div>
                <div class="job-description">
                    We are looking for a Python developer with 3+ years experience.
                </div>
                <div class="salary">20-30 million VND</div>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, "lxml")
        result = _extract_jd(soup, "https://topcv.vn/job/test")

        assert result["title"] == "Senior Python Developer"
        assert result["company"] == "TechCorp Vietnam"
        assert result["location"] == "Ho Chi Minh City"
        assert "Python developer" in result["description"]
        assert result["salary"] == "20-30 million VND"

    def test_extract_jd_missing_fields(self):
        """Test extraction with missing fields."""
        html = "<html><body><h1 class='title'>Job Title</h1></body></html>"
        soup = BeautifulSoup(html, "lxml")
        result = _extract_jd(soup, "https://topcv.vn/job/test")

        assert result["title"] == "Job Title"
        assert result["company"] == "Unknown"

    def test_extract_jd_fallback_to_default(self):
        """Test fallback to default selectors for unknown site."""
        html = "<html><body><h1>My Job Title</h1><p>Description here</p></body></html>"
        soup = BeautifulSoup(html, "lxml")
        result = _extract_jd(soup, "https://unknown-site.com/job")

        assert result["title"] == "My Job Title"

    def test_scrape_sync_with_example(self):
        """Test sync scrape with example.com (static page)."""
        result = scrape_sync("https://example.com", timeout=5000)
        assert isinstance(result, dict)
        assert "title" in result or "error" in result