# app/db/models/user.py

from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.db.session import Base

# What is Base?
# ─────────────
# Base is the parent class that tells SQLAlchemy 
# "this is a database table"

class User(Base):
    """
    User model - represents the 'users' table in PostgreSQL
    
    Each attribute becomes a column in the database:
    - user_id becomes a column named 'user_id'
    - email becomes a column named 'email'
    - etc.
    """
    
    # Table name in the database
    __tablename__ = "users"
    
    # Columns
    # ───────
    
    # Primary Key (unique identifier for each user)
    user_id = Column(
        UUID(as_uuid=True),           # PostgreSQL UUID type
        primary_key=True,              # This is the primary key
        default=uuid.uuid4,            # Auto-generate UUID
        nullable=False                 # Cannot be NULL
    )
    
    # Email (unique per user)
    email = Column(
        String(255),                   # VARCHAR(255)
        unique=True,                   # No duplicate emails
        nullable=False,                # Required field
        index=True                     # Create index for faster searches
    )
    
    # Password (hashed)
    password_hash = Column(
        String(255),
        nullable=False
    )
    
    # Email verification
    email_verified = Column(
        Boolean,
        default=False                  # Default value
    )
    
    email_verification_token = Column(
        String(255),
        nullable=True                  # Optional field
    )
    
    email_verified_at = Column(
        DateTime,
        nullable=True
    )
    
    # Profile information
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_locked = Column(Boolean, default=False)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    
    # Account type
    account_type = Column(
        String(50),
        nullable=False
    )  # 'individual', 'business', 'accountant'
    
    # Timestamps
    created_at = Column(
        DateTime,
        default=datetime.utcnow,       # Automatically set when created
        nullable=False
    )
    
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,      # Automatically update when changed
        nullable=False
    )
    
    last_login_at = Column(DateTime, nullable=True)
    
    # Soft delete
    deleted_at = Column(DateTime, nullable=True)
    
    # String representation (useful for debugging)
    def __repr__(self):
        """
        When you print(user), you'll see:
        <User(email='john@example.com')>
        """
        return f"<User(email='{self.email}')>"
    
    # Helper method to convert to dictionary
    def to_dict(self):
        """
        Convert model to dictionary (useful for JSON responses)
        
        Usage:
            user = db.query(User).first()
            user_dict = user.to_dict()
            # Returns: {'user_id': '...', 'email': '...', ...}
        """
        return {
            'user_id': str(self.user_id),
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'account_type': self.account_type,
            'is_active': self.is_active,
            'email_verified': self.email_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None
        }