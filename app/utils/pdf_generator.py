from flask import send_file
from datetime import datetime
from jinja2 import Template
import os
from app.config import Config

class PDFGenerator:
    def __init__(self):
        self.config = Config()
        self.ensure_directories()
    
    def ensure_directories(self):
        """确保必要的目录存在"""
        os.makedirs(self.config.PDF_OUTPUT_DIR, exist_ok=True)
        os.makedirs(self.config.PDF_TEMPLATE_DIR, exist_ok=True)
    
    def generate_report(self, results, username):
        """生成PDF报告"""
        try:
            # 生成HTML内容
            html_content = self.generate_html(results, username)
            
            # 生成文件名
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            filepath = os.path.join(self.config.PDF_OUTPUT_DIR, filename)
            
            # 保存HTML文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return filepath
            
        except Exception as e:
            raise Exception(f"生成报告失败: {str(e)}")
    
    def generate_html(self, results, username):
        """生成HTML报告内容"""
        template = Template("""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>数据分析报告</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }
                .container {
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                    padding: 40px;
                    margin: 20px 0;
                }
                .header {
                    text-align: center;
                    border-bottom: 3px solid #667eea;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }
                .header h1 {
                    color: #667eea;
                    font-size: 2.5em;
                    margin-bottom: 10px;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
                }
                .header .meta {
                    color: #666;
                    font-size: 1.1em;
                }
                .stats {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin: 30px 0;
                }
                .stat-card {
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    padding: 25px;
                    border-radius: 12px;
                    text-align: center;
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
                }
                .stat-card h3 {
                    margin: 0 0 10px 0;
                    font-size: 2.2em;
                    font-weight: bold;
                }
                .stat-card p {
                    margin: 0;
                    opacity: 0.9;
                    font-size: 1.1em;
                }
                .results {
                    margin-top: 40px;
                }
                .results h2 {
                    color: #667eea;
                    border-left: 4px solid #667eea;
                    padding-left: 15px;
                    margin-bottom: 25px;
                    font-size: 1.8em;
                }
                .result-item {
                    background: #f8f9ff;
                    border: 1px solid #e1e8ff;
                    border-radius: 10px;
                    padding: 25px;
                    margin-bottom: 20px;
                    transition: all 0.3s ease;
                    position: relative;
                }
                .result-item:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
                }
                .result-item .rank {
                    position: absolute;
                    top: 15px;
                    right: 20px;
                    background: #667eea;
                    color: white;
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    font-size: 0.9em;
                }
                .result-item .title {
                    font-size: 1.3em;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 10px;
                    line-height: 1.4;
                }
                .result-item .url {
                    color: #667eea;
                    text-decoration: none;
                    font-size: 0.95em;
                    margin-bottom: 12px;
                    display: block;
                    word-break: break-all;
                }
                .result-item .url:hover {
                    text-decoration: underline;
                }
                .result-item .abstract {
                    color: #555;
                    font-size: 1em;
                    line-height: 1.6;
                    margin-bottom: 10px;
                }
                .result-item .keyword {
                    display: inline-block;
                    background: #e1e8ff;
                    color: #667eea;
                    padding: 4px 12px;
                    border-radius: 15px;
                    font-size: 0.85em;
                    font-weight: 500;
                }
                .footer {
                    text-align: center;
                    margin-top: 50px;
                    padding-top: 30px;
                    border-top: 2px solid #e1e8ff;
                    color: #666;
                    font-size: 0.9em;
                }
                .footer .logo {
                    font-size: 1.2em;
                    font-weight: bold;
                    color: #667eea;
                    margin-bottom: 10px;
                }
                @media print {
                    body { background: none; }
                    .container { box-shadow: none; }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>智能瞭望数据分析报告</h1>
                    <div class="meta">
                        生成时间: {{ datetime.now().strftime('%Y年%m月%d日 %H:%M:%S') }} | 
                        分析师: {{ username }} | 
                        数据来源: 百度搜索
                    </div>
                </div>

                <div class="stats">
                    <div class="stat-card">
                        <h3>{{ results|length }}</h3>
                        <p>搜索结果总数</p>
                    </div>
                    <div class="stat-card">
                        <h3>{{ unique_keywords|length }}</h3>
                        <p>关键词数量</p>
                    </div>
                    <div class="stat-card">
                        <h3>{{ processed_date }}</h3>
                        <p>处理日期</p>
                    </div>
                </div>

                <div class="results">
                    <h2>详细搜索结果</h2>
                    {% for result in results %}
                    <div class="result-item">
                        <div class="rank">{{ result.rank }}</div>
                        <div class="title">{{ result.title }}</div>
                        <a href="{{ result.url }}" class="url">{{ result.url }}</a>
                        <div class="abstract">{{ result.abstract }}</div>
                        <span class="keyword">{{ result.keyword }}</span>
                    </div>
                    {% endfor %}
                </div>

                <div class="footer">
                    <div class="logo">智能瞭望数据分析处理系统</div>
                    <p>本报告由智能瞭望系统自动生成，基于百度搜索结果进行数据分析和整理</p>
                    <p>© 2024 智能瞭望系统 - 让数据分析更简单、更智能</p>
                </div>
            </div>
        </body>
        </html>
        """)
        
        # 准备数据
        unique_keywords = list(set(result.keyword for result in results))
        processed_date = datetime.now().strftime('%Y年%m月%d日')
        
        return template.render(
            results=results,
            username=username,
            datetime=datetime,
            unique_keywords=unique_keywords,
            processed_date=processed_date
        )