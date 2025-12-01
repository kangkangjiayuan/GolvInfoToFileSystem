"""文件存储测试 - File Storage Tests"""

import os
import shutil
import tempfile
import unittest

from src.data_retrieval import DataRecord, SearchResult
from src.storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """FileStorage测试类"""
    
    def setUp(self):
        """测试前置设置"""
        self.test_dir = tempfile.mkdtemp()
        self.storage = FileStorage(self.test_dir)
    
    def tearDown(self):
        """测试后置清理"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_save_record(self):
        """测试保存记录"""
        record = DataRecord(
            title="测试记录",
            content="测试内容"
        )
        
        path = self.storage.save_record(record)
        
        self.assertTrue(os.path.exists(path))
    
    def test_load_record(self):
        """测试加载记录"""
        record = DataRecord(
            title="测试记录",
            content="测试内容"
        )
        self.storage.save_record(record)
        
        loaded = self.storage.load_record(record.id)
        
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.title, "测试记录")
    
    def test_load_nonexistent_record(self):
        """测试加载不存在的记录"""
        loaded = self.storage.load_record("nonexistent-id")
        
        self.assertIsNone(loaded)
    
    def test_delete_record(self):
        """测试删除记录"""
        record = DataRecord(title="测试记录")
        self.storage.save_record(record)
        
        result = self.storage.delete_record(record.id)
        
        self.assertTrue(result)
        self.assertFalse(self.storage.record_exists(record.id))
    
    def test_delete_nonexistent_record(self):
        """测试删除不存在的记录"""
        result = self.storage.delete_record("nonexistent-id")
        
        self.assertFalse(result)
    
    def test_load_all_records(self):
        """测试加载所有记录"""
        records = [
            DataRecord(title="记录1"),
            DataRecord(title="记录2"),
            DataRecord(title="记录3")
        ]
        for record in records:
            self.storage.save_record(record)
        
        loaded = self.storage.load_all_records()
        
        self.assertEqual(len(loaded), 3)
    
    def test_save_all_records(self):
        """测试保存所有记录"""
        records = [
            DataRecord(title="记录1"),
            DataRecord(title="记录2")
        ]
        
        count = self.storage.save_all_records(records)
        
        self.assertEqual(count, 2)
        self.assertEqual(self.storage.get_record_count(), 2)
    
    def test_record_exists(self):
        """测试记录是否存在"""
        record = DataRecord(title="测试记录")
        
        self.assertFalse(self.storage.record_exists(record.id))
        
        self.storage.save_record(record)
        
        self.assertTrue(self.storage.record_exists(record.id))
    
    def test_get_record_count(self):
        """测试获取记录数量"""
        self.assertEqual(self.storage.get_record_count(), 0)
        
        records = [DataRecord(title=f"记录{i}") for i in range(5)]
        self.storage.save_all_records(records)
        
        self.assertEqual(self.storage.get_record_count(), 5)
    
    def test_save_search_result(self):
        """测试保存搜索结果"""
        result = SearchResult(
            query="测试",
            records=[DataRecord(title="测试记录")],
            total_count=1
        )
        
        path = self.storage.save_search_result(result, "test_result.json")
        
        self.assertTrue(os.path.exists(path))
    
    def test_clear_all(self):
        """测试清除所有记录"""
        records = [DataRecord(title=f"记录{i}") for i in range(3)]
        self.storage.save_all_records(records)
        
        deleted = self.storage.clear_all()
        
        self.assertEqual(deleted, 3)
        self.assertEqual(self.storage.get_record_count(), 0)


if __name__ == "__main__":
    unittest.main()
