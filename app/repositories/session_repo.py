"""Session repository.

Provides data access layer for Session entity CRUD operations.
"""

from sqlalchemy.orm import Session as DBSession
from sqlalchemy.exc import IntegrityError
from app.models.session import Session
import uuid


class SessionRepository:
    """Session data access repository.

    Handles all database operations for Session entities including creation,
    retrieval, updates, and deletion scoped to a specific user.

    Attributes:
        db: SQLAlchemy database session
    """

    def __init__(self, db: DBSession):
        self.db = db

    def create_session(self, user_id: str, session_name: str, session_description: str = None) -> Session:
        """Create a new session for a user.

        Args:
            user_id: Owning user UUID
            session_name: Human-readable session name
            session_description: Optional description

        Returns:
            Created Session object

        Raises:
            ValueError: If a constraint violation occurs
        """
        try:
            session = Session(
                session_id=str(uuid.uuid4()),
                user_id=user_id,
                session_name=session_name,
                session_description=session_description,
            )
            self.db.add(session)
            self.db.commit()
            self.db.refresh(session)
            return session
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Session creation failed due to a constraint violation")

    def get_session_by_id(self, session_id: str) -> Session:
        """Retrieve a session by its unique identifier.

        Args:
            session_id: Session UUID

        Returns:
            Session object or None if not found
        """
        return self.db.query(Session).filter(Session.session_id == session_id).first()

    def get_sessions_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> tuple[list[Session], int]:
        """Retrieve all sessions belonging to a user with pagination.

        Args:
            user_id: Owning user UUID
            skip: Number of records to skip
            limit: Maximum records to return

        Returns:
            Tuple of (session list, total count)
        """
        query = self.db.query(Session).filter(Session.user_id == user_id)
        total = query.count()
        sessions = query.order_by(Session.created_at.desc()).offset(skip).limit(limit).all()
        return sessions, total

    def update_session(self, session_id: str, **kwargs) -> Session:
        """Update session fields.

        Args:
            session_id: Session UUID
            **kwargs: Fields to update (session_name, session_description)

        Returns:
            Updated Session object

        Raises:
            ValueError: If session not found
        """
        session = self.get_session_by_id(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        for key, value in kwargs.items():
            if hasattr(session, key) and value is not None:
                setattr(session, key, value)

        self.db.commit()
        self.db.refresh(session)
        return session

    def delete_session(self, session_id: str) -> None:
        """Permanently delete a session.

        Args:
            session_id: Session UUID

        Raises:
            ValueError: If session not found
        """
        session = self.get_session_by_id(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        self.db.delete(session)
        self.db.commit()
