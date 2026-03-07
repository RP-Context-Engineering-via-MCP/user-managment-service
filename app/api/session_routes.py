"""Session API Routes Module.

Provides RESTful API endpoints for session management operations scoped
to a specific user:
- Create a session for a user
- Retrieve a single session
- List all sessions for a user
- Update a session
- Delete a session
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session as DBSession

from app.core.database import get_db
from app.services.session_service import SessionService
from app.schemas.session_dto import (
    SessionCreateRequest,
    SessionUpdateRequest,
    SessionResponse,
    SessionListResponse,
)

router = APIRouter(
    prefix="/api/users/{user_id}/sessions",
    tags=["sessions"],
)


def get_session_service(db: DBSession = Depends(get_db)) -> SessionService:
    return SessionService(db)


def to_session_response(session) -> dict:
    return {
        "session_id": session.session_id,
        "session_name": session.session_name,
        "session_description": session.session_description,
        "created_at": session.created_at,
        "user_id": session.user_id,
    }


@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(
    user_id: str,
    data: SessionCreateRequest,
    service: SessionService = Depends(get_session_service),
):
    """Create a new session for the given user.

    Args:
        user_id: Owning user UUID (path parameter).
        data: Session creation payload.
        service: Injected SessionService dependency.

    Returns:
        SessionResponse: Created session data.

    Raises:
        HTTPException 404: If the user does not exist.
        HTTPException 500: If session creation fails.
    """
    try:
        session = service.create_session(user_id=user_id, data=data)
        return to_session_response(session)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create session: {str(e)}",
        )


@router.get("/", response_model=SessionListResponse)
def list_sessions(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: SessionService = Depends(get_session_service),
):
    """List all sessions for the given user with pagination.

    Args:
        user_id: Owning user UUID (path parameter).
        skip: Pagination offset.
        limit: Maximum records to return.
        service: Injected SessionService dependency.

    Returns:
        SessionListResponse: Paginated list of sessions with total count.

    Raises:
        HTTPException 404: If the user does not exist.
        HTTPException 500: If the query fails.
    """
    try:
        sessions, total = service.list_sessions(user_id=user_id, skip=skip, limit=limit)
        return SessionListResponse(total=total, sessions=[to_session_response(s) for s in sessions])
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/{session_id}", response_model=SessionResponse)
def get_session(
    user_id: str,
    session_id: str,
    service: SessionService = Depends(get_session_service),
):
    """Retrieve a single session by ID for the given user.

    Args:
        user_id: Owning user UUID (path parameter).
        session_id: Session UUID (path parameter).
        service: Injected SessionService dependency.

    Returns:
        SessionResponse: Session data.

    Raises:
        HTTPException 404: If the session does not exist or does not belong to the user.
    """
    try:
        session = service.get_session(session_id=session_id, user_id=user_id)
        return to_session_response(session)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{session_id}", response_model=SessionResponse)
def update_session(
    user_id: str,
    session_id: str,
    data: SessionUpdateRequest,
    service: SessionService = Depends(get_session_service),
):
    """Update a session's name or description.

    Args:
        user_id: Owning user UUID (path parameter).
        session_id: Session UUID (path parameter).
        data: Updated fields.
        service: Injected SessionService dependency.

    Returns:
        SessionResponse: Updated session data.

    Raises:
        HTTPException 404: If the session does not exist or does not belong to the user.
        HTTPException 500: If the update fails.
    """
    try:
        session = service.update_session(session_id=session_id, user_id=user_id, data=data)
        return to_session_response(session)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update session: {str(e)}",
        )


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    user_id: str,
    session_id: str,
    service: SessionService = Depends(get_session_service),
):
    """Delete a session.

    Args:
        user_id: Owning user UUID (path parameter).
        session_id: Session UUID (path parameter).
        service: Injected SessionService dependency.

    Returns:
        None: No content on successful deletion (204 status).

    Raises:
        HTTPException 404: If the session does not exist or does not belong to the user.
        HTTPException 500: If the deletion fails.
    """
    try:
        service.delete_session(session_id=session_id, user_id=user_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete session: {str(e)}",
        )
