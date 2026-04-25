from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from typing import Optional
import logging
import asyncio

logger = logging.getLogger(__name__)

SELECTORS = {
    "default": {
        "title": "h1, .title, [class*='title']",
        "company": ".company-name, .company, [class*='company']",
        "location": ".location, [class*='location']",
        "description": ".description, .content, [class*='description']",
        "requirements": ".requirement, [class*='requirement']",
        "salary": ".salary, [class*='salary']",
    },
    "topcv.vn": {
        "title": "h1.title, .job-title-main, [class*='job-title']",
        "company": ".company-name, .company, [class*='company']",
        "location": ".location, [class*='location']",
        "description": ".job-description, .jd-content, .content-more, [class*='description']",
        "requirements": ".requirement, [class*='requirement']",
        "salary": ".salary, [class*='salary']",
    }
}

def _extract_jd(soup: BeautifulSoup, url: str) -> dict:
    """Extract JD fields from HTML using site-specific selectors."""
    from urllib.parse import urlparse
    site = urlparse(url).netloc.replace("www.", "")
    
    selectors = SELECTORS.get(site, SELECTORS.get("default"))
    
    title = _find_first(soup, selectors.get("title", "h1"))
    company = _find_first(soup, selectors.get("company", "[class*='company']"))
    location = _find_first(soup, selectors.get("location", ""))
    description = _find_first(soup, selectors.get("description", ""))
    requirements = _find_first(soup, selectors.get("requirements", ""))
    salary = _find_first(soup, selectors.get("salary", ""))
    
    return {
        "title": title or "Unknown",
        "company": company or "Unknown",
        "location": location or "N/A",
        "description": description or "",
        "requirements": requirements or "",
        "salary": salary or "Negotiable",
    }

def _find_first(soup: BeautifulSoup, selectors: str) -> Optional[str]:
    """Find first matching element and return its text."""
    if not selectors:
        return None
    for sel in selectors.split(", "):
        el = soup.select_one(sel.strip())
        if el:
            return el.get_text(strip=True)
    return None

async def scrape(url: str, timeout: int = 30000) -> dict:
    """Scrape JD from URL using Playwright for JavaScript-rendered content."""
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, wait_until="networkidle", timeout=timeout)
            content = await page.content()
            await browser.close()
        
        soup = BeautifulSoup(content, "lxml")
        return _extract_jd(soup, url)
        
    except asyncio.TimeoutError:
        logger.error(f"Timeout scraping {url}")
        return {"error": "Timeout - page took too long to load"}
    except Exception as e:
        logger.error(f"Failed to scrape {url}: {e}")
        return {"error": str(e)}

def scrape_sync(url: str, timeout: int = 30000) -> dict:
    """Synchronous wrapper for scrape."""
    return asyncio.run(scrape(url, timeout))