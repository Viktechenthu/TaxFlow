"""User API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import User  # Add this import
from app.services.user_service import UserService
from app.schemas.user import (
    UserRegisterRequest,
    UserRegisterResponse,
    UserLoginRequest,
    UserLoginResponse,
    UserUpdateRequest,
    UserResponse,
    MessageResponse
)

router = APIRouter()

@router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    try:
        user = UserService.create_user(db, user_data)
        
        return UserRegisterResponse(
            success=True,
            message="User registered successfully",
            user=UserResponse.model_validate(user)
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=UserLoginResponse)
def login_user(
    credentials: UserLoginRequest,
    db: Session = Depends(get_db)
):
    """Login with email and password"""
    user = UserService.authenticate_user(db, credentials.email, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Placeholder token (we'll add JWT next)
    access_token = f"mock_token_for_{user.user_id}"
    
    return UserLoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )

@router.get("/me", response_model=UserResponse)
def get_current_user(db: Session = Depends(get_db)):
    """Get current user profile (placeholder)"""
    user = db.query(User).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.model_validate(user)

@router.put("/me", response_model=UserResponse)
def update_current_user(
    user_data: UserUpdateRequest,
    db: Session = Depends(get_db)
):
    """Update current user profile (placeholder)"""
    user = db.query(User).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    updated_user = UserService.update_user(db, str(user.user_id), user_data)
    return UserResponse.model_validate(updated_user)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = UserService.get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.model_validate(user)
