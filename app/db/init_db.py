#!/usr/bin/env python3
"""
Database initialization script for SQLite setup.
Run this script to create the database file and tables.
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

from app.db.models import Base, User
from app.db.session import engine, SessionLocal

def create_database_and_tables():
    """Create the SQLite database file and all tables."""
    try:
        # Ensure data directory exists
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print(f"SQLite database created successfully at: {engine.url}")
        print("All tables created successfully.")
        return True
    except Exception as e:
        print(f"Error creating database and tables: {e}")
        return False

def create_sample_users():
    """Create sample users for testing."""
    db = SessionLocal()
    try:
        # Check if users already exist
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"Database already has {existing_users} users.")
            return True
        
        # Create sample users
        sample_users = [
            User(username="admin", password="admin123", role="admin"),
            User(username="tony", password="password123", role="engineering"),
            User(username="bruce", password="securepass", role="marketing"),
            User(username="sam", password="financepass", role="finance"),
            User(username="peter", password="pete123", role="engineering"),
            User(username="sid", password="sidpass123", role="marketing"),
            User(username="natasha", password="hrpass123", role="hr"),
            User(username="elena", password="execpass", role="c-level"),
        ]
        
        for user in sample_users:
            db.add(user)
        
        db.commit()
        print(f"Created {len(sample_users)} sample users successfully.")
        print("\nSample Users:")
        print("Username: admin, Password: admin123 (Role: admin)")
        print("Username: tony, Password: password123 (Role: engineering)")
        print("Username: bruce, Password: securepass (Role: marketing)")
        print("Username: sam, Password: financepass (Role: finance)")
        print("Username: peter, Password: pete123 (Role: engineering)")
        print("Username: sid, Password: sidpass123 (Role: marketing)")
        print("Username: natasha, Password: hrpass123 (Role: hr)")
        print("Username: elena, Password: execpass (Role: c-level)")
        return True
    except Exception as e:
        print(f"Error creating sample users: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def check_database_status():
    """Check and display database status."""
    db = SessionLocal()
    try:
        user_count = db.query(User).count()
        print(f"\nDatabase Status:")
        print(f"- Location: {engine.url}")
        print(f"- Total users: {user_count}")
        
        if user_count > 0:
            print("\nExisting users:")
            users = db.query(User).all()
            for user in users:
                print(f"  - {user.username} ({user.role})")
        
        return True
    except Exception as e:
        print(f"Error checking database status: {e}")
        return False
    finally:
        db.close()

def main():
    """Initialize the SQLite database setup."""
    print("Starting SQLite database initialization...")
    
    # Step 1: Create database and tables
    if not create_database_and_tables():
        print("Failed to create database and tables. Exiting.")
        return False
    
    # Step 2: Create sample users
    if not create_sample_users():
        print("Failed to create sample users. Exiting.")
        return False
    
    # Step 3: Check database status
    if not check_database_status():
        print("Failed to check database status.")
        return False
    
    print("\n" + "="*50)
    print("SQLite database initialization completed successfully!")
    print("You can now start the FastAPI application.")
    print("The database file is located at: ./data/app.db")
    print("="*50)
    return True

if __name__ == "__main__":
    main()