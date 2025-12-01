#!/usr/bin/env python3
"""
智能瞭望数据分析处理系统
启动脚本
"""

from app import create_app
import os

def main():
    """主函数"""
    app = create_app()
    
    # 获取端口
    port = int(os.environ.get('PORT', 8080))
    
    # 启动应用
    print("=" * 50)
    print("智能瞭望数据分析处理系统")
    print("=" * 50)
    print(f"应用地址: http://localhost:{port}")
    print("默认管理员账号: admin")
    print("默认管理员密码: admin123")
    print("=" * 50)
    print("按 Ctrl+C 停止服务")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True,
        threaded=True
    )

if __name__ == '__main__':
    main()