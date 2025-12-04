from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.session import Base

class UserRole(Base):
    """
    User roles for RBAC (Role-Based Access Control)
    Allows users to have multiple roles
    """
    
    __tablename__ = "user_roles"
    
    role_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign Key to User
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.user_id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    # Role name: 'client', 'accountant', 'admin'
    role_name = Column(String(50), nullable=False, index=True)
    
    # Who assigned this role
    assigned_by = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    assigned_at = Column(DateTime, default=datetime.utcnow)
    
    # Organization scoping (for future multi-tenant support)
    organization_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Role status
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=True)  # Optional: temporary roles
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="roles")
    
    def __repr__(self):
        return f"<UserRole(user_id='{self.user_id}', role='{self.role_name}')>"
    
    def to_dict(self):
        return {
            'role_id': str(self.role_id),
            'role_name': self.role_name,
            'is_active': self.is_active,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None
        }