from sqlalchemy import Column, String, Boolean, Date, ForeignKey, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.session import Base

class UserProfile(Base):
    """
    Extended user profile information
    Separate from User for cleaner organization
    """
    
    __tablename__ = "user_profiles"
    
    # Primary Key
    profile_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign Key to User (ONE-to-ONE relationship)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.user_id', ondelete='CASCADE'),
        unique=True,  # Ensures one profile per user
        nullable=False,
        index=True
    )
    
    # Business Information
    business_name = Column(String(255))
    business_number = Column(String(50))  # CRA Business Number
    hst_number = Column(String(50))
    industry = Column(String(100))
    fiscal_year_end = Column(Date)
    
    # Address
    address_line1 = Column(String(255))
    address_line2 = Column(String(255))
    city = Column(String(100))
    province = Column(String(50))
    postal_code = Column(String(10))
    country = Column(String(50), default='Canada')
    
    # Preferences
    language = Column(String(10), default='en')
    currency = Column(String(3), default='CAD')
    date_format = Column(String(20), default='DD/MM/YYYY')
    timezone = Column(String(50), default='America/Toronto')
    
    # Notification Settings
    email_notifications = Column(Boolean, default=True)
    processing_alerts = Column(Boolean, default=True)
    weekly_summary = Column(Boolean, default=False)
    marketing_emails = Column(Boolean, default=False)
    
    # Profile Completion
    profile_completed = Column(Boolean, default=False)
    profile_completion_percentage = Column(Integer, default=0)
    
    # Metadata (flexible JSON field for future additions)
    profile_metadata = Column(JSONB)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to User
    user = relationship("User", back_populates="profile")
    
    def __repr__(self):
        return f"<UserProfile(user_id='{self.user_id}', business_name='{self.business_name}')>"
    
    def to_dict(self):
        return {
            'profile_id': str(self.profile_id),
            'user_id': str(self.user_id),
            'business_name': self.business_name,
            'business_number': self.business_number,
            'address': {
                'line1': self.address_line1,
                'city': self.city,
                'province': self.province,
                'postal_code': self.postal_code
            },
            'preferences': {
                'language': self.language,
                'currency': self.currency,
                'timezone': self.timezone
            }
        }