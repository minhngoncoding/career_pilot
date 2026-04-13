from pydantic import BaseModel, Field, field_validator
from typing import Optional


SUPPORTED_INTENTS = [
    "CV_ANALYSIS",
    "JOB_MATCH",
    "SKILL_GAP",
    "CV_GENERATOR",
    "INTERVIEW",
    "GREETING",
]


class IntentParameters(BaseModel):
    cv_text: Optional[str] = Field(
        default=None, description="Extracted CV text from user message"
    )
    target_jd: Optional[str] = Field(
        default=None, description="Job description if provided by user"
    )
    target_position: Optional[str] = Field(
        default=None, description="Target job role if mentioned"
    )
    target_company: Optional[str] = Field(
        default=None, description="Target company if mentioned"
    )


class IntentDetection(BaseModel):
    intent: str = Field(..., description="Detected user intent")
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence score from 0.0 to 1.0"
    )
    parameters: IntentParameters = Field(
        default_factory=IntentParameters,
        description="Extracted parameters from user message",
    )

    @field_validator("intent")
    @classmethod
    def validate_intent(cls, v: str) -> str:
        if v not in SUPPORTED_INTENTS:
            raise ValueError(
                f"Invalid intent: '{v}'. Must be one of {SUPPORTED_INTENTS}"
            )
        return v


# CV Analyzer models
class CVAnalysis(BaseModel):
    score: int = Field(..., ge=1, le=10, description="Overall CV score from 1 to 10")
    strengths: list[str] = Field(
        default_factory=list, description="List of CV strengths"
    )
    improvements: list[str] = Field(
        default_factory=list, description="Areas that need improvement"
    )
    recommendations: list[str] = Field(
        default_factory=list, description="Actionable recommendations"
    )


# Job Matcher models
class JobMatchItem(BaseModel):
    rank: int = Field(..., description="Match rank")
    job_title: str = Field(..., description="Job title")
    company: str = Field(default="", description="Company name")
    match_score: float = Field(..., ge=0.0, le=1.0, description="Match percentage")
    matched_skills: list[str] = Field(
        default_factory=list, description="Skills that match"
    )
    missing_skills: list[str] = Field(
        default_factory=list, description="Missing skills"
    )
    jd_summary: str = Field(default="", description="Job description summary")


class JobMatch(BaseModel):
    matches: list[JobMatchItem] = Field(
        default_factory=list, description="List of matched jobs"
    )
    recommendations: list[str] = Field(
        default_factory=list, description="Overall recommendations"
    )


# Skill Gap models
class SkillGapItem(BaseModel):
    skill: str = Field(..., description="Skill name")
    priority: str = Field(..., description="Priority: high, medium, low")
    gap_level: str = Field(..., description="Gap level: missing, partial, advanced")
    resources: list[str] = Field(default_factory=list, description="Learning resources")


class SkillGapAnalysis(BaseModel):
    current_skills: list[str] = Field(
        default_factory=list, description="Skills from CV"
    )
    required_skills: list[str] = Field(
        default_factory=list, description="Skills for target role"
    )
    skill_gaps: list[SkillGapItem] = Field(
        default_factory=list, description="Identified skill gaps"
    )
    roadmap: list[str] = Field(default_factory=list, description="Learning roadmap")
    timeline: str = Field(default="", description="Suggested timeline")


# CV Generator models
class GeneratedCV(BaseModel):
    content: str = Field(..., description="Generated CV in markdown format")
    optimization_notes: list[str] = Field(
        default_factory=list, description="Notes about optimizations made"
    )


# Interview models
class InterviewQuestion(BaseModel):
    question: str = Field(..., description="Interview question")
    question_type: str = Field(..., description="Type: behavioral, technical, company")
    sample_answer: Optional[str] = Field(
        default=None, description="Sample answer for reference"
    )


class InterviewFeedback(BaseModel):
    question: str = Field(..., description="Question asked")
    answer: str = Field(..., description="User's answer")
    feedback: str = Field(..., description="Feedback on the answer")
    score: float = Field(..., ge=0.0, le=10.0, description="Score from 0 to 10")
    strengths: list[str] = Field(
        default_factory=list, description="Strengths in answer"
    )
    improvements: list[str] = Field(
        default_factory=list, description="Areas to improve"
    )


class InterviewSession(BaseModel):
    position: str = Field(..., description="Interview position")
    questions: list[InterviewQuestion] = Field(
        default_factory=list, description="Interview questions"
    )
    question_history: list[InterviewFeedback] = Field(
        default_factory=list, description="History of questions and feedback"
    )
    total_questions: int = Field(default=0, description="Total questions asked")
    overall_score: float = Field(default=0.0, description="Overall interview score")
    is_active: bool = Field(
        default=True, description="Whether interview is still active"
    )
