"""Session data transfer objects.

Provides Pydantic schemas for session-related API requests and responses.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class SessionCreateRequest(BaseModel):
    """Session creation request schema.

    Attributes:
        session_name: Human-readable name for the session (required)
        session_description: Optional description of the session
    """
    session_name: str = Field(..., min_length=1, max_length=255)
    session_description: Optional[str] = Field(None, max_length=1000)


class SessionUpdateRequest(BaseModel):
    """Session update request schema.

    All fields are optional for partial updates.

    Attributes:
        session_name: Updated session name
        session_description: Updated session description
    """
    session_name: Optional[str] = Field(None, min_length=1, max_length=255)
    session_description: Optional[str] = Field(None, max_length=1000)


class SessionResponse(BaseModel):
    """Session response schema.

    Attributes:
        session_id: Unique session identifier (UUID)
        session_name: Human-readable session name
        session_description: Optional session description
        created_at: Session creation timestamp
        user_id: Owning user identifier
    """
    session_id: str
    session_name: str
    session_description: Optional[str] = None
    created_at: datetime
    user_id: str

    class Config:
        from_attributes = True


class SessionListResponse(BaseModel):
    """Paginated session list response schema.

    Attributes:
        total: Total number of sessions matching the query
        sessions: List of session response objects
    """
    total: int
    sessions: list[SessionResponse]

    class Config:
        from_attributes = True
