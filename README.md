# GolvInfoToFileSystem

一个进行信息检索的仓库，检索信息后存储到仓库就可查看，还可以生成报告。

A data retrieval system that searches for information, stores it in the repository, and can generate reports.

## 功能特性 / Features

- 📝 **数据管理**: 添加、删除、修改数据记录
- 🔍 **数据检索**: 支持关键词搜索、分类过滤、标签过滤
- 💾 **持久化存储**: 将数据保存到文件系统
- 📊 **报告生成**: 支持Markdown、JSON、CSV多种格式报告

## 快速开始 / Quick Start

### 初始化数据存储

```bash
# 初始化并创建示例数据
python main.py init --with-samples

# 仅初始化存储目录
python main.py init
```

### 添加数据记录

```bash
python main.py add "记录标题" --content "记录内容" --category "分类" --tags "标签1,标签2"
```

### 搜索数据

```bash
# 关键词搜索
python main.py search "Python"

# 按分类搜索
python main.py search --category "编程"

# 按标签搜索
python main.py search --tags "机器学习,AI"

# 搜索并生成报告
python main.py search "Python" --report
```

### 列出所有记录

```bash
python main.py list
```

### 生成报告

```bash
# 生成Markdown报告
python main.py report --format md

# 生成JSON报告
python main.py report --format json

# 生成CSV报告
python main.py report --format csv
```

### 删除记录

```bash
python main.py delete <记录ID>
```

## 项目结构 / Project Structure

```
GolvInfoToFileSystem/
├── main.py                 # 主程序入口
├── src/
│   ├── __init__.py
│   ├── data_retrieval/     # 数据检索模块
│   │   ├── __init__.py
│   │   ├── models.py       # 数据模型
│   │   └── retriever.py    # 数据检索器
│   ├── storage/            # 存储模块
│   │   ├── __init__.py
│   │   └── file_storage.py # 文件存储实现
│   └── report/             # 报告模块
│       ├── __init__.py
│       └── generator.py    # 报告生成器
├── data/                   # 数据存储目录
├── reports/                # 报告输出目录
└── tests/                  # 测试目录
    ├── test_models.py
    ├── test_retriever.py
    ├── test_storage.py
    └── test_report.py
```

## 测试 / Testing

```bash
# 运行所有测试
python -m pytest tests/

# 或使用unittest
python -m unittest discover tests/
```

## 许可证 / License

MIT License
