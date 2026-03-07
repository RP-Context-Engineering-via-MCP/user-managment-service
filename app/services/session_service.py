"""Session business logic service.

Provides high-level session operations including creation,
retrieval, updates, and deletion scoped to a user.
"""

from sqlalchemy.orm import Session as DBSession
from app.repositories.session_repo import SessionRepository
from app.repositories.user_repo import UserRepository
from app.schemas.session_dto import SessionCreateRequest, SessionUpdateRequest
from app.models.session import Session


class SessionService:
    """Session business logic service.

    Orchestrates session operations and enforces ownership rules.

    Attributes:
        repo: Session repository
        user_repo: User repository (for existence checks)
    """

    def __init__(self, db: DBSession):
        self.repo = SessionRepository(db)
        self.user_repo = UserRepository(db)

    def _require_user(self, user_id: str):
        """Ensure user exists, raise ValueError if not."""
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

    def create_session(self, user_id: str, data: SessionCreateRequest) -> Session:
        """Create a new session for a user.

        Args:
            user_id: Owning user UUID
            data: Session creation request

        Returns:
            Created Session object

        Raises:
            ValueError: If user does not exist
        """
        self._require_user(user_id)
        return self.repo.create_session(
            user_id=user_id,
            session_name=data.session_name,
            session_description=data.session_description,
        )

    def get_session(self, session_id: str, user_id: str) -> Session:
        """Retrieve a session, verifying it belongs to the given user.

        Args:
            session_id: Session UUID
            user_id: Requesting user UUID

        Returns:
            Session object

        Raises:
            ValueError: If session not found or does not belong to user
        """
        session = self.repo.get_session_by_id(session_id)
        if not session or session.user_id != user_id:
            raise ValueError(f"Session {session_id} not found")
        return session

    def list_sessions(self, user_id: str, skip: int = 0, limit: int = 100) -> tuple[list[Session], int]:
        """List all sessions for a user with pagination.

        Args:
            user_id: Owning user UUID
            skip: Pagination offset
            limit: Maximum records to return

        Returns:
            Tuple of (session list, total count)
        """
        self._require_user(user_id)
        return self.repo.get_sessions_by_user(user_id, skip=skip, limit=limit)

    def update_session(self, session_id: str, user_id: str, data: SessionUpdateRequest) -> Session:
        """Update a session's fields.

        Args:
            session_id: Session UUID
            user_id: Requesting user UUID
            data: Fields to update

        Returns:
            Updated Session object

        Raises:
            ValueError: If session not found or does not belong to user
        """
        session = self.get_session(session_id, user_id)
        update_fields = data.dict(exclude_none=True)
        return self.repo.update_session(session.session_id, **update_fields)

    def delete_session(self, session_id: str, user_id: str) -> None:
        """Delete a session.

        Args:
            session_id: Session UUID
            user_id: Requesting user UUID

        Raises:
            ValueError: If session not found or does not belong to user
        """
        session = self.get_session(session_id, user_id)
        self.repo.delete_session(session.session_id)
