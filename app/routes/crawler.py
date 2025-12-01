from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
import threading
import time
from datetime import datetime
from app.models.data import SearchResult, SearchJob
from app import db
from baidu_spider import BaiduSpider

crawler_bp = Blueprint('crawler', __name__)

@crawler_bp.route('/crawler')
@login_required
def crawler_page():
    return render_template('crawler/index.html')

@crawler_bp.route('/api/search', methods=['POST'])
@login_required
def start_search():
    keyword = request.json.get('keyword', '').strip()
    
    if not keyword:
        return jsonify({'success': False, 'message': '请输入搜索关键词'})
    
    try:
        # 创建搜索任务
        job = SearchJob(
            keyword=keyword,
            status='running',
            user_id=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        
        # 在后台线程中执行搜索
        thread = threading.Thread(target=perform_search, args=(job.id, keyword, current_user.id))
        thread.start()
        
        return jsonify({
            'success': True, 
            'message': '搜索任务已启动',
            'job_id': job.id
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'启动搜索失败: {str(e)}'})

def perform_search(job_id, keyword, user_id):
    """在后台执行搜索任务"""
    from app import create_app
    app = create_app()
    
    with app.app_context():
        job = SearchJob.query.get(job_id)
        spider = BaiduSpider()
        
        try:
            # 更新进度：开始搜索
            job.status = 'searching'
            job.progress = 10
            db.session.commit()
            
            # 执行搜索
            html_content = spider.search(keyword)
            
            if html_content:
                # 更新进度：开始解析
                job.status = 'parsing'
                job.progress = 30
                db.session.commit()
                
                # 解析结果
                results = spider.parse_results(html_content)
                
                # 更新进度：开始保存
                job.status = 'saving'
                job.progress = 60
                db.session.commit()
                
                # 保存结果到数据库
                total_results = len(results)
                for index, result in enumerate(results):
                    search_result = SearchResult(
                        keyword=keyword,
                        title=result['title'],
                        url=result['url'],
                        abstract=result['abstract'],
                        cover_url=result.get('cover_url', ''),
                        rank=result['rank'],
                        user_id=user_id
                    )
                    db.session.add(search_result)
                    
                    # 更新保存进度
                    if total_results > 0:
                        save_progress = 60 + (index + 1) * 30 / total_results
                        job.progress = int(save_progress)
                        db.session.commit()
                
                # 更新任务状态为完成
                job.status = 'completed'
                job.progress = 100
                job.results_count = len(results)
                job.completed_at = datetime.utcnow()
                db.session.commit()
                
            else:
                job.status = 'failed'
                job.progress = 0
                db.session.commit()
                
        except Exception as e:
            job.status = 'failed'
            job.progress = 0
            db.session.commit()
            app.logger.error(f"搜索任务失败: {str(e)}")

@crawler_bp.route('/api/search/status/<int:job_id>')
@login_required
def search_status(job_id):
    job = SearchJob.query.get_or_404(job_id)
    
    if job.user_id != current_user.id:
        return jsonify({'success': False, 'message': '无权访问此任务'})
    
    return jsonify({
        'success': True,
        'status': job.status,
        'progress': job.progress if hasattr(job, 'progress') else (100 if job.status == 'completed' else 0),
        'results_count': job.results_count,
        'created_at': job.created_at.strftime('%Y-%m-%d %H:%M:%S')
    })

@crawler_bp.route('/api/search/results/<int:job_id>')
@login_required
def get_search_results(job_id):
    job = SearchJob.query.get_or_404(job_id)
    
    if job.user_id != current_user.id:
        return jsonify({'success': False, 'message': '无权访问此任务'})
    
    results = SearchResult.query.filter_by(keyword=job.keyword, user_id=current_user.id).all()
    
    return jsonify({
        'success': True,
        'results': [result.to_dict() for result in results]
    })

@crawler_bp.route('/api/search/save', methods=['POST'])
@login_required
def save_results():
    result_ids = request.json.get('result_ids', [])
    
    if not result_ids:
        return jsonify({'success': False, 'message': '请选择要保存的结果'})
    
    try:
        # 标记选中的结果为已处理
        SearchResult.query.filter(
            SearchResult.id.in_(result_ids),
            SearchResult.user_id == current_user.id
        ).update({'is_processed': True}, synchronize_session=False)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'成功保存 {len(result_ids)} 条数据到数据库'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'保存失败: {str(e)}'})