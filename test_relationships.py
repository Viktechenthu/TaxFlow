from app.db.session import get_db_session
from app.db.models import User, UserProfile, UserRole

db = get_db_session()

try:
    print("Creating user with profile and role...")
    
    # Create user
    user = User(
        email="alice@example.com",
        password_hash="temp_hash",
        first_name="Alice",
        last_name="Smith",
        account_type="business"
    )
    db.add(user)
    db.flush()  # Get user_id without committing
    
    # Create profile for user
    profile = UserProfile(
        user_id=user.user_id,
        business_name="Alice's Consulting",
        business_number="123456789",
        city="Toronto",
        province="Ontario"
    )
    db.add(profile)
    
    # Assign role to user
    role = UserRole(
        user_id=user.user_id,
        role_name="client"
    )
    db.add(role)
    
    # Commit all together
    db.commit()
    db.refresh(user)
    
    print(f"✓ User created: {user.email}")
    print(f"✓ Profile created: {user.profile.business_name}")
    print(f"✓ Role assigned: {user.roles[0].role_name}")
    
    # Query back with relationships
    print("\n✓ Querying user with relationships...")
    found = db.query(User).filter(User.email == "alice@example.com").first()
    
    print(f"  User: {found.email}")
    print(f"  Business: {found.profile.business_name}")
    print(f"  City: {found.profile.city}")
    print(f"  Role: {found.roles[0].role_name}")
    
    print("\n✅ Relationships working correctly!")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    db.rollback()
    
finally:
    db.close()