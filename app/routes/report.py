from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app.models.data import Report
from app import db

report_bp = Blueprint('report', __name__)

@report_bp.route('/report')
@login_required
def report_index():
    return render_template('report/index.html')