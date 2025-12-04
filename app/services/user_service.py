"""User service - Business logic for user operations"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
from datetime import datetime

from app.db.models import User, UserProfile, UserRole
from app.utils.security import hash_password, verify_password
from app.schemas.user import UserRegisterRequest, UserUpdateRequest

class UserService:
    """Service for user-related operations"""
    
    @staticmethod
    def create_user(db: Session, user_data: UserRegisterRequest) -> User:
        """
        Create a new user with profile and role
        
        Args:
            db: Database session
            user_data: User registration data
            
        Returns:
            Created user object
            
        Raises:
            ValueError: If email already exists
        """
        # Check if email exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise ValueError("Email already registered")
        
        # Create user
        user = User(
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone=user_data.phone,
            account_type=user_data.account_type,
            is_active=True,
            email_verified=False
        )
        
        try:
            db.add(user)
            db.flush()  # Get user_id without committing
            
            # Create profile
            profile = UserProfile(
                user_id=user.user_id,
                profile_completed=False,
                profile_completion_percentage=25  # Has basic info
            )
            db.add(profile)
            
            # Assign default role based on account type
            role_name = "accountant" if user_data.account_type == "accountant" else "client"
            role = UserRole(
                user_id=user.user_id,
                role_name=role_name,
                is_active=True
            )
            db.add(role)
            
            db.commit()
            db.refresh(user)
            
            return user
            
        except IntegrityError as e:
            db.rollback()
            raise ValueError("Failed to create user") from e
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password
        
        Args:
            db: Database session
            email: User email
            password: Plain text password
            
        Returns:
            User object if authenticated, None otherwise
        """
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            return None
        
        # Check if account is locked
        if user.is_locked:
            if user.locked_until and user.locked_until > datetime.utcnow():
                return None  # Still locked
            else:
                # Unlock account
                user.is_locked = False
                user.locked_until = None
                user.failed_login_attempts = 0
                db.commit()
        
        # Verify password
        if not verify_password(password, user.password_hash):
            # Increment failed attempts
            user.failed_login_attempts += 1
            
            # Lock account after 5 failed attempts
            if user.failed_login_attempts >= 5:
                user.is_locked = True
                from datetime import timedelta
                user.locked_until = datetime.utcnow() + timedelta(minutes=30)
            
            db.commit()
            return None
        
        # Success - reset failed attempts and update last login
        user.failed_login_attempts = 0
        user.last_login_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.user_id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def update_user(db: Session, user_id: str, user_data: UserUpdateRequest) -> Optional[User]:
        """Update user information"""
        user = db.query(User).filter(User.user_id == user_id).first()
        
        if not user:
            return None
        
        # Update fields if provided
        if user_data.first_name is not None:
            user.first_name = user_data.first_name
        if user_data.last_name is not None:
            user.last_name = user_data.last_name
        if user_data.phone is not None:
            user.phone = user_data.phone
        
        user.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(user)
        
        return user
