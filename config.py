import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    DB_NAME = os.getenv('DB_NAME', 'dairy_shop')
    DB_PORT = os.getenv('DB_PORT', '3306')
    
    # SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = (
        f"mysql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}"
        f"/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Upload Configuration
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'bills')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # ML Model Configuration
    TFIDF_VECTORIZER_PATH = 'tfidf_vectorizer.pkl'
    COSINE_SIM_PATH = 'cosine_sim.pkl'
    ML_PRODUCTS_CSV = 'dairy_products_large.csv'
    
    # Admin Configuration
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'admin123'
    
    # Product Configuration
    DEFAULT_STOCK = 100
    LOW_STOCK_THRESHOLD = 5
    
    # Cart Configuration
    CART_SESSION_KEY = 'cart'
    
    # Session and Cookie Settings
    SESSION_TYPE = 'filesystem'
    
    # Uploads folder
    UPLOADS_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')
    
    @staticmethod
    def init_app(app):
        """Initialize app with configuration"""
        # Create upload directory if it doesn't exist
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER) 