from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.modules.auth.model import User, UserSession


class AuthRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def find_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.db.execute(stmt).scalar_one_or_none()

    def find_user_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def create_session(
        self,
        *,
        user_id: int,
        refresh_token_hash: str,
        expires_at: datetime,
        ip_address: str | None,
        user_agent: str | None,
    ) -> UserSession:
        session = UserSession(
            user_id=user_id,
            refresh_token_hash=refresh_token_hash,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent,
            created_at=datetime.utcnow(),
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def find_session_by_refresh_hash(self, refresh_token_hash: str) -> UserSession | None:
        stmt = select(UserSession).where(UserSession.refresh_token_hash == refresh_token_hash)
        return self.db.execute(stmt).scalar_one_or_none()

    def delete_session_by_refresh_hash(self, refresh_token_hash: str) -> None:
        stmt = delete(UserSession).where(UserSession.refresh_token_hash == refresh_token_hash)
        self.db.execute(stmt)
        self.db.commit()

    def update_last_login_at(self, user: User, login_at: datetime) -> None:
        user.last_login_at = login_at
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

