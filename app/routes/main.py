from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app.models.data import SearchResult, SearchJob
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # 获取统计数据
    total_results = SearchResult.query.filter_by(user_id=current_user.id).count()
    recent_jobs = SearchJob.query.filter_by(user_id=current_user.id).order_by(SearchJob.created_at.desc()).limit(5).all()
    current_time = datetime.now()
    
    return render_template('dashboard.html', 
                         total_results=total_results,
                         recent_jobs=recent_jobs,
                         current_time=current_time)

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)