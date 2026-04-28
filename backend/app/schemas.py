from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreateRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=255)
    department: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    department: str
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class SectionedSyllabus(BaseModel):
    description: str
    learning_outcomes: list[str]
    weekly_topics: list[str]


class UploadSyllabusResponse(BaseModel):
    syllabus_id: int
    parsed: SectionedSyllabus


class CatalogIngestRequest(BaseModel):
    source: str = Field(default="json_feed", pattern="^(json_feed|coursera_api)$")
    feed_path: str | None = None


class CatalogIngestResponse(BaseModel):
    ingestion_run_id: int
    source: str
    status: str
    ingested_count: int
    created_count: int
    updated_count: int
    error_message: str


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


class RecommendationRunSummary(BaseModel):
    id: int
    syllabus_id: int
    created_at: datetime
    top_n: int
    status: str


class CourseSummary(BaseModel):
    id: int
    provider_course_id: str
    title: str
    partner_name: str
    level: str
    language_code: str
    url: str
    is_active: bool

