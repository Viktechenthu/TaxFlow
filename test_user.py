from app.db.session import get_db_session
from app.db.models.user import User

print("Connecting to database...")
db = get_db_session()

try:
    print("\nCreating user...")
    user = User(
        email="john@example.com",
        password_hash="temporary_hash",
        first_name="John",
        last_name="Doe",
        account_type="individual"
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    print(f"✓ User created successfully!")
    print(f"  User ID: {user.user_id}")
    print(f"  Email: {user.email}")
    print(f"  Name: {user.first_name} {user.last_name}")
    
    # Query it back
    print("\n✓ Querying user from database...")
    found = db.query(User).filter(User.email == "john@example.com").first()
    
    if found:
        print(f"  Found: {found.email}")
        print(f"  Created at: {found.created_at}")
    
    print("\n✓ Success! Everything is working!")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    db.rollback()
    
finally:
    db.close()