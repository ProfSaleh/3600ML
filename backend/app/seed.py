from sqlalchemy.orm import Session

from .models import Course


SAMPLE_COURSES = [
    {
        "provider_course_id": "google-project-management",
        "title": "Foundations of Project Management",
        "url": "https://www.coursera.org/learn/project-management-foundations",
        "partner_name": "Google",
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
    {
        "provider_course_id": "michigan-python-data",
        "title": "Applied Data Science with Python",
        "url": "https://www.coursera.org/specializations/data-science-python",
        "partner_name": "University of Michigan",
        "description": (
            "Develop practical Python skills for data wrangling, analysis, and "
            "visualization in real-world settings."
        ),
        "learning_outcomes": [
            "Use pandas for data cleaning and transformation.",
            "Perform exploratory data analysis and visualization.",
            "Build reproducible analytical workflows in Python.",
        ],
        "weekly_topics": [
            "Python for tabular data",
            "Data cleaning with pandas",
            "Visualization with matplotlib and seaborn",
            "Applied analysis projects",
        ],
    },
    {
        "provider_course_id": "duke-ai-product-management",
        "title": "AI Product Management",
        "url": "https://www.coursera.org/learn/ai-product-management-duke",
        "partner_name": "Duke University",
        "description": (
            "Learn to scope, design, and evaluate AI-enabled products with a focus "
            "on value, data, and model constraints."
        ),
        "learning_outcomes": [
            "Define AI product opportunities and constraints.",
            "Assess data readiness for AI applications.",
            "Measure product outcomes and iteration strategies.",
        ],
        "weekly_topics": [
            "AI opportunity identification",
            "Data strategy and feasibility",
            "Model performance and product KPIs",
            "Responsible AI and product iteration",
        ],
    },
]


def seed_courses_if_empty(session: Session) -> int:
    existing = session.query(Course).count()
    if existing > 0:
        return existing

    for course_payload in SAMPLE_COURSES:
        course = Course(
            provider_course_id=course_payload["provider_course_id"],
            title=course_payload["title"],
            url=course_payload["url"],
            partner_name=course_payload["partner_name"],
            level=course_payload.get("level", "Mixed"),
            is_active=True,
            description_text=course_payload["description"],
            outcomes_text="\n".join(course_payload["learning_outcomes"]),
            weekly_topics_text="\n".join(course_payload["weekly_topics"]),
        )
        session.add(course)

    session.commit()
    return session.query(Course).count()
