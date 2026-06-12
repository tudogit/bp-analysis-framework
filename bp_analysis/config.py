"""Configuration Management"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Base Configuration"""
    
    # Database
    DATABASE_URL = os.getenv(
        'DATABASE_URL',
        'sqlite:///bp_analysis.db'
    )
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Performance
    MAX_EVENTS_PER_QUERY = int(os.getenv('MAX_EVENTS_PER_QUERY', 100000))
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 1000))
    
    # Analysis
    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'True').lower() == 'true'
    CACHE_TTL_SECONDS = int(os.getenv('CACHE_TTL_SECONDS', 3600))
    
    # Process Mining
    MIN_VARIANT_FREQUENCY = int(os.getenv('MIN_VARIANT_FREQUENCY', 2))
    BOTTLENECK_PERCENTILE = int(os.getenv('BOTTLENECK_PERCENTILE', 90))
    
    # API
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))
    API_DEBUG = os.getenv('API_DEBUG', 'False').lower() == 'true'
    
    # Directories
    DATA_DIR = os.getenv('DATA_DIR', './data')
    LOGS_DIR = os.getenv('LOGS_DIR', './logs')
    EXPORTS_DIR = os.getenv('EXPORTS_DIR', './exports')


class DevelopmentConfig(Config):
    """Development Configuration"""
    DEBUG = True
    TESTING = False
    DATABASE_URL = 'sqlite:///bp_analysis_dev.db'
    LOG_LEVEL = 'DEBUG'
    API_DEBUG = True


class TestingConfig(Config):
    """Testing Configuration"""
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
    LOG_LEVEL = 'WARNING'
    CACHE_ENABLED = False


class ProductionConfig(Config):
    """Production Configuration"""
    DEBUG = False
    TESTING = False
    LOG_LEVEL = 'INFO'
    CACHE_ENABLED = True


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('ENV', 'development')
    
    if env == 'production':
        return ProductionConfig()
    elif env == 'testing':
        return TestingConfig()
    else:
        return DevelopmentConfig()


# Export current config
config = get_config()
