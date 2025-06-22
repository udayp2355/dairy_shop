# KrishnaKath Dairy - MySQL Database Setup

This document provides step-by-step instructions to set up the KrishnaKath Dairy application with MySQL database.

## Prerequisites

1. **Python 3.8+** installed on your system
2. **MySQL Server** installed and running
3. **Git** (optional, for version control)

## Installation Steps

### 1. Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd dairyfinal

# Or simply download and extract the project files
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. MySQL Database Setup

#### Option A: Using the Database Setup Script (Recommended)

```bash
python database_setup.py
```

#### Option B: Manual Database Setup

1. Open MySQL command line or MySQL Workbench
2. Create the database:

```sql
CREATE DATABASE dairy_shop;
USE dairy_shop;
```

3. Create the users table:

```sql
CREATE TABLE user (
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
);
```

4. Create the product table:

```sql
CREATE TABLE product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price FLOAT NOT NULL,
    description TEXT NOT NULL,
    image VARCHAR(200) NOT NULL,
    stock INT DEFAULT 100,
    category VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

5. Create the product specification table:

```sql
CREATE TABLE product_specification (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    feature VARCHAR(100) NOT NULL,
    value VARCHAR(100) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE
);
```

6. Create the ML product table:

```sql
CREATE TABLE ml_product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    price FLOAT NOT NULL,
    combined_features TEXT NOT NULL
);
```

7. Create the feedback table:

```sql
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Environment Configuration

1. Copy the environment template:

```bash
cp env_example.txt .env
```

2. Edit the `.env` file with your MySQL credentials:

```env
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=dairy_shop
DB_PORT=3306

# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True
```

### 5. Product Data Migration

**Important**: After setting up the database, you need to migrate the product data from CSV files to MySQL:

```bash
python migrate_products_to_db.py
```

This script will:

- Migrate 12 main dairy products with specifications
- Migrate 5000+ ML products for recommendations
- Create all necessary database relationships

**Migration Options:**

```bash
# Full migration (default)
python migrate_products_to_db.py

# Specific commands
python migrate_products_to_db.py migrate    # Run full migration
python migrate_products_to_db.py verify     # Verify migration
python migrate_products_to_db.py reset      # Reset product data
python migrate_products_to_db.py create-tables  # Create tables only
```

### 6. Test Database Connection

Before running the application, test the database connection:

```bash
python test_db_connection.py
```

### 7. Database Migration (Optional)

If you want to use Flask-Migrate for database versioning:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 8. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Default Credentials

### Admin User

- **Username:** admin
- **Password:** admin123

### Regular User

- Create a new account through the signup page

## Features Implemented

### User Authentication

- ✅ User registration with extended profile information
- ✅ User login/logout functionality
- ✅ Password hashing and security
- ✅ Email validation
- ✅ Admin user management

### Product Management

- ✅ Complete product database with specifications
- ✅ Product catalog with images and descriptions
- ✅ Stock management system
- ✅ Product recommendations using ML
- ✅ Admin panel for stock updates

### Database Features

- ✅ MySQL database integration
- ✅ User table with comprehensive user information
- ✅ Product table with specifications
- ✅ ML Product table for recommendations
- ✅ Feedback table for customer feedback
- ✅ Environment variable configuration
- ✅ Database migration support

### Security Features

- ✅ Password hashing using Werkzeug
- ✅ Session management
- ✅ Input validation
- ✅ SQL injection protection (via SQLAlchemy ORM)

## Database Schema

### User Table

- `id`: Primary key (auto-increment)
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Hashed password
- `first_name`: User's first name
- `last_name`: User's last name
- `phone`: Phone number
- `address`: User's address
- `created_at`: Account creation timestamp
- `is_active`: Account status

### Product Table

- `id`: Primary key (auto-increment)
- `name`: Product name
- `price`: Product price
- `description`: Product description
- `image`: Product image filename
- `stock`: Current stock quantity
- `category`: Product category
- `created_at`: Product creation timestamp
- `updated_at`: Last update timestamp

### Product Specification Table

- `id`: Primary key (auto-increment)
- `product_id`: Foreign key to product
- `feature`: Specification feature name
- `value`: Specification value

### ML Product Table

- `id`: Primary key (auto-increment)
- `product_id`: Product ID for ML
- `product_name`: Product name
- `category`: Product category
- `description`: Product description
- `ingredients`: Product ingredients
- `price`: Product price
- `combined_features`: Combined features for ML

### Feedback Table

- `id`: Primary key (auto-increment)
- `name`: Customer name
- `email`: Customer email
- `message`: Feedback message
- `created_at`: Feedback submission timestamp

## Troubleshooting

### Common Issues

1. **MySQL Connection Error**

   - Ensure MySQL server is running
   - Check database credentials in `.env` file
   - Verify database exists

2. **Import Error for mysql-connector-python**

   ```bash
   pip install mysql-connector-python
   ```

3. **PyMySQL Import Error**

   ```bash
   pip install PyMySQL
   ```

4. **Database Permission Error**

   - Ensure MySQL user has proper permissions
   - Grant privileges: `GRANT ALL PRIVILEGES ON dairy_shop.* TO 'username'@'localhost';`

5. **Port Already in Use**

   - Change the port in app.py or kill the existing process
   - Use: `lsof -ti:5000 | xargs kill -9`

6. **Environment Variables Not Loading**
   - Ensure `.env` file exists in the project root
   - Check that `python-dotenv` is installed
   - Verify `.env` file format is correct

### Testing Database Connection

Run the test script to diagnose connection issues:

```bash
python test_db_connection.py
```

This script will:

- Test direct MySQL connection
- Test Flask-SQLAlchemy connection
- Show database version and tables
- Provide troubleshooting tips

### Database Reset

To reset the database:

```sql
DROP DATABASE dairy_shop;
CREATE DATABASE dairy_shop;
```

Then run `python database_setup.py` again.

### Common Error Messages and Solutions

1. **"Access denied for user"**

   - Check MySQL user credentials
   - Ensure user has proper permissions

2. **"Can't connect to MySQL server"**

   - Verify MySQL service is running
   - Check host and port configuration

3. **"Unknown database"**

   - Run `python database_setup.py` to create database
   - Or manually create the database

4. **"Table doesn't exist"**
   - Run `python database_setup.py` to create tables
   - Or manually create the required tables

## Next Steps

After successful setup, you can:

1. Create additional user accounts
2. Test the feedback system
3. Continue with other application features
4. Customize the UI and styling

## Support

For issues or questions:

1. Run `python test_db_connection.py` to diagnose issues
2. Check the troubleshooting section
3. Verify all prerequisites are met
4. Ensure MySQL server is running
5. Check application logs for error messages
