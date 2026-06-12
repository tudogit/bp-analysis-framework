# Business Process Analysis Framework (BP-AF)

完整的业务流程（BP）分析框架，支持Python和SQL实现，包含数据挖掘、性能分析、流程可视化和最佳实践。

## 🎯 核心功能

- ✅ **流程事件管理**：事件日志存储与查询
- ✅ **数据抽取转换**：ETL 管道
- ✅ **性能分析**：周期时间、吞吐量、瓶颈检测
- ✅ **流程挖掘**：流程发现、合规检查
- ✅ **可视化**：Sankey 图、甘特图、性能指标
- ✅ **仪表板**：实时监控面板

## 📋 快速开始

### 1. 环境配置

```bash
# 克隆仓库
git clone https://github.com/tudogit/bp-analysis-framework.git
cd bp-analysis-framework

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 数据库初始化

```bash
# PostgreSQL
psql -U postgres -d bp_analysis < db/schema.sql

# 或 SQLite (开发环境)
python db/init_sqlite.py
```

### 3. 基础使用

```python
from bp_analysis.core import BPAnalyzer
from bp_analysis.connectors import SQLiteConnector

# 初始化分析器
connector = SQLiteConnector('bp_analysis.db')
analyzer = BPAnalyzer(connector)

# 导入事件日志
analyzer.import_events('data/sample_events.csv')

# 分析流程
metrics = analyzer.calculate_metrics()
print(metrics)

# 生成可视化
analyzer.visualize_process_flow(output='process_flow.html')
```

## 📁 项目结构

```
bp-analysis-framework/
├── README.md
├── requirements.txt
├── setup.py
├── .gitignore
│
├── db/
│   ├── schema.sql
│   ├── schema_sqlite.sql
│   └── init_sqlite.py
│
├── bp_analysis/
│   ├── __init__.py
│   ├── core.py
│   ├── models.py
│   ├── config.py
│   ├── connectors/
│   ├── etl/
│   ├── analysis/
│   ├── visualization/
│   └── utils/
│
├── tests/
├── examples/
├── data/
├── docs/
└── scripts/
```

## 🚀 核心特性

### 1. 流程事件管理
- 批��导入事件日志（CSV、JSON、XLS）
- 事件去重与验证
- 时间序列索引优化

### 2. 性能分析
- **周期时间**：从开始到完成的平均时间
- **吞吐量**：单位时间内完成的流程数
- **资源利用率**：员工/系统的工作负载
- **等待时间**：活动间隔分析

### 3. 流程挖掘
- 自动流程发现（Alpha、Heuristics 算法）
- 流程变异检测
- 异常路径识别

### 4. 可视化
- Sankey 流程图（活动流转）
- 性能热力图（瓶颈识别）
- 甘特图（时间分布）
- 仪表板（KPI 监控）

## 📖 文档

- [架构设计](docs/ARCHITECTURE.md)
- [最佳实践](docs/BEST_PRACTICES.md)
- [API 参考](docs/API_REFERENCE.md)
- [教程](docs/TUTORIALS.md)
- [故障排除](docs/TROUBLESHOOTING.md)

## 📞 支持

- 📧 Email: support@bp-analysis.dev
- 💬 Issues: GitHub Issues
- 📚 Wiki: 项目 Wiki

---

MIT License | 2024 BP Analysis Team
