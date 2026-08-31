import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "novamart-dev-key-98102-secure")
    SESSION_COOKIE_NAME = "novamart_session"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Phase 2 Database Placeholder (Not active in Phase 1)
    DATABASE_URL = os.environ.get("DATABASE_URL", None)
    
    # Marketplace Default Settings
    CURRENCY_SYMBOL = "₹"
    CURRENCY_CODE = "INR"
    PLATFORM_NAME = "NOVA MART"
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
