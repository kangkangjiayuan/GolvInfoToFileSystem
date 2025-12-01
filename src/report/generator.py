"""报告生成器 - Report Generator

提供从数据记录生成报告的功能。
Provides functionality to generate reports from data records.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..data_retrieval.models import DataRecord, SearchResult


class ReportGenerator:
    """报告生成器 - Report Generator
    
    从数据记录生成各种格式的报告。
    Generates reports in various formats from data records.
    """
    
    def __init__(self, output_path: str = "reports"):
        """初始化报告生成器 - Initialize report generator.
        
        Args:
            output_path: 报告输出路径 - Path for report output.
        """
        self.output_path = Path(output_path)
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self) -> None:
        """确保输出目录存在 - Ensure output directory exists."""
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    def generate_summary_report(
        self,
        records: List[DataRecord],
        title: str = "数据检索报告",
        filename: Optional[str] = None
    ) -> str:
        """生成摘要报告 - Generate summary report.
        
        Args:
            records: 数据记录列表 - List of data records.
            title: 报告标题 - Report title.
            filename: 文件名（可选） - Filename (optional).
            
        Returns:
            报告文件路径 - Path to the report file.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"summary_report_{timestamp}.md"
        
        # 统计信息 - Statistics
        categories = {}
        tags = {}
        sources = {}
        
        for record in records:
            # 按分类统计 - Count by category
            if record.category:
                categories[record.category] = categories.get(record.category, 0) + 1
            
            # 按标签统计 - Count by tags
            for tag in record.tags:
                tags[tag] = tags.get(tag, 0) + 1
            
            # 按来源统计 - Count by source
            if record.source:
                sources[record.source] = sources.get(record.source, 0) + 1
        
        # 生成Markdown报告 - Generate Markdown report
        report_lines = [
            f"# {title}",
            "",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 概览",
            "",
            f"- **总记录数**: {len(records)}",
            f"- **分类数**: {len(categories)}",
            f"- **标签数**: {len(tags)}",
            f"- **来源数**: {len(sources)}",
            "",
        ]
        
        # 分类统计 - Category statistics
        if categories:
            report_lines.extend([
                "## 分类统计",
                "",
                "| 分类 | 记录数 |",
                "|------|--------|",
            ])
            for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
                report_lines.append(f"| {cat} | {count} |")
            report_lines.append("")
        
        # 标签统计 - Tag statistics
        if tags:
            report_lines.extend([
                "## 标签统计",
                "",
                "| 标签 | 出现次数 |",
                "|------|----------|",
            ])
            for tag, count in sorted(tags.items(), key=lambda x: -x[1])[:20]:
                report_lines.append(f"| {tag} | {count} |")
            report_lines.append("")
        
        # 来源统计 - Source statistics
        if sources:
            report_lines.extend([
                "## 来源统计",
                "",
                "| 来源 | 记录数 |",
                "|------|--------|",
            ])
            for source, count in sorted(sources.items(), key=lambda x: -x[1]):
                report_lines.append(f"| {source} | {count} |")
            report_lines.append("")
        
        # 记录列表 - Record list
        if records:
            report_lines.extend([
                "## 记录列表",
                "",
            ])
            for i, record in enumerate(records[:50], 1):  # 最多显示50条
                report_lines.append(f"### {i}. {record.title or '(无标题)'}")
                report_lines.append("")
                if record.content:
                    # 截取前200个字符 - Truncate to first 200 characters
                    content_preview = record.content[:200]
                    if len(record.content) > 200:
                        content_preview += "..."
                    report_lines.append(f"> {content_preview}")
                    report_lines.append("")
                if record.category:
                    report_lines.append(f"- **分类**: {record.category}")
                if record.tags:
                    report_lines.append(f"- **标签**: {', '.join(record.tags)}")
                if record.source:
                    report_lines.append(f"- **来源**: {record.source}")
                report_lines.append(f"- **创建时间**: {record.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                report_lines.append("")
        
        # 写入文件 - Write to file
        file_path = self.output_path / filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))
        
        return str(file_path)
    
    def generate_search_report(
        self,
        result: SearchResult,
        filename: Optional[str] = None
    ) -> str:
        """生成搜索结果报告 - Generate search result report.
        
        Args:
            result: 搜索结果 - Search result.
            filename: 文件名（可选） - Filename (optional).
            
        Returns:
            报告文件路径 - Path to the report file.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"search_report_{timestamp}.md"
        
        report_lines = [
            "# 搜索结果报告",
            "",
            f"**搜索关键词**: {result.query or '(全部)'}",
            f"**搜索时间**: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"**耗时**: {result.search_time_ms:.2f} ms",
            "",
            "## 结果统计",
            "",
            f"- **总匹配数**: {result.total_count}",
            f"- **当前页**: {result.page}",
            f"- **每页数量**: {result.page_size}",
            "",
        ]
        
        if result.records:
            report_lines.extend([
                "## 匹配记录",
                "",
            ])
            for i, record in enumerate(result.records, 1):
                report_lines.append(f"### {i}. {record.title or '(无标题)'}")
                report_lines.append("")
                if record.content:
                    content_preview = record.content[:300]
                    if len(record.content) > 300:
                        content_preview += "..."
                    report_lines.append(f"> {content_preview}")
                    report_lines.append("")
                if record.category:
                    report_lines.append(f"- **分类**: {record.category}")
                if record.tags:
                    report_lines.append(f"- **标签**: {', '.join(record.tags)}")
                if record.source:
                    report_lines.append(f"- **来源**: {record.source}")
                report_lines.append("")
        else:
            report_lines.extend([
                "## 匹配记录",
                "",
                "未找到匹配的记录。",
                "",
            ])
        
        file_path = self.output_path / filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))
        
        return str(file_path)
    
    def generate_json_report(
        self,
        records: List[DataRecord],
        filename: Optional[str] = None
    ) -> str:
        """生成JSON格式报告 - Generate JSON format report.
        
        Args:
            records: 数据记录列表 - List of data records.
            filename: 文件名（可选） - Filename (optional).
            
        Returns:
            报告文件路径 - Path to the report file.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data_report_{timestamp}.json"
        
        report_data = {
            "generated_at": datetime.now().isoformat(),
            "total_records": len(records),
            "records": [record.to_dict() for record in records]
        }
        
        file_path = self.output_path / filename
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        return str(file_path)
    
    def generate_csv_report(
        self,
        records: List[DataRecord],
        filename: Optional[str] = None
    ) -> str:
        """生成CSV格式报告 - Generate CSV format report.
        
        Args:
            records: 数据记录列表 - List of data records.
            filename: 文件名（可选） - Filename (optional).
            
        Returns:
            报告文件路径 - Path to the report file.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data_report_{timestamp}.csv"
        
        # CSV头部 - CSV header
        headers = ["ID", "标题", "内容", "分类", "标签", "来源", "创建时间", "更新时间"]
        
        lines = [",".join(headers)]
        for record in records:
            row = [
                self._escape_csv(record.id),
                self._escape_csv(record.title),
                self._escape_csv(record.content[:100] + "..." if len(record.content) > 100 else record.content),
                self._escape_csv(record.category),
                self._escape_csv(";".join(record.tags)),
                self._escape_csv(record.source),
                self._escape_csv(record.created_at.strftime('%Y-%m-%d %H:%M:%S')),
                self._escape_csv(record.updated_at.strftime('%Y-%m-%d %H:%M:%S'))
            ]
            lines.append(",".join(row))
        
        file_path = self.output_path / filename
        with open(file_path, "w", encoding="utf-8-sig") as f:  # utf-8-sig for Excel compatibility
            f.write("\n".join(lines))
        
        return str(file_path)
    
    def _escape_csv(self, value: str) -> str:
        """转义CSV字段值 - Escape CSV field value.
        
        Args:
            value: 原始值 - Original value.
            
        Returns:
            转义后的值 - Escaped value.
        """
        if not value:
            return ""
        # 如果包含逗号、引号或换行符，需要用引号包围并转义内部引号
        if "," in value or '"' in value or "\n" in value:
            value = value.replace('"', '""')
            return f'"{value}"'
        return value
