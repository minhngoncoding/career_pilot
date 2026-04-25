import pytest
from career_pilot.agents.router import extract_url, has_url


class TestRouterUrlExtraction:
    """Test URL extraction in router."""

    def test_extract_url_simple(self):
        """Test extracting simple URL."""
        text = "Check this job https://topcv.vn/job/12345"
        assert extract_url(text) == "https://topcv.vn/job/12345"

    def test_extract_url_with_path(self):
        """Test extracting URL with full path."""
        text = "https://www.topcv.vn/viec-lam/developer-python/abc123"
        assert extract_url(text) == "https://www.topcv.vn/viec-lam/developer-python/abc123"

    def test_extract_url_none(self):
        """Test no URL in text."""
        text = "Analyze my CV please"
        assert extract_url(text) is None

    def test_has_url_true(self):
        """Test has_url returns True."""
        assert has_url("https://topcv.vn/job/123")

    def test_has_url_false(self):
        """Test has_url returns False."""
        assert not has_url("Analyze my CV")