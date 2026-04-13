from career_pilot.core.llm import CareerPilotLLM
from career_pilot.agents.models import CVAnalysis
from career_pilot.prompts import CV_ANALYZER_SYSTEM, CV_ANALYZER_USER


class CVAnalyzer:
    def __init__(self):
        self._llm = CareerPilotLLM(temperature=0.1)

    @property
    def llm(self):
        return self._llm.with_structured_output(CVAnalysis)

    def analyze_cv(self, cv_text: str, user_request: str = "") -> str:
        """Analyze CV and return formatted string for user."""
        prompt = CV_ANALYZER_USER.format(cv_text=cv_text, user_request=user_request)
        result = self.llm.invoke(CV_ANALYZER_SYSTEM + "\n\n" + prompt)

        # Format immediately and return string
        return self._format(result)

    def _format(self, result: CVAnalysis) -> str:
        """Format CVAnalysis into user-friendly message."""
        score = result.score
        score_emoji = "🟢" if score >= 8 else "🟡" if score >= 6 else "🔴"

        response = "## 📊 CV Analysis Result\n\n"
        response += f"**Overall Score:** {score_emoji} **{score}/10**\n\n"

        if result.strengths:
            response += "### ✅ Strengths\n"
            for s in result.strengths:
                response += f"• {s}\n"
            response += "\n"

        if result.improvements:
            response += "### ⚠️ Areas for Improvement\n"
            for i in result.improvements:
                response += f"• {i}\n"
            response += "\n"

        if result.recommendations:
            response += "### 💡 Recommendations\n"
            for r in result.recommendations:
                response += f"• {r}\n"

        return response
