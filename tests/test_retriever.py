"""数据检索器测试 - Data Retriever Tests"""

import unittest

from src.data_retrieval import DataRetriever, DataRecord


class TestDataRetriever(unittest.TestCase):
    """DataRetriever测试类"""
    
    def setUp(self):
        """测试前置设置"""
        self.records = [
            DataRecord(
                title="Python编程入门",
                content="Python是一种简单易学的编程语言",
                category="编程",
                tags=["Python", "编程"]
            ),
            DataRecord(
                title="机器学习基础",
                content="机器学习是人工智能的一个分支",
                category="人工智能",
                tags=["机器学习", "AI"]
            ),
            DataRecord(
                title="Web开发指南",
                content="Web开发包括前端和后端",
                category="编程",
                tags=["Web", "前端"]
            ),
        ]
        self.retriever = DataRetriever(self.records)
    
    def test_init_with_records(self):
        """测试使用记录初始化"""
        self.assertEqual(self.retriever.count(), 3)
    
    def test_add_record(self):
        """测试添加记录"""
        new_record = DataRecord(title="新记录")
        self.retriever.add_record(new_record)
        
        self.assertEqual(self.retriever.count(), 4)
    
    def test_remove_record(self):
        """测试删除记录"""
        record = self.records[0]
        result = self.retriever.remove_record(record.id)
        
        self.assertTrue(result)
        self.assertEqual(self.retriever.count(), 2)
    
    def test_remove_nonexistent_record(self):
        """测试删除不存在的记录"""
        result = self.retriever.remove_record("nonexistent-id")
        
        self.assertFalse(result)
    
    def test_get_record(self):
        """测试获取记录"""
        record = self.records[0]
        retrieved = self.retriever.get_record(record.id)
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.title, record.title)
    
    def test_get_nonexistent_record(self):
        """测试获取不存在的记录"""
        retrieved = self.retriever.get_record("nonexistent-id")
        
        self.assertIsNone(retrieved)
    
    def test_get_all_records(self):
        """测试获取所有记录"""
        all_records = self.retriever.get_all_records()
        
        self.assertEqual(len(all_records), 3)
    
    def test_search_by_keyword(self):
        """测试关键词搜索"""
        result = self.retriever.search("Python")
        
        self.assertEqual(result.total_count, 1)
        self.assertEqual(result.records[0].title, "Python编程入门")
    
    def test_search_case_insensitive(self):
        """测试不区分大小写搜索"""
        result = self.retriever.search("python")
        
        self.assertEqual(result.total_count, 1)
    
    def test_search_by_category(self):
        """测试按分类搜索"""
        result = self.retriever.search("", category="编程")
        
        self.assertEqual(result.total_count, 2)
    
    def test_search_by_tags(self):
        """测试按标签搜索"""
        result = self.retriever.search("", tags=["AI"])
        
        self.assertEqual(result.total_count, 1)
        self.assertEqual(result.records[0].title, "机器学习基础")
    
    def test_search_pagination(self):
        """测试搜索分页"""
        result = self.retriever.search("", page=1, page_size=2)
        
        self.assertEqual(len(result.records), 2)
        self.assertEqual(result.total_count, 3)
        self.assertEqual(result.page, 1)
        self.assertEqual(result.page_size, 2)
    
    def test_search_by_category_method(self):
        """测试search_by_category方法"""
        records = self.retriever.search_by_category("编程")
        
        self.assertEqual(len(records), 2)
    
    def test_search_by_tags_method(self):
        """测试search_by_tags方法"""
        records = self.retriever.search_by_tags(["Python"])
        
        self.assertEqual(len(records), 1)
    
    def test_search_by_tags_match_all(self):
        """测试search_by_tags匹配所有标签"""
        records = self.retriever.search_by_tags(["Python", "编程"], match_all=True)
        
        self.assertEqual(len(records), 1)
    
    def test_get_categories(self):
        """测试获取所有分类"""
        categories = self.retriever.get_categories()
        
        self.assertIn("编程", categories)
        self.assertIn("人工智能", categories)
    
    def test_get_tags(self):
        """测试获取所有标签"""
        tags = self.retriever.get_tags()
        
        self.assertIn("Python", tags)
        self.assertIn("AI", tags)


if __name__ == "__main__":
    unittest.main()
