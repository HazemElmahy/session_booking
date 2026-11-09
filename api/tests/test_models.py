from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models import AuthSession, User


def make_user(**overrides) -> User:
    fields = {
        "email": "ana@example.com",
        "password_hash": "not-a-real-hash",
        "name": "Ana",
        "role": "member",
        "timezone": "Europe/Lisbon",
    }
    fields.update(overrides)
    return User(**fields)


def test_user_round_trip(db):
    with db() as session:
        user = make_user()
        session.add(user)
        session.commit()
        user_id = user.id

    with db() as session:
        loaded = session.get(User, user_id)
        assert loaded is not None
        assert loaded.email == "ana@example.com"
        assert loaded.created_at is not None


def test_email_is_unique_ignoring_case(db):
    with db() as session:
        session.add(make_user(email="Ana@Example.com"))
        session.commit()

    with db() as session:
        session.add(make_user(email="ana@example.com"))
        with pytest.raises(IntegrityError):
            session.commit()


def test_role_is_restricted_to_member_or_professional(db):
    with db() as session:
        session.add(make_user(role="admin"))
        with pytest.raises(IntegrityError):
            session.commit()


def test_auth_session_belongs_to_a_user(db):
    with db() as session:
        user = make_user()
        session.add(user)
        session.flush()
        session.add(
            AuthSession(
                token_hash="hash-of-token",
                user_id=user.id,
                expires_at=datetime.now(UTC) + timedelta(days=7),
            )
        )
        session.commit()

    with db() as session:
        auth = session.scalars(select(AuthSession)).one()
        assert auth.user.email == "ana@example.com"
