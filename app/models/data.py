from datetime import datetime
from app import db

class SearchResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    url = db.Column(db.String(1000), nullable=False)
    abstract = db.Column(db.Text)
    cover_url = db.Column(db.String(1000))
    rank = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_processed = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'keyword': self.keyword,
            'title': self.title,
            'url': self.url,
            'abstract': self.abstract,
            'cover_url': self.cover_url,
            'rank': self.rank,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class SearchJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, searching, parsing, saving, completed, failed
    progress = db.Column(db.Integer, default=0)  # 进度百分比 0-100
    results_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'keyword': self.keyword,
            'status': self.status,
            'progress': self.progress,
            'results_count': self.results_count,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'completed_at': self.completed_at.strftime('%Y-%m-%d %H:%M:%S') if self.completed_at else None
        }

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text)
    file_path = db.Column(db.String(1000))
    file_size = db.Column(db.Integer, default=0)  # 文件大小（字节）
    data_count = db.Column(db.Integer, default=0)  # 数据数量
    status = db.Column(db.String(50), default='completed')  # 状态：completed, generating, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    search_job_id = db.Column(db.Integer, db.ForeignKey('search_job.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'data_count': self.data_count,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }