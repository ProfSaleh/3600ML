from pydantic import BaseModel, Field


class SectionedSyllabus(BaseModel):
    description: str
    learning_outcomes: list[str]
    weekly_topics: list[str]


class UploadSyllabusResponse(BaseModel):
    syllabus_id: int
    parsed: SectionedSyllabus


class CourseRecommendation(BaseModel):
    rank: int
    course_id: int
    title: str
    provider: str
    partner_name: str
    level: str
    url: str
    overall_score: float = Field(ge=0.0, le=1.0)
    description_score: float = Field(ge=0.0, le=1.0)
    learning_outcome_score: float = Field(ge=0.0, le=1.0)
    weekly_topic_score: float = Field(ge=0.0, le=1.0)
    explanation: str


class RecommendationResponse(BaseModel):
    run_id: int
    syllabus_id: int
    top_n: int
    weights: dict[str, float]
    recommendations: list[CourseRecommendation]

