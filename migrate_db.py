#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库迁移脚本 - 添加progress字段到search_job表
"""

import sqlite3
import os

def migrate_database():
    """执行数据库迁移"""
    db_path = 'instance/data.db'
    
    if not os.path.exists(db_path):
        print(f"数据库文件不存在: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查search_job表的progress字段是否存在
        cursor.execute("PRAGMA table_info(search_job)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'progress' not in columns:
            print("正在添加progress字段到search_job表...")
            cursor.execute("ALTER TABLE search_job ADD COLUMN progress INTEGER DEFAULT 0")
            print("progress字段添加成功")
        else:
            print("progress字段已存在")
        
        # 更新现有数据的progress值
        print("更新现有数据的progress值...")
        cursor.execute("UPDATE search_job SET progress = 100 WHERE status = 'completed'")
        cursor.execute("UPDATE search_job SET progress = 0 WHERE status IN ('pending', 'failed')")
        
        # 检查report表的新字段是否存在
        cursor.execute("PRAGMA table_info(report)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'file_size' not in columns:
            print("正在添加file_size字段到report表...")
            cursor.execute("ALTER TABLE report ADD COLUMN file_size INTEGER DEFAULT 0")
            print("file_size字段添加成功")
        
        if 'data_count' not in columns:
            print("正在添加data_count字段到report表...")
            cursor.execute("ALTER TABLE report ADD COLUMN data_count INTEGER DEFAULT 0")
            print("data_count字段添加成功")
        
        if 'status' not in columns:
            print("正在添加status字段到report表...")
            cursor.execute("ALTER TABLE report ADD COLUMN status VARCHAR(50) DEFAULT 'completed'")
            print("status字段添加成功")
        
        conn.commit()
        print("数据库迁移完成")
        return True
        
    except Exception as e:
        print(f"数据库迁移失败: {e}")
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()