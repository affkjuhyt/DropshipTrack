import logging
import traceback
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

logger = logging.getLogger(__name__)

# Database connection settings (should come from config)
DATABASE_URL = "postgresql://user:password@localhost/dropship"
REPLICA_URL = "postgresql://user:password@localhost/dropship_replica"

# Create engines
writer_engine = create_engine(DATABASE_URL)
replica_engine = create_engine(REPLICA_URL)

# Session factories
WriterSession = scoped_session(sessionmaker(bind=writer_engine))
ReplicaSession = scoped_session(sessionmaker(bind=replica_engine))

UNSAFE_WRITER_ACCESS_MSG = (
    "Unsafe access to the writer DB detected. Use `with allow_writer()` context "
    "or explicitly specify the replica connection."
)
TRACEBACK_LIMIT = 20

class UnsafeWriterAccessError(Exception):
    pass

@contextmanager
def allow_writer() -> Generator[None, None, None]:
    """Context manager that allows write access to the writer database."""
    try:
        WriterSession.execute_wrapper = safe_writer_check
        yield
    finally:
        WriterSession.execute_wrapper = None

@contextmanager
def get_db_session(writer_allowed: bool = False):
    """Get a database session with optional writer access."""
    session = WriterSession() if writer_allowed else ReplicaSession()
    try:
        yield session
    except Exception as e:
        session.rollback()
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        session.close()

def safe_writer_check(execute, *args, **kwargs):
    """Check if writer access is allowed before executing queries."""
    if not getattr(WriterSession, "_allow_writer", False):
        stack_trace = traceback.extract_stack(limit=TRACEBACK_LIMIT)
        error_msg = f"{UNSAFE_WRITER_ACCESS_MSG}\n" \
                   f"Traceback:\n{''.join(traceback.format_list(stack_trace))}"
        logger.warning(error_msg)
        raise UnsafeWriterAccessError(UNSAFE_WRITER_ACCESS_MSG)
    return execute(*args, **kwargs)