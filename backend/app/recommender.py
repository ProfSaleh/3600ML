from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import List

from .models import Course


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "with",
    "will",
    "this",
    "you",
    "your",
    "into",
}

DESCRIPTION_WEIGHT = 0.25
OUTCOME_WEIGHT = 0.45
TOPIC_WEIGHT = 0.30


def tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return [token for token in tokens if token not in STOPWORDS and len(token) > 2]


def text_to_vector(text: str) -> Counter:
    return Counter(tokenize(text))


def cosine_similarity(vec_a: Counter, vec_b: Counter) -> float:
    if not vec_a or not vec_b:
        return 0.0

    dot_product = sum(value * vec_b.get(key, 0) for key, value in vec_a.items())
    norm_a = math.sqrt(sum(value * value for value in vec_a.values()))
    norm_b = math.sqrt(sum(value * value for value in vec_b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def top_shared_terms(text_a: str, text_b: str, limit: int = 5) -> list[str]:
    freq_a = text_to_vector(text_a)
    freq_b = text_to_vector(text_b)
    overlaps = {term: min(freq_a[term], freq_b[term]) for term in set(freq_a) & set(freq_b)}
    ranked = sorted(overlaps.items(), key=lambda item: (-item[1], item[0]))
    return [term for term, _ in ranked[:limit]]


@dataclass
class RecommendationScore:
    course: Course
    overall_score: float
    description_score: float
    learning_outcome_score: float
    weekly_topic_score: float
    explanation: str


def rank_courses_for_sections(
    description: str,
    outcomes_text: str,
    weekly_topics_text: str,
    courses: List[Course],
    top_n: int = 5,
) -> List[RecommendationScore]:
    description_vector = text_to_vector(description)
    outcomes_vector = text_to_vector(outcomes_text)
    topics_vector = text_to_vector(weekly_topics_text)

    recommendations: List[RecommendationScore] = []

    for course in courses:
        course_description_vec = text_to_vector(course.description_text)
        course_outcomes_vec = text_to_vector(course.outcomes_text)
        course_topics_vec = text_to_vector(course.weekly_topics_text)

        description_score = cosine_similarity(description_vector, course_description_vec)
        learning_outcome_score = cosine_similarity(outcomes_vector, course_outcomes_vec)
        weekly_topic_score = cosine_similarity(topics_vector, course_topics_vec)

        overall_score = (
            (DESCRIPTION_WEIGHT * description_score)
            + (OUTCOME_WEIGHT * learning_outcome_score)
            + (TOPIC_WEIGHT * weekly_topic_score)
        )

        shared_description = top_shared_terms(description, course.description_text, limit=4)
        shared_outcomes = top_shared_terms(outcomes_text, course.outcomes_text, limit=4)
        shared_topics = top_shared_terms(weekly_topics_text, course.weekly_topics_text, limit=4)
        evidence = [*shared_outcomes[:2], *shared_topics[:2], *shared_description[:1]]
        evidence_text = ", ".join(dict.fromkeys(evidence)) if evidence else "general thematic overlap"
        explanation = (
            f"Strongest overlap in learning outcomes and weekly topics. "
            f"Shared terms: {evidence_text}."
        )

        recommendations.append(
            RecommendationScore(
                course=course,
                overall_score=overall_score,
                description_score=description_score,
                learning_outcome_score=learning_outcome_score,
                weekly_topic_score=weekly_topic_score,
                explanation=explanation,
            )
        )

    recommendations.sort(key=lambda item: item.overall_score, reverse=True)
    return recommendations[:top_n]
