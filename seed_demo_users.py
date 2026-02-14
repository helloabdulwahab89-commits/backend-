"""
Script to create demo users for testing.
Creates 2 admins, 2 faculty, and 2 students with profiles.
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.models.faculty import Faculty
from app.models.student import Student
from app.auth import get_password_hash
from datetime import date

# Create tables
Base.metadata.create_all(bind=engine)

def create_demo_users():
    """Create demo users with profiles"""
    db = SessionLocal()
    
    try:
        # ===== ADMIN USERS =====
        admins = [
            {"email": "admin@school.com", "password": "admin123"},
            {"email": "principal@school.com", "password": "principal123"},
        ]
        
        for admin_data in admins:
            existing = db.query(User).filter(User.email == admin_data["email"]).first()
            if existing:
                existing.hashed_password = get_password_hash(admin_data["password"])
                print(f"Updated admin: {admin_data['email']}")
            else:
                admin = User(
                    email=admin_data["email"],
                    hashed_password=get_password_hash(admin_data["password"]),
                    role=UserRole.ADMIN,
                    is_active=True
                )
                db.add(admin)
                print(f"Created admin: {admin_data['email']}")
        
        db.commit()
        
        # ===== FACULTY USERS =====
        faculty_data = [
            {
                "email": "teacher1@school.com",
                "password": "teacher123",
                "faculty_id": "FAC001",
                "first_name": "Ahmed",
                "last_name": "Khan",
                "subject": "Mathematics",
                "department": "Science",
                "phone": "03001234567",
                "qualification": "M.Sc Mathematics"
            },
            {
                "email": "teacher2@school.com",
                "password": "teacher456",
                "faculty_id": "FAC002",
                "first_name": "Sara",
                "last_name": "Ali",
                "subject": "Physics",
                "department": "Science",
                "phone": "03009876543",
                "qualification": "M.Sc Physics"
            },
        ]
        
        for fac_data in faculty_data:
            existing_user = db.query(User).filter(User.email == fac_data["email"]).first()
            
            if existing_user:
                existing_user.hashed_password = get_password_hash(fac_data["password"])
                print(f"Updated faculty user: {fac_data['email']}")
            else:
                user = User(
                    email=fac_data["email"],
                    hashed_password=get_password_hash(fac_data["password"]),
                    role=UserRole.FACULTY,
                    is_active=True
                )
                db.add(user)
                db.flush()
                
                # Check if faculty profile exists
                existing_faculty = db.query(Faculty).filter(Faculty.faculty_id == fac_data["faculty_id"]).first()
                if not existing_faculty:
                    faculty = Faculty(
                        user_id=user.id,
                        faculty_id=fac_data["faculty_id"],
                        first_name=fac_data["first_name"],
                        last_name=fac_data["last_name"],
                        subject=fac_data["subject"],
                        department=fac_data["department"],
                        phone=fac_data["phone"],
                        qualification=fac_data["qualification"],
                        date_of_joining=date.today()
                    )
                    db.add(faculty)
                    print(f"Created faculty: {fac_data['first_name']} {fac_data['last_name']} ({fac_data['email']})")
        
        db.commit()
        
        # ===== STUDENT USERS =====
        student_data = [
            {
                "email": "student1@school.com",
                "password": "student123",
                "student_id": "STU001",
                "first_name": "Ali",
                "last_name": "Hassan",
                "grade": "10",
                "section": "A",
                "phone": "03111234567",
                "parent_name": "Hassan Ahmed",
                "parent_phone": "03211234567",
                "address": "House 123, Street 5, Islamabad"
            },
            {
                "email": "student2@school.com",
                "password": "student456",
                "student_id": "STU002",
                "first_name": "Fatima",
                "last_name": "Malik",
                "grade": "9",
                "section": "B",
                "phone": "03119876543",
                "parent_name": "Malik Riaz",
                "parent_phone": "03219876543",
                "address": "House 456, Street 10, Lahore"
            },
        ]
        
        for stu_data in student_data:
            existing_user = db.query(User).filter(User.email == stu_data["email"]).first()
            
            if existing_user:
                existing_user.hashed_password = get_password_hash(stu_data["password"])
                print(f"Updated student user: {stu_data['email']}")
            else:
                user = User(
                    email=stu_data["email"],
                    hashed_password=get_password_hash(stu_data["password"]),
                    role=UserRole.STUDENT,
                    is_active=True
                )
                db.add(user)
                db.flush()
                
                # Check if student profile exists
                existing_student = db.query(Student).filter(Student.student_id == stu_data["student_id"]).first()
                if not existing_student:
                    student = Student(
                        user_id=user.id,
                        student_id=stu_data["student_id"],
                        first_name=stu_data["first_name"],
                        last_name=stu_data["last_name"],
                        grade=stu_data["grade"],
                        section=stu_data["section"],
                        phone=stu_data["phone"],
                        parent_name=stu_data["parent_name"],
                        parent_phone=stu_data["parent_phone"],
                        address=stu_data["address"],
                        date_of_birth=date(2010, 1, 15),
                        enrollment_date=date.today()
                    )
                    db.add(student)
                    print(f"Created student: {stu_data['first_name']} {stu_data['last_name']} ({stu_data['email']})")
        
        db.commit()
        
        print("\n" + "="*50)
        print("DEMO USERS CREATED SUCCESSFULLY!")
        print("="*50)
        print("\n📌 ADMIN CREDENTIALS:")
        print("   1. admin@school.com / admin123")
        print("   2. principal@school.com / principal123")
        print("\n📌 FACULTY CREDENTIALS:")
        print("   1. teacher1@school.com / teacher123 (Ahmed Khan - Math)")
        print("   2. teacher2@school.com / teacher456 (Sara Ali - Physics)")
        print("\n📌 STUDENT CREDENTIALS:")
        print("   1. student1@school.com / student123 (Ali Hassan - Grade 10A)")
        print("   2. student2@school.com / student456 (Fatima Malik - Grade 9B)")
        print("="*50)
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_demo_users()
