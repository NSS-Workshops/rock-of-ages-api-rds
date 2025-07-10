#!/usr/bin/env python3
"""
Test script to verify RDS PostgreSQL connection
"""
import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rockproject.settings')
django.setup()

from django.db import connection
from django.core.management.color import make_style

style = make_style()

def test_database_connection():
    """Test the database connection and display info"""
    try:
        with connection.cursor() as cursor:
            # Test basic connection
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            
            print(style.SUCCESS("✅ Database connection successful!"))
            print(f"📊 PostgreSQL Version: {version}")
            
            # Get database info
            cursor.execute("SELECT current_database();")
            db_name = cursor.fetchone()[0]
            print(f"🗄️  Connected to database: {db_name}")
            
            # Check if tables exist
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name LIKE 'rockapi_%';
            """)
            tables = cursor.fetchall()
            
            if tables:
                print(f"📋 Found {len(tables)} app tables:")
                for table in tables:
                    print(f"   - {table[0]}")
            else:
                print(style.WARNING("⚠️  No app tables found. Run migrations first."))
                
    except Exception as e:
        print(style.ERROR(f"❌ Database connection failed: {e}"))
        sys.exit(1)

if __name__ == "__main__":
    test_database_connection()