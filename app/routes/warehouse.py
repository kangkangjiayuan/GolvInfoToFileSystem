from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app.models.data import SearchResult, Report
from app import db
from app.utils.pdf_generator import PDFGenerator
import os

warehouse_bp = Blueprint('warehouse', __name__)

@warehouse_bp.route('/warehouse')
@login_required
def warehouse_index():
    # 获取筛选参数
    keyword = request.args.get('keyword', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    page = request.args.get('page', 1, type=int)
    
    # 构建查询
    query = SearchResult.query.filter_by(user_id=current_user.id, is_processed=True)
    
    if keyword:
        query = query.filter(SearchResult.keyword.contains(keyword))
    
    if date_from:
        query = query.filter(SearchResult.created_at >= datetime.strptime(date_from, '%Y-%m-%d'))
    
    if date_to:
        query = query.filter(SearchResult.created_at < datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1))
    
    # 分页
    per_page = 20
    results = query.order_by(SearchResult.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('warehouse/index.html', 
                         results=results,
                         keyword=keyword,
                         date_from=date_from,
                         date_to=date_to)

@warehouse_bp.route('/warehouse/data/<int:result_id>')
@login_required
def view_data(result_id):
    result = SearchResult.query.get_or_404(result_id)
    
    if result.user_id != current_user.id:
        flash('无权访问此数据', 'error')
        return redirect(url_for('warehouse.warehouse_index'))
    
    return render_template('warehouse/view_data.html', result=result)

@warehouse_bp.route('/warehouse/generate-report', methods=['POST'])
@login_required
def generate_report():
    selected_ids = request.json.get('selected_ids', [])
    
    if not selected_ids:
        return jsonify({'success': False, 'message': '请选择要生成报告的数据'})
    
    try:
        # 获取选中的数据
        results = SearchResult.query.filter(
            SearchResult.id.in_(selected_ids),
            SearchResult.user_id == current_user.id
        ).all()
        
        if not results:
            return jsonify({'success': False, 'message': '未找到选中的数据'})
        
        # 生成报告
        generator = PDFGenerator()
        report_path = generator.generate_report(results, current_user.username)
        
        # 获取文件大小
        import os
        file_size = os.path.getsize(report_path) if os.path.exists(report_path) else 0
        
        # 保存报告记录
        report = Report(
            title=f"数据分析报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            file_path=report_path,
            file_size=file_size,
            data_count=len(results),
            status='completed',
            user_id=current_user.id
        )
        db.session.add(report)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '报告生成成功',
            'report_id': report.id
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'报告生成失败: {str(e)}'})

@warehouse_bp.route('/warehouse/reports')
@login_required
def reports_list():
    page = request.args.get('page', 1, type=int)
    
    reports = Report.query.filter_by(user_id=current_user.id).order_by(
        Report.created_at.desc()
    ).paginate(page=page, per_page=10, error_out=False)
    
    return render_template('warehouse/reports.html', reports=reports)

@warehouse_bp.route('/warehouse/reports/<int:report_id>')
@login_required
def view_report(report_id):
    report = Report.query.get_or_404(report_id)
    
    if report.user_id != current_user.id:
        flash('无权访问此报告', 'error')
        return redirect(url_for('warehouse.reports_list'))
    
    return render_template('warehouse/report_detail.html', report=report)

@warehouse_bp.route('/warehouse/reports/download/<int:report_id>')
@login_required
def download_report(report_id):
    report = Report.query.get_or_404(report_id)
    
    if report.user_id != current_user.id:
        flash('无权访问此报告', 'error')
        return redirect(url_for('warehouse.reports_list'))
    
    if not os.path.exists(report.file_path):
        flash('报告文件不存在', 'error')
        return redirect(url_for('warehouse.reports_list'))
    
    return send_file(report.file_path, as_attachment=True, 
                    download_name=os.path.basename(report.file_path))

@warehouse_bp.route('/warehouse/data/delete/<int:result_id>', methods=['POST'])
@login_required
def delete_result(result_id):
    result = SearchResult.query.get_or_404(result_id)
    
    if result.user_id != current_user.id:
        return jsonify({'success': False, 'message': '无权删除此数据'})
    
    try:
        db.session.delete(result)
        db.session.commit()
        return jsonify({'success': True, 'message': '数据删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'删除失败: {str(e)}'})

@warehouse_bp.route('/warehouse/data/batch_delete', methods=['POST'])
@login_required
def batch_delete_results():
    data = request.get_json()
    result_ids = data.get('result_ids', [])
    
    if not result_ids:
        return jsonify({'success': False, 'message': '未选择要删除的数据'})
    
    try:
        deleted_count = 0
        for result_id in result_ids:
            result = SearchResult.query.get(result_id)
            if result and result.user_id == current_user.id:
                db.session.delete(result)
                deleted_count += 1
        
        db.session.commit()
        return jsonify({
            'success': True, 
            'message': f'成功删除 {deleted_count} 条数据',
            'deleted_count': deleted_count
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'批量删除失败: {str(e)}'})