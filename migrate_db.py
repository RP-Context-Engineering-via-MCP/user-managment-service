"""Database migration script.

Applies schema changes to the existing database:
- Creates the `session` table (if it does not already exist)
- Adds the relationship between `user` and `session` (one-to-many)

Safe to run multiple times — all operations are idempotent.

Usage:
    python migrate_db.py
"""

import sys
from sqlalchemy import create_engine, inspect, text
from app.core.config import settings
from app.core.database import Base

# Import ALL models so SQLAlchemy registers them before we touch the DB
from app.models.user import User          # noqa: F401
from app.models.session import Session    # noqa: F401

# Build engine with SSL required (needed for Supabase / cloud PostgreSQL)
# and a 10-second connection timeout so failures are reported quickly.
_db_url = settings.DATABASE_URL
if "?" not in _db_url:
    _db_url += "?sslmode=require"
elif "sslmode" not in _db_url:
    _db_url += "&sslmode=require"

engine = create_engine(
    _db_url,
    connect_args={"connect_timeout": 10},
    echo=False,
)


def table_exists(inspector, table_name: str) -> bool:
    return table_name in inspector.get_table_names()


def column_exists(inspector, table_name: str, column_name: str) -> bool:
    if not table_exists(inspector, table_name):
        return False
    cols = [c["name"] for c in inspector.get_columns(table_name)]
    return column_name in cols


def run_migration():
    inspector = inspect(engine)

    print("=" * 60)
    print("  User Management Service — Database Migration")
    print("=" * 60)

    with engine.begin() as conn:

        # ------------------------------------------------------------------
        # 1. Create `session` table
        # ------------------------------------------------------------------
        if not table_exists(inspector, "session"):
            print("[+] Creating table: session ...")
            conn.execute(text("""
                CREATE TABLE session (
                    session_id          VARCHAR(36)     NOT NULL,
                    session_name        VARCHAR(255)    NOT NULL,
                    session_description VARCHAR(1000),
                    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                    user_id             VARCHAR(36)     NOT NULL,
                    PRIMARY KEY (session_id),
                    CONSTRAINT fk_session_user
                        FOREIGN KEY (user_id)
                        REFERENCES "user" (user_id)
                        ON DELETE CASCADE
                )
            """))
            conn.execute(text("CREATE INDEX ix_session_session_id ON session (session_id)"))
            conn.execute(text("CREATE INDEX ix_session_user_id    ON session (user_id)"))
            print("    Table `session` created successfully.")
        else:
            print("[=] Table `session` already exists — skipping creation.")

            # If table already exists, ensure all expected columns are present
            missing = []
            for col in ("session_name", "session_description", "created_at", "user_id"):
                if not column_exists(inspector, "session", col):
                    missing.append(col)

            if missing:
                print(f"[!] WARNING: Missing columns in `session`: {missing}")
                print("    Please inspect and fix manually.")
            else:
                print("[=] All expected columns are present in `session`.")

    print()
    print("[✓] Migration completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    try:
        run_migration()
    except Exception as exc:
        print(f"\n[✗] Migration FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
