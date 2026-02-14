"""
Script to create an initial admin user.
Run this after setting up the database.
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.auth import get_password_hash

# Create tables
Base.metadata.create_all(bind=engine)


def create_admin(email: str, password: str):
    """Create an admin user"""
    db = SessionLocal()
    try:
        # Check if admin already exists
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"User with email {email} already exists!")
            return
        
        admin = User(
            email=email,
            hashed_password=get_password_hash(password),
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin)
        db.commit()
        print(f"Admin user created successfully!")
        print(f"Email: {email}")
        print(f"Role: admin")
    except Exception as e:
        print(f"Error creating admin: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 3:
        email = sys.argv[1]
        password = sys.argv[2]
    else:
        email = input("Enter admin email: ")
        password = input("Enter admin password: ")
    
    create_admin(email, password)
