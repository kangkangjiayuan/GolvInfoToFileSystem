"""数据检索系统主程序 - Data Retrieval System Main Program

提供命令行接口来使用数据检索系统。
Provides a command-line interface for using the data retrieval system.
"""

import argparse
import json
import sys
from pathlib import Path

from src.data_retrieval import DataRetriever, DataRecord
from src.storage import FileStorage
from src.report import ReportGenerator


def create_sample_data() -> list:
    """创建示例数据 - Create sample data."""
    return [
        DataRecord(
            title="Python编程入门",
            content="Python是一种简单易学的编程语言，适合初学者入门。它有着清晰的语法和丰富的库支持。",
            source="技术文档",
            category="编程",
            tags=["Python", "编程", "入门"]
        ),
        DataRecord(
            title="机器学习基础",
            content="机器学习是人工智能的一个分支，通过算法让计算机从数据中学习并做出预测。",
            source="学术论文",
            category="人工智能",
            tags=["机器学习", "AI", "数据科学"]
        ),
        DataRecord(
            title="Web开发指南",
            content="Web开发包括前端和后端两个部分，前端负责用户界面，后端负责数据处理和业务逻辑。",
            source="技术博客",
            category="编程",
            tags=["Web", "前端", "后端"]
        ),
        DataRecord(
            title="数据库设计原则",
            content="良好的数据库设计应该遵循规范化原则，确保数据完整性和查询效率。",
            source="技术文档",
            category="数据库",
            tags=["数据库", "SQL", "设计"]
        ),
        DataRecord(
            title="云计算概述",
            content="云计算提供了弹性、可扩展的计算资源，企业可以按需使用和付费。",
            source="行业报告",
            category="云计算",
            tags=["云计算", "AWS", "Azure"]
        ),
    ]


def init_command(args):
    """初始化命令 - Initialize command."""
    storage = FileStorage(args.data_path)
    
    if args.with_samples:
        samples = create_sample_data()
        count = storage.save_all_records(samples)
        print(f"已初始化数据存储，创建了 {count} 条示例记录。")
        print(f"数据存储路径: {args.data_path}")
    else:
        print(f"已初始化数据存储路径: {args.data_path}")


def add_command(args):
    """添加记录命令 - Add record command."""
    storage = FileStorage(args.data_path)
    
    record = DataRecord(
        title=args.title,
        content=args.content or "",
        source=args.source or "",
        category=args.category or "",
        tags=args.tags.split(",") if args.tags else []
    )
    
    path = storage.save_record(record)
    print(f"已添加记录: {record.id}")
    print(f"保存路径: {path}")


def search_command(args):
    """搜索命令 - Search command."""
    storage = FileStorage(args.data_path)
    records = storage.load_all_records()
    
    retriever = DataRetriever(records)
    result = retriever.search(
        query=args.query,
        category=args.category,
        tags=args.tags.split(",") if args.tags else None,
        page=args.page,
        page_size=args.page_size
    )
    
    print(f"\n搜索关键词: {result.query or '(全部)'}")
    print(f"找到 {result.total_count} 条匹配记录 (耗时 {result.search_time_ms:.2f}ms)")
    print(f"当前第 {result.page} 页，共 {(result.total_count + result.page_size - 1) // result.page_size} 页")
    print("-" * 50)
    
    for i, record in enumerate(result.records, 1):
        print(f"\n{i}. {record.title or '(无标题)'}")
        if record.content:
            preview = record.content[:100]
            if len(record.content) > 100:
                preview += "..."
            print(f"   {preview}")
        if record.category:
            print(f"   分类: {record.category}")
        if record.tags:
            print(f"   标签: {', '.join(record.tags)}")
    
    # 可选：生成搜索报告
    if args.report:
        generator = ReportGenerator(args.report_path)
        report_path = generator.generate_search_report(result)
        print(f"\n报告已生成: {report_path}")


def list_command(args):
    """列表命令 - List command."""
    storage = FileStorage(args.data_path)
    records = storage.load_all_records()
    
    print(f"\n共有 {len(records)} 条记录:")
    print("-" * 50)
    
    for i, record in enumerate(records, 1):
        print(f"\n{i}. [{record.id[:8]}...] {record.title or '(无标题)'}")
        if record.category:
            print(f"   分类: {record.category}")
        if record.tags:
            print(f"   标签: {', '.join(record.tags)}")


def report_command(args):
    """生成报告命令 - Generate report command."""
    storage = FileStorage(args.data_path)
    records = storage.load_all_records()
    
    generator = ReportGenerator(args.report_path)
    
    if args.format == "md" or args.format == "markdown":
        report_path = generator.generate_summary_report(records, args.title or "数据检索报告")
    elif args.format == "json":
        report_path = generator.generate_json_report(records)
    elif args.format == "csv":
        report_path = generator.generate_csv_report(records)
    else:
        report_path = generator.generate_summary_report(records, args.title or "数据检索报告")
    
    print(f"报告已生成: {report_path}")


def delete_command(args):
    """删除记录命令 - Delete record command."""
    storage = FileStorage(args.data_path)
    
    if storage.delete_record(args.id):
        print(f"已删除记录: {args.id}")
    else:
        print(f"未找到记录: {args.id}")


def main():
    """主函数 - Main function."""
    parser = argparse.ArgumentParser(
        description="数据检索系统 - Data Retrieval System",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--data-path", "-d",
        default="data",
        help="数据存储路径 (默认: data)"
    )
    parser.add_argument(
        "--report-path", "-r",
        default="reports",
        help="报告输出路径 (默认: reports)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # init 命令
    init_parser = subparsers.add_parser("init", help="初始化数据存储")
    init_parser.add_argument("--with-samples", action="store_true", help="创建示例数据")
    init_parser.set_defaults(func=init_command)
    
    # add 命令
    add_parser = subparsers.add_parser("add", help="添加数据记录")
    add_parser.add_argument("title", help="记录标题")
    add_parser.add_argument("--content", "-c", help="记录内容")
    add_parser.add_argument("--source", "-s", help="数据来源")
    add_parser.add_argument("--category", help="分类")
    add_parser.add_argument("--tags", "-t", help="标签（逗号分隔）")
    add_parser.set_defaults(func=add_command)
    
    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索数据记录")
    search_parser.add_argument("query", nargs="?", default="", help="搜索关键词")
    search_parser.add_argument("--category", help="按分类过滤")
    search_parser.add_argument("--tags", "-t", help="按标签过滤（逗号分隔）")
    search_parser.add_argument("--page", "-p", type=int, default=1, help="页码")
    search_parser.add_argument("--page-size", type=int, default=10, help="每页数量")
    search_parser.add_argument("--report", action="store_true", help="生成搜索报告")
    search_parser.set_defaults(func=search_command)
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出所有记录")
    list_parser.set_defaults(func=list_command)
    
    # report 命令
    report_parser = subparsers.add_parser("report", help="生成报告")
    report_parser.add_argument("--format", "-f", choices=["md", "markdown", "json", "csv"], default="md", help="报告格式")
    report_parser.add_argument("--title", help="报告标题")
    report_parser.set_defaults(func=report_command)
    
    # delete 命令
    delete_parser = subparsers.add_parser("delete", help="删除记录")
    delete_parser.add_argument("id", help="记录ID")
    delete_parser.set_defaults(func=delete_command)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
