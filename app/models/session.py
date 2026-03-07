"""Session domain model.

Defines the Session entity linked to a User (one user -> many sessions).
"""

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Session(Base):
    """Session entity representing a user session.

    Attributes:
        session_id: Unique identifier (UUID format)
        session_name: Human-readable name for the session
        session_description: Optional description of the session
        created_at: Timestamp when the session was created
        user_id: Foreign key referencing the owning user
    """

    __tablename__ = "session"

    session_id = Column(String(36), primary_key=True, index=True)
    session_name = Column(String(255), nullable=False)
    session_description = Column(String(1000), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user_id = Column(String(36), ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False, index=True)

    user = relationship("User", back_populates="sessions")

    def __repr__(self):
        return f"<Session(session_id={self.session_id}, session_name={self.session_name}, user_id={self.user_id})>"
