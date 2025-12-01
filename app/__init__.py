from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # 配置
    app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录系统'
    
    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.crawler import crawler_bp
    from app.routes.warehouse import warehouse_bp
    from app.routes.report import report_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(crawler_bp)
    app.register_blueprint(warehouse_bp)
    app.register_blueprint(report_bp)
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
        # 创建默认管理员用户
        from app.models.user import User
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', password='admin123')
            db.session.add(admin)
            db.session.commit()
    
    # 配置用户加载回调
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app