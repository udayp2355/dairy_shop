#!/usr/bin/env python3
"""
Database Setup Script for KrishnaKath Dairy
This script initializes the MySQL database and creates all necessary tables.
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'password'),
            port=os.getenv('DB_PORT', 3306)
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            database_name = os.getenv('DB_NAME', 'dairy_shop')
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            print(f"Database '{database_name}' created successfully or already exists.")
            
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"Error creating database: {e}")

def create_tables():
    """Create all necessary tables"""
    try:
        # Connect to the specific database
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'password'),
            database=os.getenv('DB_NAME', 'dairy_shop'),
            port=os.getenv('DB_PORT', 3306)
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create users table
            create_users_table = """
            CREATE TABLE IF NOT EXISTS user (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                phone VARCHAR(15),
                address TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
            """
            
            # Create product table
            create_product_table = """
            CREATE TABLE IF NOT EXISTS product (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price FLOAT NOT NULL,
                description TEXT NOT NULL,
                image VARCHAR(200) NOT NULL,
                stock INT DEFAULT 100,
                category VARCHAR(50),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
            
            # Create product specification table
            create_product_specification_table = """
            CREATE TABLE IF NOT EXISTS product_specification (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_id INT NOT NULL,
                feature VARCHAR(100) NOT NULL,
                value VARCHAR(100) NOT NULL,
                FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE
            )
            """
            
            # Create ML product table
            create_ml_product_table = """
            CREATE TABLE IF NOT EXISTS ml_product (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_id INT NOT NULL,
                product_name VARCHAR(100) NOT NULL,
                category VARCHAR(100) NOT NULL,
                description TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                price FLOAT NOT NULL,
                combined_features TEXT NOT NULL
            )
            """
            
            # Create feedback table
            create_feedback_table = """
            CREATE TABLE IF NOT EXISTS feedback (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                message TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            # Execute table creation
            cursor.execute(create_users_table)
            print("Users table created successfully or already exists.")
            
            cursor.execute(create_product_table)
            print("Product table created successfully or already exists.")
            
            cursor.execute(create_product_specification_table)
            print("Product specification table created successfully or already exists.")
            
            cursor.execute(create_ml_product_table)
            print("ML Product table created successfully or already exists.")
            
            cursor.execute(create_feedback_table)
            print("Feedback table created successfully or already exists.")
            
            connection.commit()
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"Error creating tables: {e}")

def create_admin_user():
    """Create a default admin user"""
    try:
        from werkzeug.security import generate_password_hash
        import mysql.connector
        
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'password'),
            database=os.getenv('DB_NAME', 'dairy_shop'),
            port=os.getenv('DB_PORT', 3306)
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Check if admin user already exists
            cursor.execute("SELECT id FROM user WHERE username = 'admin'")
            admin_exists = cursor.fetchone()
            
            if not admin_exists:
                # Create admin user
                admin_password_hash = generate_password_hash('admin123', method='pbkdf2:sha256')
                insert_admin = """
                INSERT INTO user (username, email, password_hash, first_name, last_name, is_active)
                VALUES ('admin', 'admin@krishnakathdairy.com', %s, 'Admin', 'User', TRUE)
                """
                cursor.execute(insert_admin, (admin_password_hash,))
                connection.commit()
                print("Admin user created successfully.")
            else:
                print("Admin user already exists.")
            
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"Error creating admin user: {e}")

def run_product_migration():
    """Run the product migration script"""
    try:
        print("\n" + "=" * 60)
        print("Running product migration...")
        
        # Import and run the migration script
        import subprocess
        result = subprocess.run([sys.executable, 'migrate_products_to_db.py', 'migrate'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Product migration completed successfully!")
            print(result.stdout)
        else:
            print("❌ Product migration failed!")
            print(result.stderr)
            
    except Exception as e:
        print(f"Error running product migration: {e}")

if __name__ == "__main__":
    print("Setting up KrishnaKath Dairy Database...")
    print("=" * 50)
    
    create_database()
    create_tables()
    create_admin_user()
    
    # Ask user if they want to run product migration
    print("\n" + "=" * 50)
    print("Database setup completed successfully!")
    print("\nDefault admin credentials:")
    print("Username: admin")
    print("Password: admin123")
    
    print("\n" + "=" * 50)
    print("Next steps:")
    print("1. Run product migration: python migrate_products_to_db.py")
    print("2. Start the application: python app.py")
    print("\nYou can now run the Flask application.") 