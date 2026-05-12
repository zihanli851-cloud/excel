# 项目清单筛选查询插件 - 后端 A 开发设计文档

版本：V1.0  
日期：2026-05-12  
范围：后端 A  
参考文档：

- 《需求文档_项目清单筛选查询插件_V2.docx》
- 《开发文档_项目清单筛选查询插件_V2.docx》

## 实施进度

- [x] ~~搭建 backend 目录、依赖清单与配置骨架~~
- [x] ~~实现数据库连接、Project 模型与初始化入口~~
- [x] ~~实现金额解析、表头校验、年度解析、黄色识别、无效分类~~
- [x] ~~实现 Excel 导入服务和上传接口~~
- [x] ~~实现 Excel 导出服务~~
- [x] ~~补充 pytest 单元测试与基础验证~~

## 补充实施进度

- [x] ~~补齐迁移/初始化 SQL 与项目响应 schema~~
- [x] ~~补齐后端 B/前端预留路由与导出占位接口~~
- [x] ~~增强导入批量写入、金额 warning、表头多字段 warning~~
- [x] ~~补充对应测试并做可运行验证~~

## 1. 后端 A 定位

后端 A 负责项目的数据底座和文件处理能力，目标是在不依赖前端完整完成、不依赖后端 B 全部接口完成的情况下，先跑通：

```text
Excel 文件 -> 表头校验 -> Sheet 年度解析 -> 行数据清洗 -> 黄色无效数据识别 -> 金额解析 -> SQLite 入库 -> 可供查询 API 使用的数据模型
```

后端 A 本阶段优先完成稳定、可复用、可测试的数据导入与导出基础能力。前端与后端 B 的部分只保留必要接口契约和协作边界，不在本文档中展开实现。

## 2. 分工边界

| 角色 | 本文档处理方式 | 说明 |
|---|---|---|
| 后端 A | 详细设计并实现 | 项目骨架、配置管理、数据库模型、Excel 导入、金额解析、无效数据识别、导出服务底层能力 |
| 后端 B | 预留接口契约 | 查询 API、认证、审计、查询历史、复核接口由后端 B 实现，后端 A 提供数据模型与服务函数 |
| 前端 | 预留对接字段 | 查询页、结果列表、导入页、登录页、审计页等由前端实现，后端 A 保证字段和数据语义稳定 |

## 3. 技术架构

### 3.1 推荐技术栈

| 模块 | 技术 | 说明 |
|---|---|---|
| Web 框架 | FastAPI | 轻量、Swagger 友好，便于前后端联调 |
| ORM | SQLAlchemy 2.x | 同时支持 SQLite 与 PostgreSQL |
| 数据校验 | Pydantic Settings / Pydantic | 配置与 DTO 结构化 |
| Excel 解析 | openpyxl | 可读取单元格填充色，用于识别黄色无效行 |
| 数据库 | SQLite 开发 / PostgreSQL 生产 | 通过 DB_URL 切换 |
| 迁移 | Alembic | 后续表结构变更可控 |
| 测试 | pytest | 覆盖金额解析、无效分类、导入流程 |

### 3.2 目录结构建议

```text
backend/
  app/
    main.py
    core/
      config.py
      database.py
      logging.py
    models/
      project.py
      user.py
      audit_log.py
      query_history.py
    schemas/
      project.py
      import_result.py
      export.py
    services/
      excel_importer.py
      excel_exporter.py
      amount_parser.py
      invalid_classifier.py
      project_repository.py
    api/
      deps.py
      routes/
        import_routes.py        # 后端 A 可先提供
        export_routes.py        # 可先提供底层能力，路由可与后端 B 协调
        project_routes.py       # 后端 B 主责，后端 A 预留
        auth_routes.py          # 后端 B 主责
        audit_routes.py         # 后端 B 主责
    migrations/
    tests/
      test_amount_parser.py
      test_invalid_classifier.py
      test_excel_importer.py
  uploads/
  exports/
  .env.example
  requirements.txt
```

## 4. 配置设计

所有环境差异必须从配置读取，不写死在业务代码中。

| 配置项 | 开发默认值 | 生产示例 | 后端 A 用途 |
|---|---|---|---|
| DB_URL | sqlite:///./dev.db | postgresql://user:pass@server/project_list | 数据库连接 |
| EXCEL_UPLOAD_DIR | ./uploads | /data/uploads | 上传文件保存目录 |
| EXCEL_EXPORT_DIR | ./exports | /data/exports | 导出文件临时目录 |
| SECRET_KEY | dev-only-key | 生产强随机值 | 预留给后端 B 认证 |
| LOG_LEVEL | DEBUG | INFO | 日志级别 |
| IMPORT_BATCH_SIZE | 500 | 1000 | 批量入库大小 |

`.env.example` 示例：

```env
APP_NAME=project-list-plugin
ENV=dev
DB_URL=sqlite:///./dev.db
EXCEL_UPLOAD_DIR=./uploads
EXCEL_EXPORT_DIR=./exports
SECRET_KEY=change-me-in-production
LOG_LEVEL=DEBUG
IMPORT_BATCH_SIZE=500
```

## 5. 数据库设计

### 5.1 projects 项目清单表

金额字段采用“原文 TEXT + 解析数字 NUMERIC”的双字段策略，保证展示不丢原始信息，同时支持范围筛选。

| 字段名 | 类型 | 约束 | 说明 |
|---|---|---|---|
| id | Integer | PK | 自增主键 |
| seq_no | Integer | nullable | Excel 原始序号 |
| project_name | Text | not null | 项目名称 |
| project_code | String(50) | index | 项目编号，通常以 P 开头 |
| purchaser | Text | index | 采购人 |
| bid_open_date | Date | index nullable | 开标时间 |
| commission_amount | Text | nullable | 委托金额原文 |
| commission_num | Numeric(18, 4) | nullable | 委托金额解析数字 |
| max_price | Text | nullable | 最高限价原文 |
| max_price_num | Numeric(18, 4) | nullable | 最高限价解析数字 |
| bid_amount | Text | nullable | 中标金额原文 |
| bid_amount_num | Numeric(18, 4) | nullable | 中标金额解析数字 |
| bid_amount_detail | Text | nullable | 中标金额分包明细原文 |
| sheet_year | SmallInteger | not null, index | 所属 Sheet 年度 |
| is_invalid | Boolean | not null, default false, index | 是否无效数据 |
| invalid_reason | String(50) | nullable, index | 无效原因 |
| source_file | String(255) | nullable | 来源文件名 |
| source_sheet | String(100) | nullable | 来源 Sheet 名 |
| source_row | Integer | nullable | Excel 原始行号 |
| row_hash | String(64) | unique/index | 用于重复导入识别 |
| created_at | DateTime | not null | 导入时间 |
| updated_at | DateTime | not null | 更新时间 |

建议唯一策略：

- 首选 `project_code` 非空时，使用 `project_code + sheet_year` 去重。
- 若 `project_code` 为空，使用 `row_hash` 去重。
- `row_hash` 建议由 `sheet_year + source_sheet + seq_no + project_name + purchaser + bid_open_date` 生成。

### 5.2 invalid_reason 枚举

| 枚举值 | 含义 | 识别关键词 |
|---|---|---|
| BID_FAILED | 废标 | 废标、投标人不足、有效投标人不足 |
| TERMINATED | 终止采购 | 终止采购、供应商不足 |
| CANCELLED | 采购取消 | 采购任务取消、重大变故 |
| WINNER_QUIT | 中标人放弃 | 放弃中标、重新开展 |
| BREACH | 履约失败 | 无法履约、自愿放弃签订 |
| OTHER | 其他 | 黄色标记但未匹配关键词 |

### 5.3 后端 B 预留表

以下表由后端 B 负责业务实现，后端 A 可先在迁移中建表或提供模型占位，避免后续联调时重复调整结构。

| 表名 | 主责 | 用途 |
|---|---|---|
| users | 后端 B | 登录用户、角色、启停状态 |
| audit_logs | 后端 B | 查询、导出、复核、导入、登录操作留痕 |
| query_history | 后端 B | 近期查询条件保存与复用 |

## 6. Excel 导入模块设计

### 6.1 输入约束

导入文件必须满足：

- Excel 工作簿按年度分 Sheet，例如 `2023年`。
- 每个有效 Sheet 使用统一 9 字段表头。
- 黄色背景行表示无效数据，不可删除，只做标记。
- 金额字段可能是数字、`360.28万元`、`无`、`单价限价`、`废标` 等混合格式。

预期表头：

| Excel 字段 | 入库字段 |
|---|---|
| 序号 | seq_no |
| 项目名称 | project_name |
| 项目编号 | project_code |
| 采购人 | purchaser |
| 开标时间 | bid_open_date |
| 委托金额(万元)合计 | commission_amount / commission_num |
| 最高限价(万元)（分包） | max_price / max_price_num |
| 中标金额(万元)合计 | bid_amount / bid_amount_num |
| 中标金额(万元)（分包） | bid_amount_detail |

### 6.2 导入流程

```text
1. 保存上传文件到 EXCEL_UPLOAD_DIR
2. 使用 openpyxl load_workbook(file, data_only=False) 读取工作簿
3. 遍历 Sheet，解析 Sheet 年度
4. 定位并校验表头
5. 逐行读取数据
6. 判断是否为空行，跳过全空行
7. 检测行背景色，识别黄色无效标记
8. 从中标金额字段按关键词分类 invalid_reason
9. 解析三个金额字段的数字值
10. 生成 Project ORM 对象
11. 批量 upsert / insert
12. 返回导入统计与异常明细
```

### 6.3 表头校验策略

导入前必须做表头校验，避免真实 Excel 格式变化导致错误入库。

校验规则：

- 支持字段名前后空格、换行、全角半角括号差异的归一化。
- 必须包含 9 个核心字段。
- 若缺少字段，直接终止导入，返回缺失字段列表。
- 若多出字段，本期可忽略，但记录 warning。

### 6.4 Sheet 年度解析

支持：

- `2023年` -> `2023`
- `2023` -> `2023`
- `项目清单2023` -> `2023`

如果 Sheet 名无法解析年份：

- 默认跳过该 Sheet。
- 在导入结果 `warnings` 中记录。

### 6.5 黄色背景识别

黄色识别以单元格填充色为主，内容关键词为辅。

建议规则：

- 扫描整行核心字段单元格，只要存在明显黄色填充，则该行视为无效数据。
- 支持常见黄色 RGB：`FFFF00`、`FFFFFF00`、`FFFF99`、`FFF2CC`。
- 若颜色不是标准黄色，但色相接近黄色，可通过 RGB 阈值判断：
  - R >= 220
  - G >= 200
  - B <= 180
- 如果背景不是黄色，但中标金额字段包含废标、终止采购等强关键词，可标记为无效，来源记录为 `keyword_detected`。

### 6.6 无效原因分类

按优先级匹配中标金额字段和必要时的整行文本：

```text
BID_FAILED    -> 废标、投标人不足、有效投标人不足
TERMINATED    -> 终止采购、供应商不足
CANCELLED     -> 采购任务取消、重大变故
WINNER_QUIT   -> 放弃中标、重新开展
BREACH        -> 无法履约、自愿放弃签订
OTHER         -> 黄色标记但未命中以上关键词
```

分类函数必须纯函数化，方便单元测试：

```python
def classify_invalid_reason(text: str, is_yellow: bool) -> str | None:
    ...
```

返回规则：

- 非黄色且无关键词：`None`
- 黄色但无关键词：`OTHER`
- 命中关键词：返回对应枚举

### 6.7 金额解析

金额解析只提取可用于范围筛选的数字，不改变原文。

示例：

| 原文 | 解析值 |
|---|---|
| `360.28` | `360.28` |
| `360.28万元` | `360.28` |
| `约 50 万元` | `50` |
| `1,200.50` | `1200.50` |
| `无` | `NULL` |
| `单价限价` | `NULL` |
| `废标` | `NULL` |

实现要求：

- 返回 `Decimal | None`。
- 解析失败不抛出业务中断异常，只记录 warning。
- 支持中文空格、英文逗号、全角数字的基础归一化。
- 不推断单位换算，文档字段本身以“万元”为单位，解析出的数字默认仍按万元存储。

### 6.8 导入结果返回结构

导入服务返回结构建议：

```json
{
  "file_name": "项目清单-脱敏模板.xlsx",
  "total_rows": 423,
  "imported_rows": 423,
  "valid_rows": 337,
  "invalid_rows": 86,
  "skipped_rows": 0,
  "sheet_stats": [
    {
      "sheet_name": "2023年",
      "sheet_year": 2023,
      "total_rows": 423,
      "imported_rows": 423,
      "invalid_rows": 86
    }
  ],
  "warnings": [
    {
      "sheet": "说明",
      "row": null,
      "field": null,
      "message": "Sheet 名无法解析年份，已跳过"
    }
  ]
}
```

## 7. Excel 导出模块设计

导出模块由后端 A 提供底层能力，具体导出入口可由后端 B 在查询 API 完成后调用。

### 7.1 输入

```python
def export_projects(projects: list[Project], file_name: str | None = None) -> ExportResult:
    ...
```

### 7.2 输出要求

- 导出为 `.xlsx`。
- 文件名格式：`查询结果_YYYYMMDD_HHmmss.xlsx`。
- 字段保持与原始 Excel 一致。
- 无效数据行使用黄色背景。
- 表头加粗。
- 冻结首行。
- 自动列宽。
- 日期和金额展示使用原文字段，不用解析数字替换原文。

### 7.3 字段顺序

```text
序号
项目名称
项目编号
采购人
开标时间
委托金额(万元)合计
最高限价(万元)（分包）
中标金额(万元)合计
中标金额(万元)（分包）
无效原因
所属年度
```

## 8. 给后端 B 的预留契约

后端 B 实现查询 API 时，建议直接基于后端 A 的 `projects` 表和 repository 方法。

### 8.1 查询参数

| 参数 | 类型 | 说明 |
|---|---|---|
| keyword | string | 项目名称模糊搜索 |
| code | string | 项目编号精确或前缀匹配 |
| purchaser | string | 采购人筛选 |
| date_from | date | 开标开始日期 |
| date_to | date | 开标结束日期 |
| amount_min | decimal | 金额下限 |
| amount_max | decimal | 金额上限 |
| amount_field | enum | `commission` / `max_price` / `bid_amount` / `any` |
| invalid_mode | enum | `valid_only` / `all` / `invalid_only` |
| invalid_reason | enum | 无效原因筛选 |
| page | int | 页码 |
| page_size | int | 每页条数 |
| sort_by | string | 排序字段 |
| sort_order | enum | `asc` / `desc` |

### 8.2 无效数据过滤语义

| invalid_mode | SQL 语义 |
|---|---|
| valid_only | `is_invalid = false` |
| all | 不追加 `is_invalid` 条件 |
| invalid_only | `is_invalid = true`，可叠加 `invalid_reason` |

### 8.3 金额字段过滤语义

| amount_field | SQL 语义 |
|---|---|
| commission | 使用 `commission_num` |
| max_price | 使用 `max_price_num` |
| bid_amount | 使用 `bid_amount_num` |
| any | 三个数字字段任意一个满足范围 |

### 8.4 后端 A 可提供的 Repository 方法

```python
class ProjectRepository:
    def bulk_upsert(self, projects: list[Project]) -> ImportWriteResult:
        ...

    def get_by_id(self, project_id: int) -> Project | None:
        ...

    def list_purchasers(self) -> list[str]:
        ...

    def count_invalid_by_reason(self) -> dict[str, int]:
        ...

    def search_base_query(self):
        """返回后端 B 可继续拼接条件的 SQLAlchemy query/select。"""
        ...
```

## 9. 给前端的预留字段

前端展示结果时，建议使用以下字段。字段名由后端 B API 统一返回，后端 A 保证数据库层含义稳定。

```json
{
  "id": 1,
  "seq_no": 1,
  "project_name": "某项目",
  "project_code": "P20260917341",
  "purchaser": "某采购人",
  "bid_open_date": "2026-05-12",
  "commission_amount": "360.28万元",
  "commission_num": "360.2800",
  "max_price": "单价限价",
  "max_price_num": null,
  "bid_amount": "投标人不足三家，废标",
  "bid_amount_num": null,
  "bid_amount_detail": "",
  "sheet_year": 2026,
  "is_invalid": true,
  "invalid_reason": "BID_FAILED"
}
```

前端只需要根据：

- `is_invalid = true` 时显示黄色行背景。
- `invalid_reason` 显示中文原因。
- 原文金额字段用于展示。
- `*_num` 字段主要用于筛选，不建议直接展示给业务用户。

## 10. 后端 A 接口建议

后端 A 至少可先提供导入接口，便于联调。

### 10.1 上传导入

```http
POST /api/import/upload
Content-Type: multipart/form-data
Authorization: Bearer <token>

file=<xlsx>
```

响应：

```json
{
  "success": true,
  "data": {
    "file_name": "项目清单-脱敏模板.xlsx",
    "total_rows": 423,
    "imported_rows": 423,
    "valid_rows": 337,
    "invalid_rows": 86,
    "warnings": []
  }
}
```

鉴权由后端 B 负责。后端 A 初期可临时跳过鉴权或使用依赖占位，但路由路径和响应结构保持稳定。

### 10.2 导出服务占位

```http
POST /api/projects/export
```

该路由最终由后端 B 负责按查询条件取数并调用后端 A 的 `excel_exporter`。后端 A 本阶段只保证 `export_projects()` 可被调用。

## 11. 测试计划

### 11.1 单元测试

| 测试对象 | 覆盖点 |
|---|---|
| amount_parser | 数字、数字加单位、逗号、全角数字、纯文字、空值 |
| invalid_classifier | 废标、终止采购、取消、放弃、履约失败、OTHER、非无效 |
| header_validator | 正常表头、缺字段、多字段、空格换行、括号差异 |
| sheet_year_parser | `2023年`、`2023`、`项目清单2023`、无法解析 |
| color_detector | 标准黄色、浅黄色、非黄色、无填充 |

### 11.2 集成测试

使用脱敏模板 Excel 跑完整导入：

- 总行数约 423 行。
- 无效数据约 86 行。
- `projects` 表数据完整。
- 黄色行可识别为 `is_invalid = true`。
- 金额文本保留，数字字段尽量解析。
- 解析失败不影响导入。

### 11.3 验收检查

后端 A 完成标准：

- 能启动 FastAPI 服务。
- 能初始化 SQLite 数据库。
- 能通过接口或脚本导入脱敏 Excel。
- 能正确生成 `projects` 数据。
- 能识别黄色无效行并分类。
- 能解析委托金额、最高限价、中标金额数字字段。
- 能提供导出服务函数并生成符合格式的 Excel。
- 给后端 B 的查询字段和 repository 方法可用。

## 12. 实施顺序

建议按以下顺序开发：

1. 创建后端项目骨架与配置模块。
2. 建立 SQLAlchemy 数据库连接和 `projects` 模型。
3. 配置 Alembic 或初始化建表脚本。
4. 实现金额解析、年度解析、表头归一化、黄色识别、无效分类等纯函数。
5. 实现 Excel 导入服务。
6. 实现导入 API 或导入 CLI。
7. 使用脱敏 Excel 完整导入验证。
8. 实现导出服务函数。
9. 补单元测试和集成测试。
10. 与后端 B 对齐查询字段、无效模式、金额模式。

## 13. 风险与处理

| 风险 | 表现 | 后端 A 处理方式 |
|---|---|---|
| 真实 Excel 表头变化 | 字段缺失或顺序不同 | 表头归一化 + 缺字段直接报错 + 多字段 warning |
| 黄色识别不稳定 | 无效漏标或误标 | 背景色为主，关键词为辅，颜色阈值可配置 |
| 金额格式复杂 | 范围筛选漏数据 | 原文保留，数字解析失败置 NULL 并记录 warning |
| 重复导入 | 数据重复 | 使用 `project_code + sheet_year` 或 `row_hash` 去重 |
| 后端 B 尚未完成 | 无法完整查询联调 | 后端 A 提供导入 API、repository 和测试脚本先独立验证 |
| 前端尚未完成 | 无页面上传 | 后端 A 提供 Swagger 或 CLI 导入入口 |

## 14. 本阶段交付物

后端 A 本阶段应交付：

- 可运行的 FastAPI 后端骨架。
- `.env.example` 配置模板。
- 数据库模型与初始化脚本/迁移。
- Excel 导入模块。
- 金额解析模块。
- 黄色无效数据识别模块。
- 无效原因分类模块。
- Excel 导出服务模块。
- 单元测试与导入集成测试。
- 一份导入脱敏 Excel 后的统计结果说明。

当前验证说明：

- 已通过 AST 语法检查。
- 已通过 wheel 解压到 `.deps` 的方式加载 `sqlalchemy` 与 `openpyxl`，避免 pip 系统临时目录权限问题。
- 已通过完整测试：`10 passed`。
