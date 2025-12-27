import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    DEBUG = False
    TESTING = False
    
    # Database
    DATABASE_PATH = os.environ.get('DATABASE_PATH', 'finance.db')
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # Chatterbox
    CHATTERBOX_API_KEY = os.environ.get('CHATTERBOX_API_KEY')
    
    # Intelligence
    ANOMALY_CONTAMINATION = float(os.environ.get('ANOMALY_CONTAMINATION', '0.1'))
    FORECAST_DEFAULT_DAYS = int(os.environ.get('FORECAST_DEFAULT_DAYS', '30'))
    MIN_TRANSACTIONS_FOR_ANALYSIS = int(os.environ.get('MIN_TRANSACTIONS_FOR_ANALYSIS', '10'))

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
