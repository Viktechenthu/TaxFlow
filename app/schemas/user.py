"""Pydantic schemas for User API requests/responses"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
import re

# Request Schemas (Input)
# ─────────────────────────

class UserRegisterRequest(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)  # ← Added max_length
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    account_type: str = Field(..., pattern="^(individual|business|accountant)$")
    phone: Optional[str] = None
    
    @field_validator('password')
    def validate_password(cls, v):
        """Ensure password has uppercase, lowercase, and number"""
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "john@example.com",
                "password": "SecurePass123",
                "first_name": "John",
                "last_name": "Doe",
                "account_type": "individual",
                "phone": "+1-555-0123"
            }
        }
    }

class UserLoginRequest(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "john@example.com",
                "password": "SecurePass123"
            }
        }
    }

class UserUpdateRequest(BaseModel):
    """Schema for updating user profile"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = None
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "John",
                "last_name": "Smith",
                "phone": "+1-555-9999"
            }
        }
    }

# Response Schemas (Output)
# ─────────────────────────

class UserResponse(BaseModel):
    """Schema for user data in responses"""
    user_id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    account_type: str
    is_active: bool
    email_verified: bool
    created_at: datetime
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "account_type": "individual",
                "is_active": True,
                "email_verified": False,
                "created_at": "2024-12-02T10:30:00Z"
            }
        }
    }

class UserRegisterResponse(BaseModel):
    """Schema for registration response"""
    success: bool
    message: str
    user: UserResponse
    
class UserLoginResponse(BaseModel):
    """Schema for login response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class MessageResponse(BaseModel):
    """Generic message response"""
    success: bool
    message: str
