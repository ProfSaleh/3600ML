from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from .auth import hash_password
from .config import settings
from .models import User


def ensure_bootstrap_admin(session: Session) -> None:
    if not settings.bootstrap_admin_email or not settings.bootstrap_admin_password:
        return

    existing = session.scalar(
        select(User).where(User.email == settings.bootstrap_admin_email.lower())
    )
    if existing:
        return

    admin = User(
        email=settings.bootstrap_admin_email.lower(),
        full_name=settings.bootstrap_admin_name,
        department=settings.bootstrap_admin_department,
        password_hash=hash_password(settings.bootstrap_admin_password),
        is_admin=True,
    )
    session.add(admin)
    session.commit()
