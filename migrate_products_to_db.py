#!/usr/bin/env python3
"""
Product Migration Script for KrishnaKath Dairy
This script migrates all product data from CSV files and hardcoded lists to MySQL database.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the app using the create_app function
from app import create_app, db
from services.product_service import ProductService

# Create the app
app = create_app()

# Import migration functions
def migrate_products_to_db():
    """Migrate main products to database"""
    # Implement using ProductService
    csv_file = 'data/products.csv'
    success, message = ProductService.migrate_products_from_csv(csv_file)
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")

def migrate_ml_products_to_db():
    """Migrate ML products to database"""
    # Implement using ProductService
    csv_file = 'data/ml_products.csv'
    success, message = ProductService.migrate_ml_products_from_csv(csv_file)
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")

def create_product_tables():
    """Create product-related tables in the database"""
    try:
        with app.app_context():
            print("Creating product tables...")
            
            # Create all tables
            db.create_all()
            
            print("✅ Product tables created successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Error creating product tables: {e}")
        return False

def migrate_all_data():
    """Migrate all product data to database"""
    try:
        with app.app_context():
            print("Starting product data migration...")
            print("=" * 60)
            
            # Step 1: Create tables
            if not create_product_tables():
                return False
            
            print("\n" + "=" * 60)
            
            # Step 2: Migrate main products
            print("Migrating main products...")
            migrate_products_to_db()
            
            print("\n" + "=" * 60)
            
            # Step 3: Migrate ML products
            print("Migrating ML products for recommendations...")
            migrate_ml_products_to_db()
            
            print("\n" + "=" * 60)
            print("🎉 All product data migrated successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        return False

def verify_migration():
    """Verify that the migration was successful"""
    try:
        with app.app_context():
            from app import Product, ProductSpecification, MLProduct
            
            print("\nVerifying migration...")
            print("=" * 60)
            
            # Check main products
            product_count = Product.query.count()
            print(f"✅ Main products: {product_count}")
            
            # Check product specifications
            spec_count = ProductSpecification.query.count()
            print(f"✅ Product specifications: {spec_count}")
            
            # Check ML products
            ml_product_count = MLProduct.query.count()
            print(f"✅ ML products: {ml_product_count}")
            
            # Show sample products
            print("\nSample products:")
            products = Product.query.limit(5).all()
            for product in products:
                print(f"  - {product.name}: ₹{product.price} (Stock: {product.stock})")
            
            print("\n" + "=" * 60)
            print("✅ Migration verification completed!")
            return True
            
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False

def reset_product_data():
    """Reset all product data (use with caution)"""
    try:
        with app.app_context():
            print("⚠️  WARNING: This will delete all product data!")
            confirm = input("Are you sure you want to continue? (yes/no): ")
            
            if confirm.lower() != 'yes':
                print("Migration cancelled.")
                return False
            
            print("Deleting existing product data...")
            
            # Delete all product-related data
            from app import Product, ProductSpecification, MLProduct
            
            ProductSpecification.query.delete()
            MLProduct.query.delete()
            Product.query.delete()
            
            db.session.commit()
            print("✅ Product data reset successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Error resetting product data: {e}")
        return False

if __name__ == "__main__":
    print("KrishnaKath Dairy - Product Migration Tool")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "migrate":
            success = migrate_all_data()
            if success:
                verify_migration()
        
        elif command == "verify":
            verify_migration()
        
        elif command == "reset":
            reset_product_data()
        
        elif command == "create-tables":
            create_product_tables()
        
        else:
            print(f"Unknown command: {command}")
            print("Available commands: migrate, verify, reset, create-tables")
    
    else:
        # Default: run full migration
        print("Running full product migration...")
        success = migrate_all_data()
        if success:
            verify_migration()
        
        print("\nUsage:")
        print("  python migrate_products_to_db.py migrate    # Run full migration")
        print("  python migrate_products_to_db.py verify     # Verify migration")
        print("  python migrate_products_to_db.py reset      # Reset product data")
        print("  python migrate_products_to_db.py create-tables  # Create tables only") 
