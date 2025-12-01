"""数据模型测试 - Data Models Tests"""

import json
import unittest
from datetime import datetime

from src.data_retrieval.models import DataRecord, SearchResult


class TestDataRecord(unittest.TestCase):
    """DataRecord模型测试类"""
    
    def test_create_record(self):
        """测试创建数据记录"""
        record = DataRecord(
            title="测试标题",
            content="测试内容",
            source="测试来源",
            category="测试分类",
            tags=["标签1", "标签2"]
        )
        
        self.assertEqual(record.title, "测试标题")
        self.assertEqual(record.content, "测试内容")
        self.assertEqual(record.source, "测试来源")
        self.assertEqual(record.category, "测试分类")
        self.assertEqual(record.tags, ["标签1", "标签2"])
        self.assertIsNotNone(record.id)
        self.assertIsInstance(record.created_at, datetime)
    
    def test_record_to_dict(self):
        """测试记录转换为字典"""
        record = DataRecord(
            title="测试标题",
            content="测试内容"
        )
        
        data = record.to_dict()
        
        self.assertIn("id", data)
        self.assertEqual(data["title"], "测试标题")
        self.assertEqual(data["content"], "测试内容")
        self.assertIn("created_at", data)
    
    def test_record_from_dict(self):
        """测试从字典创建记录"""
        data = {
            "id": "test-id-123",
            "title": "测试标题",
            "content": "测试内容",
            "source": "测试来源",
            "category": "测试分类",
            "tags": ["标签1"],
            "metadata": {},
            "created_at": "2024-01-01T12:00:00",
            "updated_at": "2024-01-01T12:00:00"
        }
        
        record = DataRecord.from_dict(data)
        
        self.assertEqual(record.id, "test-id-123")
        self.assertEqual(record.title, "测试标题")
        self.assertIsInstance(record.created_at, datetime)
    
    def test_record_to_json(self):
        """测试记录转换为JSON"""
        record = DataRecord(
            title="测试标题",
            content="测试内容"
        )
        
        json_str = record.to_json()
        data = json.loads(json_str)
        
        self.assertEqual(data["title"], "测试标题")
    
    def test_record_from_json(self):
        """测试从JSON创建记录"""
        json_str = json.dumps({
            "id": "test-id-456",
            "title": "JSON测试",
            "content": "",
            "source": "",
            "category": "",
            "tags": [],
            "metadata": {},
            "created_at": "2024-01-01T12:00:00",
            "updated_at": "2024-01-01T12:00:00"
        })
        
        record = DataRecord.from_json(json_str)
        
        self.assertEqual(record.id, "test-id-456")
        self.assertEqual(record.title, "JSON测试")


class TestSearchResult(unittest.TestCase):
    """SearchResult模型测试类"""
    
    def test_create_search_result(self):
        """测试创建搜索结果"""
        record = DataRecord(title="测试记录")
        result = SearchResult(
            query="测试",
            records=[record],
            total_count=1
        )
        
        self.assertEqual(result.query, "测试")
        self.assertEqual(len(result.records), 1)
        self.assertEqual(result.total_count, 1)
    
    def test_search_result_to_dict(self):
        """测试搜索结果转换为字典"""
        result = SearchResult(
            query="测试查询",
            records=[],
            total_count=0
        )
        
        data = result.to_dict()
        
        self.assertEqual(data["query"], "测试查询")
        self.assertEqual(data["records"], [])
    
    def test_search_result_from_dict(self):
        """测试从字典创建搜索结果"""
        data = {
            "query": "测试",
            "records": [],
            "total_count": 0,
            "page": 1,
            "page_size": 10,
            "search_time_ms": 5.0,
            "timestamp": "2024-01-01T12:00:00"
        }
        
        result = SearchResult.from_dict(data)
        
        self.assertEqual(result.query, "测试")
        self.assertIsInstance(result.timestamp, datetime)


if __name__ == "__main__":
    unittest.main()
