"""报告生成器测试 - Report Generator Tests"""

import os
import shutil
import tempfile
import unittest

from src.data_retrieval import DataRecord, SearchResult
from src.report import ReportGenerator


class TestReportGenerator(unittest.TestCase):
    """ReportGenerator测试类"""
    
    def setUp(self):
        """测试前置设置"""
        self.test_dir = tempfile.mkdtemp()
        self.generator = ReportGenerator(self.test_dir)
        self.sample_records = [
            DataRecord(
                title="测试记录1",
                content="这是测试内容1",
                category="分类A",
                tags=["标签1", "标签2"],
                source="来源1"
            ),
            DataRecord(
                title="测试记录2",
                content="这是测试内容2",
                category="分类B",
                tags=["标签2", "标签3"],
                source="来源2"
            ),
        ]
    
    def tearDown(self):
        """测试后置清理"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_generate_summary_report(self):
        """测试生成摘要报告"""
        path = self.generator.generate_summary_report(
            self.sample_records,
            title="测试报告"
        )
        
        self.assertTrue(os.path.exists(path))
        
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        self.assertIn("测试报告", content)
        self.assertIn("总记录数", content)
    
    def test_generate_search_report(self):
        """测试生成搜索报告"""
        result = SearchResult(
            query="测试查询",
            records=self.sample_records,
            total_count=2,
            search_time_ms=5.0
        )
        
        path = self.generator.generate_search_report(result)
        
        self.assertTrue(os.path.exists(path))
        
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        self.assertIn("搜索结果报告", content)
        self.assertIn("测试查询", content)
    
    def test_generate_json_report(self):
        """测试生成JSON报告"""
        path = self.generator.generate_json_report(self.sample_records)
        
        self.assertTrue(os.path.exists(path))
        self.assertTrue(path.endswith(".json"))
    
    def test_generate_csv_report(self):
        """测试生成CSV报告"""
        path = self.generator.generate_csv_report(self.sample_records)
        
        self.assertTrue(os.path.exists(path))
        self.assertTrue(path.endswith(".csv"))
        
        with open(path, "r", encoding="utf-8-sig") as f:
            content = f.read()
        
        self.assertIn("ID", content)
        self.assertIn("标题", content)
    
    def test_generate_report_with_custom_filename(self):
        """测试使用自定义文件名生成报告"""
        path = self.generator.generate_summary_report(
            self.sample_records,
            filename="custom_report.md"
        )
        
        self.assertTrue(path.endswith("custom_report.md"))
    
    def test_generate_empty_report(self):
        """测试生成空报告"""
        path = self.generator.generate_summary_report([])
        
        self.assertTrue(os.path.exists(path))
    
    def test_csv_escape(self):
        """测试CSV字段转义"""
        record_with_special_chars = DataRecord(
            title='包含逗号,和"引号"的标题',
            content="多行\n内容"
        )
        
        path = self.generator.generate_csv_report([record_with_special_chars])
        
        self.assertTrue(os.path.exists(path))


if __name__ == "__main__":
    unittest.main()
