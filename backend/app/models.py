from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Syllabus(Base):
    __tablename__ = "syllabi"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    faculty_name: Mapped[str] = mapped_column(String(255), nullable=False)
    department: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    stored_path: Mapped[str] = mapped_column(String(500), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    description_text: Mapped[str] = mapped_column(Text, default="")
    outcomes_text: Mapped[str] = mapped_column(Text, default="")
    weekly_topics_text: Mapped[str] = mapped_column(Text, default="")

    runs: Mapped[list["RecommendationRun"]] = relationship(
        back_populates="syllabus", cascade="all, delete-orphan"
    )


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    provider_course_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    provider: Mapped[str] = mapped_column(String(64), default="coursera")
    partner_name: Mapped[str] = mapped_column(String(255), default="")
    level: Mapped[str] = mapped_column(String(120), default="Mixed")
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    description_text: Mapped[str] = mapped_column(Text, default="")
    outcomes_text: Mapped[str] = mapped_column(Text, default="")
    weekly_topics_text: Mapped[str] = mapped_column(Text, default="")

    recommendation_results: Mapped[list["RecommendationResult"]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )


class RecommendationRun(Base):
    __tablename__ = "recommendation_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    syllabus_id: Mapped[int] = mapped_column(ForeignKey("syllabi.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(32), default="completed")
    weight_description: Mapped[float] = mapped_column(Float, default=0.25)
    weight_learning_outcome: Mapped[float] = mapped_column(Float, default=0.45)
    weight_weekly_topic: Mapped[float] = mapped_column(Float, default=0.30)
    top_n: Mapped[int] = mapped_column(Integer, default=5)

    syllabus: Mapped[Syllabus] = relationship(back_populates="runs")
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
