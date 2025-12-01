# 智能瞭望数据分析处理系统

一个基于Flask的智能数据分析处理平台，集成了数据采集、存储、分析和报告生成功能。

## 功能特性

### 🔍 数据采集
- **百度爬虫集成**: 自动化采集百度搜索结果
- **智能关键词搜索**: 支持多关键词批量搜索
- **结果预览**: 实时查看搜索结果
- **数据筛选**: 按时间、关键词等条件筛选

### 📊 数据仓库
- **SQLite数据存储**: 轻量级数据库存储
- **分类管理**: 按日期和关键词自动分类
- **批量操作**: 支持数据的批量删除和导出
- **快速检索**: 多条件组合搜索

### 📋 报告生成
- **PDF报告**: 自动生成专业的数据分析报告
- **自定义模板**: 支持多种报告模板
- **批量导出**: 一键导出多个报告
- **报告管理**: 历史报告查看和下载

### 🎨 用户界面
- **响应式设计**: 支持PC和移动端访问
- **现代化UI**: 采用Bootstrap和渐变设计
- **科技感风格**: 专业的数据可视化界面
- **用户友好**: 直观的操作体验

## 技术栈

- **后端框架**: Flask
- **数据库**: SQLite
- **前端框架**: Bootstrap 5
- **CSS预处理器**: 原生CSS + 自定义样式
- **JavaScript**: 原生JS + jQuery
- **PDF生成**: ReportLab
- **爬虫**: requests + BeautifulSoup

## 快速开始

### 环境要求
- Python 3.7+
- pip包管理器

### 安装依赖
```bash
# 克隆项目
git clone [项目地址]
cd GovInfoToFileSystem

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 运行应用
```bash
# 启动应用
python run.py

# 访问系统
打开浏览器访问: http://localhost:5000
```

### 默认账号
- 用户名: admin
- 密码: admin123

## 项目结构

```
GovInfoToFileSystem/
├── app/                    # 应用主目录
│   ├── __init__.py        # 应用初始化
│   ├── config.py          # 配置文件
│   ├── models/            # 数据模型
│   │   ├── user.py        # 用户模型
│   │   └── data.py        # 数据模型
│   ├── routes/            # 路由处理
│   │   ├── auth.py        # 认证路由
│   │   ├── main.py        # 主页面路由
│   │   ├── crawler.py     # 爬虫路由
│   │   ├── data_warehouse.py  # 数据仓库路由
│   │   └── report.py      # 报告路由
│   ├── services/          # 业务逻辑
│   │   ├── baidu_spider.py    # 百度爬虫服务
│   │   └── pdf_generator.py   # PDF生成服务
│   ├── static/            # 静态文件
│   │   ├── css/           # 样式文件
│   │   ├── js/            # JavaScript文件
│   │   └── images/        # 图片文件
│   ├── templates/         # HTML模板
│   │   ├── auth/          # 认证相关模板
│   │   ├── crawler/       # 爬虫页面模板
│   │   ├── warehouse/     # 数据仓库模板
│   │   ├── base.html      # 基础模板
│   │   └── dashboard.html # 控制台模板
│   └── utils/             # 工具函数
│       └── pdf_generator.py   # PDF生成工具
├── run.py                 # 启动脚本
└── requirements.txt       # 依赖列表
```

## 使用说明

### 1. 用户认证
- 支持用户注册和登录
- 默认管理员账号自动创建
- 安全的密码加密存储

### 2. 数据采集
- 输入关键词进行搜索
- 设置最大结果数量
- 实时查看采集进度
- 一键保存到数据仓库

### 3. 数据管理
- 按日期和关键词浏览数据
- 支持批量删除操作
- 快速搜索和筛选
- 数据详情查看

### 4. 报告生成
- 选择数据生成PDF报告
- 自定义报告标题和内容
- 批量生成多个报告
- 下载和管理历史报告

## 开发说明

### 添加新功能
1. 在相应的模块中添加业务逻辑
2. 创建对应的路由处理函数
3. 设计HTML模板页面
4. 添加必要的CSS和JavaScript

### 数据库操作
- 使用SQLAlchemy ORM进行数据库操作
- 模型定义在`app/models/`目录下
- 支持数据库迁移和版本控制

### 前端开发
- 使用Bootstrap 5构建响应式界面
- 自定义CSS样式在`app/static/css/custom.css`
- JavaScript工具函数在`app/static/js/utils.js`

## 安全说明

- 用户密码使用Werkzeug进行安全加密
- 实现CSRF保护
- 输入验证和过滤
- 安全的会话管理

## 性能优化

- 数据库查询优化
- 静态文件缓存
- 前端资源压缩
- 异步任务处理

## 故障排除

### 常见问题
1. **数据库连接失败**: 检查SQLite数据库文件权限
2. **爬虫无法工作**: 检查网络连接和目标网站可访问性
3. **PDF生成失败**: 确保ReportLab库正确安装
4. **页面显示异常**: 清除浏览器缓存或检查静态文件路径

### 日志查看
- Flask应用日志在控制台输出
- 可以配置日志文件保存路径
- 支持不同级别的日志记录

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 基础功能实现
- 用户认证系统
- 数据采集功能
- 数据仓库管理
- PDF报告生成

## 贡献指南

欢迎提交Issue和Pull Request来改进这个项目。

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 邮箱: [your-email@example.com]
- GitHub Issues: [项目地址]/issues

---

**注意**: 这是一个演示项目，请勿在生产环境中直接使用默认配置。