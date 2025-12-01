import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 应用配置
    APP_NAME = '智能瞭望数据分析处理系统'
    RESULTS_PER_PAGE = 10
    
    # 爬虫配置
    CRAWLER_TIMEOUT = 30
    MAX_RESULTS = 20
    
    # 文件上传配置
    UPLOAD_FOLDER = 'app/static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # PDF生成配置
    PDF_TEMPLATE_DIR = 'app/templates/pdf'
    PDF_OUTPUT_DIR = 'app/static/reports'