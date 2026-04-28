from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from .embedding import embed_text
from .models import Course


SAMPLE_COURSES = [
    {
        "provider_course_id": "google-project-management",
        "title": "Foundations of Project Management",
        "url": "https://www.coursera.org/learn/project-management-foundations",
        "partner_name": "Google",
        "level": "Beginner",
        "description": (
            "Learn project management fundamentals including stakeholder management, "
            "project lifecycle, scheduling, and communication."
        ),
        "learning_outcomes": [
            "Define the project lifecycle and key project roles.",
            "Apply project planning techniques using schedules and milestones.",
            "Explain stakeholder communication strategies.",
        ],
        "weekly_topics": [
            "Introduction to project management",
            "Project lifecycle phases",
            "Stakeholder and communication planning",
            "Building timelines and schedules",
        ],
    },
    {
        "provider_course_id": "ibm-data-science-methodology",
        "title": "Data Science Methodology",
        "url": "https://www.coursera.org/learn/data-science-methodology",
        "partner_name": "IBM",
        "level": "Intermediate",
        "description": (
            "Explore end-to-end data science workflows from problem definition to "
            "model evaluation and communication."
        ),
        "learning_outcomes": [
            "Frame business problems as data science questions.",
            "Evaluate analytical methods for a given dataset.",
            "Communicate insights to decision makers.",
        ],
        "weekly_topics": [
            "Business understanding and analytics framing",
            "Data requirements and collection",
            "Modeling and evaluation basics",
            "Communicating data science results",
        ],
    },
    {
        "provider_course_id": "illinois-digital-marketing",
        "title": "Digital Marketing Analytics in Practice",
        "url": "https://www.coursera.org/learn/digital-marketing-analytics-practice",
        "partner_name": "University of Illinois",
        "level": "Intermediate",
        "description": (
            "Use analytics tools and experimentation to improve digital marketing "
            "performance across channels."
        ),
        "learning_outcomes": [
            "Interpret web and campaign analytics metrics.",
            "Design A/B tests for marketing decisions.",
            "Develop data-driven channel strategies.",
        ],
        "weekly_topics": [
            "Marketing metrics and dashboards",
            "Attribution and customer funnels",
            "Experimentation and A/B testing",
            "Optimization using analytics insights",
        ],
    },
]


def seed_courses_if_empty(session: Session) -> int:
    existing = session.scalar(select(Course).limit(1))
    if existing:
        return session.query(Course).count()

    for payload in SAMPLE_COURSES:
        course = Course(
            provider="coursera",
            provider_course_id=payload["provider_course_id"],
            title=payload["title"],
            url=payload["url"],
            partner_name=payload["partner_name"],
            level=payload["level"],
            is_active=True,
            description_text=payload["description"],
            outcomes_text="\n".join(payload["learning_outcomes"]),
            weekly_topics_text="\n".join(payload["weekly_topics"]),
        )
        course.description_embedding = embed_text(course.description_text)
        course.outcomes_embedding = embed_text(course.outcomes_text)
        course.weekly_topics_embedding = embed_text(course.weekly_topics_text)
        session.add(course)

    session.commit()
    return session.query(Course).count()
