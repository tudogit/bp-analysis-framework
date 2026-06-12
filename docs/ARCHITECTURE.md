```markdown
# BP 分析框架 - 架构设计文档

## 系统架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                     前端/API 层                              │
│  (Flask/FastAPI REST APIs, Web Dashboard)                   │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   BPAnalyzer 核心类                          │
│  - import_events()      数据导入                             │
│  - calculate_metrics()  指标计算                             │
│  - discover_process()   流程挖掘                             │
│  - detect_bottlenecks() 瓶颈检测                             │
└────┬───────────────┬────���─────────┬───────────────┬──────────┘
     │               │              │               │
┌────▼──┐    ┌──────▼─────┐  ┌─────▼──────┐  ┌────▼─────────┐
│ ETL   │    │  Analysis  │  │Visualization│  │  Connectors  │
│Pipeline│    │  Modules   │  │  Modules   │  │  (DB Layer)  │
└────┬──┘    └──────┬─────┘  └─────┬──────┘  └────┬─────────┘
     │              │              │              │
     │              │              │              │
┌────▼──────────────▼──────────────▼──────────────▼─────────┐
│                    数据库层                                  │
│  (PostgreSQL / SQLite)                                      │
│  - process_instances     流程实例                           │
│  - process_events        事件日志                           │
│  - performance_metrics   性能指标                           │
│  - anomalies             异常记录                           │
└─────────────────────────────────────────────────────────────┘
```

## 模块设计

### 1. ETL 管道 (bp_analysis/etl/)

**职责**: 数据清洗、转换、验证

```python
DataTransformer
├── normalize_events()     # 数据规范化
├── validate_events()      # 数据验证
├── remove_duplicates()    # 去重处理
└── sort_events()          # 排序
```

**流程**:
```
Raw Data → Normalize → Validate → Remove Duplicates → Sort → Database
```

### 2. 分析模块 (bp_analysis/analysis/)

#### PerformanceAnalyzer - 性能分析
```python
calculate_all_metrics()
├── 周期时间 (Cycle Time)
├── 吞吐量 (Throughput)
├── 完成率 (Completion Rate)
└── 等待时间 (Waiting Time)
```

#### ProcessDiscovery - 流程挖掘
```python
discover_flow_alpha_algorithm()  # Alpha 算法
│
├── 提取活动集合
├── 发现转移关系
└── 计算流程变异

extract_variants()
└── 按频率聚合流程路径
```

#### BottleneckDetector - 瓶颈检测
```python
detect()
├── 统计活动耗时分布
├── 计算百分位数
├── 识别异常活动
└── 评估严重程度
```

### 3. 连接器层 (bp_analysis/connectors/)

**设计模式**: 策略模式 + 工厂模式

```python
BaseConnector (ABC)
├── SQLiteConnector    # 开发环境
├── PostgreSQLConnector (可选扩展)
└── MySQLConnector     (可选扩展)
```

**关键方法**:
```python
connect()                      # 建立连接
bulk_insert_events()           # 批量插入
get_instances_by_process()     # 查询实例
get_events_by_process()        # 查询事件
execute_query()                # 自定义查询
```

### 4. 核心类 (bp_analysis/core.py)

**BPAnalyzer** - 主分析器

```python
class BPAnalyzer:
    ├── __init__(connector, cache_enabled)
    ├── import_events()           # 导入事件
    ├── calculate_metrics()       # 计算指标
    ├── discover_process_flow()   # 发现流程
    ├── detect_bottlenecks()      # 检测瓶颈
    └── export_results()          # 导出结果
```

## 数据流

### 导入流程
```
CSV/JSON/XLSX
    ↓
[DataTransformer]
    ├── normalize_events()
    ├── validate_events()
    └── remove_duplicates()
    ↓
[SQLiteConnector]
    └── bulk_insert_events()
    ↓
Database
    ├── process_instances
    └── process_events
```

### 分析流程
```
Database
    ↓
[EventRetrieval]
    └── get_events_by_process()
    ↓
[DataFrame Processing]
    └── pandas operations
    ↓
[PerformanceAnalyzer]
    ├── calculate_cycle_time()
    └── calculate_throughput()
    ↓
Results Dictionary
    ↓
[Visualization/Export]
    └── JSON/CSV output
```

## 缓存策略

**启用条件**: `cache_enabled=True`

**缓存键生成**:
```python
cache_key = f"metrics_{process_name}_{start_date}_{end_date}"
```

**失效条件**:
- 导入新数据后自动清空
- 显式调用 `_clear_cache()`

## 错误处理

### 数据验证
```
Missing required columns      → Warning + Continue
Null values in critical cols  → Warning + Continue
Duplicate events             → Removed automatically
Invalid timestamps           → Converted to datetime
```

### 数据库错误
```
Connection failed            → Raise + Log
Insert failed               → Rollback + Raise + Log
Query error                 → Log + Return empty
```

## 扩展性设计

### 添加新的分析器

```python
# 1. 创建新模块
class MyAnalyzer:
    def __init__(self, connector):
        self.connector = connector
    
    def analyze(self):
        pass

# 2. 注册到 BPAnalyzer
class BPAnalyzer:
    def __init__(self, connector):
        self.my_analyzer = MyAnalyzer(connector)
```

### 添加新的数据库连接

```python
# 1. 继承 BaseConnector
class PostgreSQLConnector(BaseConnector):
    def connect(self):
        pass
    # 实现其他必要方法

# 2. 使用
analyzer = BPAnalyzer(PostgreSQLConnector(...))
```

## 性能优化

### 索引策略
```sql
-- 关键字段索引
CREATE INDEX idx_process_instances_name ON process_instances(process_name);
CREATE INDEX idx_process_events_instance ON process_events(instance_id);
CREATE INDEX idx_process_events_time ON process_events(timestamp);
```

### 批量操作
```python
# 批量插入而不是逐行插入
df.to_sql('process_events', connection, if_exists='append')
```

### 查询优化
```python
# 预过滤而不是全表扫描
WHERE process_name = ? AND timestamp BETWEEN ? AND ?
```

## 部署架构

### 开发环境
```
SQLite (in-memory or file-based)
├── 低延迟
├── 无需配置
└── 适合 < 1GB 数据
```

### 生产环境
```
PostgreSQL (可选 TimescaleDB 扩展)
├── 高并发
├── 时序数据优化
├── 集群支持
└── 备份恢复
```

## 安全考虑

### SQL 注入防护
```python
# ✓ 正确
cursor.execute("SELECT * FROM events WHERE name = ?", (name,))

# ✗ 错误
cursor.execute(f"SELECT * FROM events WHERE name = '{name}'")
```

### 环境变量配置
```bash
# .env 文件
DATABASE_URL=postgresql://user:pass@host/db
API_SECRET_KEY=...
LOG_LEVEL=INFO
```

## 监控和日志

### 日志分级
- `DEBUG` - 详细开发信息
- `INFO` - 一般运行信息
- `WARNING` - 潜在问题
- `ERROR` - 失败操作

### 日志输出
```
logs/
└── bp_analysis.log
    ├── 文件输出
    └── 控制台输出
```
```
