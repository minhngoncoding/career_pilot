from typing import Optional, List
from pydantic import BaseModel
from career_pilot.core.llm import CareerPilotLLM
from career_pilot.prompts.prompt_templates import (
    JOB_MATCHER_SYSTEM,
    JOB_MATCHER_USER,
)
from career_pilot.tools.vector_store import get_jd_store


class JobMatch(BaseModel):
    """Single job match result."""

    rank: int
    job_title: str
    company: str
    location: str
    match_score: int  # 0-100
    matched_skills: List[str]
    missing_skills: List[str]
    jd_summary: str


class JobMatchResult(BaseModel):
    """Job matching result."""

    matches: List[JobMatch]
    recommendations: str


class JobMatcher:
    """Job matching agent - matches CV to stored job descriptions."""

    def __init__(self):
        self._llm = CareerPilotLLM(temperature=0.3)
        self._jd_store = get_jd_store()

    @property
    def llm(self):
        return self._llm.with_structured_output(JobMatchResult)

    def match(
        self,
        cv_text: str,
        target_role: Optional[str] = None,
        location: Optional[str] = None,
        top_k: int = 5,
    ) -> JobMatchResult:
        """Match CV to available jobs in vector store."""
        # Search for relevant JDs
        query = target_role or cv_text
        jd_results = self._jd_store.search(query, top_k=top_k)

        if not jd_results:
            return self._no_jobs_found(cv_text, target_role, location)

        # Build JD text for matching
        jd_text = self._format_jds(jd_results)

        # Call LLM for matching
        prompt = JOB_MATCHER_USER.format(
            cv_text=cv_text,
            target_role=target_role or "",
            location=location or "",
        )

        try:
            result = self.llm.invoke(
                JOB_MATCHER_SYSTEM + "\n\n" + jd_text + "\n\n" + prompt
            )
            return result
        except Exception:
            return self._fallback_match(jd_results, cv_text)

    def _format_jds(self, jd_results: List[dict]) -> str:
        """Format JD results for LLM context."""
        formatted = []
        for i, jd in enumerate(jd_results, 1):
            meta = jd.get("metadata", {})
            formatted.append(
                f"\n--- Job {i} ---\n"
                f"Title: {meta.get('job_title', 'N/A')}\n"
                f"Company: {meta.get('company', 'N/A')}\n"
                f"Location: {meta.get('location', 'N/A')}\n"
                f"Description:\n{jd.get('text', '')}"
            )
        return "\n".join(formatted)

    def _no_jobs_found(
        self,
        cv_text: str,
        target_role: Optional[str],
        location: Optional[str],
    ) -> JobMatchResult:
        """Handle when no jobs found in vector store."""
        recommendations = (
            "No job descriptions found in the database. "
            "To get job matches:\n"
            "1. Add job descriptions using the admin panel\n"
            "2. Scrape jobs from job sites\n"
            "3. Specify a target role for broader search"
        )
        if target_role:
            location_str = f" in {location}" if location else ""
            recommendations += f"\n\nLooking for: {target_role}{location_str}"

        return JobMatchResult(matches=[], recommendations=recommendations)

    def _fallback_match(self, jd_results: List[dict], cv_text: str) -> JobMatchResult:
        """Simple keyword-based fallback matching."""
        cv_lower = cv_text.lower()
        matches = []

        for i, jd in enumerate(jd_results, 1):
            jd_text = jd.get("text", "").lower()
            meta = jd.get("metadata", {})

            # Simple keyword overlap
            cv_words = set(cv_lower.split())
            jd_words = set(jd_text.split())
            matched = cv_words & jd_words
            missing = jd_words - cv_words

            # Calculate score
            score = int(len(matched) / len(jd_words) * 100) if jd_words else 0

            matches.append(
                JobMatch(
                    rank=i,
                    job_title=meta.get("job_title", "Unknown"),
                    company=meta.get("company", "Unknown"),
                    location=meta.get("location", "N/A"),
                    match_score=min(score, 100),
                    matched_skills=list(matched)[:5],
                    missing_skills=list(missing)[:5],
                    jd_summary=jd_text[:200],
                )
            )

        return JobMatchResult(
            matches=matches,
            recommendations="Found jobs. Review matches above.",
        )

    def add_jobs(self, jd_list: List[tuple]) -> List[str]:
        """Add jobs to vector store. Format: [(jd_text, metadata_dict), ...]"""
        return self._jd_store.add_jds(jd_list)


def get_job_matcher() -> JobMatcher:
    return JobMatcher()
