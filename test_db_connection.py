#!/usr/bin/env python3
"""
Test Database Connection Script
This script tests the MySQL database connection and basic functionality.
"""

import os
from dotenv import load_dotenv
import pymysql
from pymysql import Error

# Load environment variables
load_dotenv()

def test_mysql_connection():
    """Test MySQL database connection"""
    try:
        # Configure PyMySQL
        pymysql.install_as_MySQLdb()
        
        # Get database configuration from environment
        host = os.getenv('DB_HOST', 'localhost')
        user = os.getenv('DB_USER', 'root')
        password = os.getenv('DB_PASSWORD', 'password')
        database = os.getenv('DB_NAME', 'dairy_shop')
        port = int(os.getenv('DB_PORT', '3306'))
        
        print(f"Testing connection to MySQL database...")
        print(f"Host: {host}")
        print(f"User: {user}")
        print(f"Database: {database}")
        print(f"Port: {port}")
        print("-" * 50)
        
        # Test connection
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        
        if connection.is_connected():
            print("✅ MySQL connection successful!")
            
            # Test basic query
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ MySQL Version: {version[0]}")
            
            # Test if tables exist
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"✅ Tables found: {len(tables)}")
            for table in tables:
                print(f"   - {table[0]}")
            
            cursor.close()
            connection.close()
            print("✅ Database connection test completed successfully!")
            return True
            
    except Error as e:
        print(f"❌ MySQL connection failed: {e}")
        return False

def test_flask_sqlalchemy():
    """Test Flask-SQLAlchemy connection"""
    try:
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        
        app = Flask(__name__)
        
        # Configure database URI
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f"mysql://{os.getenv('DB_USER', 'root')}:{os.getenv('DB_PASSWORD', 'password')}"
            f"@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}"
            f"/{os.getenv('DB_NAME', 'dairy_shop')}"
        )
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db = SQLAlchemy(app)
        
        with app.app_context():
            # Test database connection
            db.engine.execute('SELECT 1')
            print("✅ Flask-SQLAlchemy connection successful!")
            return True
            
    except Exception as e:
        print(f"❌ Flask-SQLAlchemy connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing KrishnaKath Dairy Database Connection")
    print("=" * 60)
    
    # Test 1: Direct MySQL connection
    mysql_success = test_mysql_connection()
    
    print("\n" + "=" * 60)
    
    # Test 2: Flask-SQLAlchemy connection
    flask_success = test_flask_sqlalchemy()
    
    print("\n" + "=" * 60)
    
    if mysql_success and flask_success:
        print("🎉 All database tests passed! The application should work correctly.")
    else:
        print("⚠️  Some tests failed. Please check your database configuration.")
        print("\nTroubleshooting tips:")
        print("1. Ensure MySQL server is running")
        print("2. Check your .env file configuration")
        print("3. Verify database and tables exist")
        print("4. Check MySQL user permissions") 