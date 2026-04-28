from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .config import settings
from .database import Base, embedding_column_type


class SectionType(str, Enum):
    DESCRIPTION = "description"
    LEARNING_OUTCOME = "learning_outcome"
    WEEKLY_TOPIC = "weekly_topic"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    department: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    syllabi: Mapped[list["Syllabus"]] = relationship(back_populates="uploaded_by")
    recommendation_runs: Mapped[list["RecommendationRun"]] = relationship(
        back_populates="requested_by"
    )
    ingestion_runs: Mapped[list["CatalogIngestionRun"]] = relationship(
        back_populates="triggered_by"
    )


class Syllabus(Base):
    __tablename__ = "syllabi"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uploaded_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    stored_path: Mapped[str] = mapped_column(String(500), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    description_text: Mapped[str] = mapped_column(Text, default="")
    outcomes_text: Mapped[str] = mapped_column(Text, default="")
    weekly_topics_text: Mapped[str] = mapped_column(Text, default="")
    description_embedding: Mapped[list[float] | None] = mapped_column(
        embedding_column_type(settings.embedding_dimensions), nullable=True
    )
    outcomes_embedding: Mapped[list[float] | None] = mapped_column(
        embedding_column_type(settings.embedding_dimensions), nullable=True
    )
    weekly_topics_embedding: Mapped[list[float] | None] = mapped_column(
        embedding_column_type(settings.embedding_dimensions), nullable=True
    )

    uploaded_by: Mapped[User] = relationship(back_populates="syllabi")
    runs: Mapped[list["RecommendationRun"]] = relationship(
        back_populates="syllabus", cascade="all, delete-orphan"
    )


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    provider: Mapped[str] = mapped_column(String(64), default="coursera")
    provider_course_id: Mapped[str] = mapped_column(String(128), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    partner_name: Mapped[str] = mapped_column(String(255), default="")
    level: Mapped[str] = mapped_column(String(120), default="Mixed")
    language_code: Mapped[str] = mapped_column(String(24), default="en")
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    description_text: Mapped[str] = mapped_column(Text, default="")
    outcomes_text: Mapped[str] = mapped_column(Text, default="")
    weekly_topics_text: Mapped[str] = mapped_column(Text, default="")
    description_embedding: Mapped[list[float] | None] = mapped_column(
        embedding_column_type(settings.embedding_dimensions), nullable=True
    )
    outcomes_embedding: Mapped[list[float] | None] = mapped_column(
        embedding_column_type(settings.embedding_dimensions), nullable=True
    )
    weekly_topics_embedding: Mapped[list[float] | None] = mapped_column(
        embedding_column_type(settings.embedding_dimensions), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    __table_args__ = (
        UniqueConstraint("provider", "provider_course_id", name="uq_provider_course"),
    )

    recommendation_results: Mapped[list["RecommendationResult"]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )


class CatalogIngestionRun(Base):
    __tablename__ = "catalog_ingestion_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    provider: Mapped[str] = mapped_column(String(64), default="coursera")
    source: Mapped[str] = mapped_column(String(64), default="json_feed")
    status: Mapped[str] = mapped_column(String(32), default="completed")
    ingested_count: Mapped[int] = mapped_column(Integer, default=0)
    created_count: Mapped[int] = mapped_column(Integer, default=0)
    updated_count: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str] = mapped_column(Text, default="")
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    triggered_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    triggered_by: Mapped[User] = relationship(back_populates="ingestion_runs")


class RecommendationRun(Base):
    __tablename__ = "recommendation_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    syllabus_id: Mapped[int] = mapped_column(ForeignKey("syllabi.id"), nullable=False)
    requested_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(32), default="completed")
    weight_description: Mapped[float] = mapped_column(Float, default=0.25)
    weight_learning_outcome: Mapped[float] = mapped_column(Float, default=0.45)
    weight_weekly_topic: Mapped[float] = mapped_column(Float, default=0.30)
    top_n: Mapped[int] = mapped_column(Integer, default=5)

    syllabus: Mapped[Syllabus] = relationship(back_populates="runs")
    requested_by: Mapped[User] = relationship(back_populates="recommendation_runs")
    results: Mapped[list["RecommendationResult"]] = relationship(
        back_populates="run", cascade="all, delete-orphan"
    )


class RecommendationResult(Base):
    __tablename__ = "recommendation_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("recommendation_runs.id"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    overall_score: Mapped[float] = mapped_column(Float, nullable=False)
    description_score: Mapped[float] = mapped_column(Float, nullable=False)
    learning_outcome_score: Mapped[float] = mapped_column(Float, nullable=False)
    weekly_topic_score: Mapped[float] = mapped_column(Float, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, default="")

    run: Mapped[RecommendationRun] = relationship(back_populates="results")
    course: Mapped[Course] = relationship(back_populates="recommendation_results")
