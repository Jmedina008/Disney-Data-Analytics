"""
Database initialization script.
Creates initial superuser and sets up database tables.
"""

import logging
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.core.security import get_password_hash
from app.db.session import SessionLocal, engine
from app.models.user import User
from app.models.api_key import Base as APIKeyBase
from app.models.user import Base as UserBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db() -> None:
    """Initialize database with required initial data."""
    try:
        db = SessionLocal()
        
        # Create tables
        APIKeyBase.metadata.create_all(bind=engine)
        UserBase.metadata.create_all(bind=engine)
        
        # Check if superuser exists
        superuser = db.query(User).filter(User.is_superuser == True).first()
        if not superuser:
            logger.info("Creating superuser account...")
            superuser = User(
                email="admin@disney-portfolio.com",
                hashed_password=get_password_hash("admin123"),  # Change this in production!
                full_name="System Administrator",
                is_active=True,
                is_superuser=True
            )
            db.add(superuser)
            db.commit()
            logger.info("Superuser created successfully")
        else:
            logger.info("Superuser already exists")
        
        db.close()
        logger.info("Database initialization completed")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

if __name__ == "__main__":
    logger.info("Creating initial data")
    init_db()
    logger.info("Initial data created") 