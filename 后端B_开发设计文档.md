# 项目清单筛选查询插件 - 后端 B 开发设计文档

版本：V1.0  
日期：2026-05-12  
范围：后端 B  
参考文档：

- 《需求文档_项目清单筛选查询插件_V2.docx》
- 《开发文档_项目清单筛选查询插件_V2.docx》
- [后端A_开发设计文档.md](/d:/Afile/excel/后端A_开发设计文档.md)

## 实施进度

- [x] ~~新增通用 schema，包括登录、查询、分页、审计、查询历史响应结构~~
- [x] ~~完成 `AuthService`、`ProjectQueryService`、`AuditService`、`QueryHistoryService`~~
- [x] ~~完成登录接口、当前用户鉴权依赖与默认管理员引导~~
- [x] ~~完成项目查询接口、按 `project_ids` 导出和按查询条件导出主链路~~
- [x] ~~完成查询历史列表/新增/删除、审计日志列表、项目复核接口~~
- [x] ~~完成 SQLite 伪数据测试与真实接口冒烟验证~~
- [ ] 待后端 A 修复 `bid_open_date` 后补做日期筛选最终验收
- [ ] 如业务确认需要，再将复核状态持久化到独立表

## 0. 当前因后端 A 未完成而暂时不能开始或不能收口的内容

截至 2026-05-12，已使用真实脱敏 Excel `可提供项目清单-脱敏模板(1).xlsx` 成功导入 SQLite，实际落库文件为 [backend/dev.db](/d:/Afile/excel/backend/dev.db)。

本次真实导入结果：

- 总行数 `423`
- 成功入库 `423`
- 有效数据 `336`
- 无效数据 `87`
- warning `17`

这意味着后端 B 已经不再受“没有真实库数据”的阻塞，查询 API、前后端联调、按查询条件导出这些工作现在都可以开始。  
但后端 A 仍存在一个会影响后端 B 收口的重要问题：

1. 不能收口日期筛选相关功能的最终验收。
   本次导入后发现 `bid_open_date` 字段质量明显异常，库内有 `413` 条记录落在 `1969-12` 到 `1970-01`，而不是业务预期年份。这会直接影响后端 B 的 `date_from` / `date_to` 筛选、排序和前端展示。

2. 不能收口依赖日期字段正确性的统计与导出验收。
   只要开标时间未修正，按日期范围查询出的结果集就不可信，进一步影响“按查询条件导出”和任何带日期条件的业务验收。

3. 不能收口复杂筛选边界 case 的全量业务正确性。
   金额、无效状态、采购人这些维度现在可以开始真实联调；但一旦叠加日期条件，结果仍需要等待后端 A 修正日期问题后再做最终验收。

上面这些内容是“暂时不能最终收口”，不是“后端 B 不能开始”。后端 B 现在已经可以基于真实库推进绝大部分开发，只需要把“日期条件相关能力”标记为待后端 A 修正后再验收。

## 1. 当前协作状态

### 1.1 后端 A 已提供内容

- SQLite 默认配置和 SQLAlchemy 连接入口。
- `projects`、`users`、`audit_logs`、`query_history` 四张表的模型和初始化 SQL。
- Excel 导入接口：`POST /api/import/upload`。
- 项目详情接口：`GET /api/projects/{project_id}`。
- 导出能力占位：`POST /api/projects/export`，当前按 `project_ids` 导出。
- 元数据接口：
  - `GET /api/purchasers`
  - `GET /api/stats/invalid`
- Repository 基础方法：
  - `get_by_id()`
  - `list_by_ids()`
  - `list_purchasers()`
  - `count_invalid_by_reason()`
  - `search_base_query()`
- 真实脱敏数据已完成一次导入，当前库内状态：
  - `projects` 共 `423` 条
  - `is_invalid = true` 共 `87` 条
  - 涉及年度 `2023`
  - 不重复采购人 `115` 个

### 1.1.1 当前已知问题

- `bid_open_date` 导入结果明显异常，当前 `2023` 年内记录数为 `0`，空日期 `10` 条，异常落在 `1969-12` 到 `1970-01` 的记录 `413` 条。
- 因此后端 B 可以先做除日期验收以外的大多数功能，但日期筛选不能直接作为正确结果对外承诺。

### 1.2 后端 B 当前剩余待完善内容

- 等后端 A 修正日期字段后，补做日期筛选、日期排序、按日期导出的最终验收。
- 视业务需要决定是否新增独立的 `project_reviews` 持久化表。
- 若后续上线要求更严格，可把当前轻量 token 方案替换为正式 JWT。

## 2. 后端 B 定位

后端 B 负责把后端 A 提供的数据底座包装成业务可用的 API 能力，目标是在不重做 Excel 导入逻辑的前提下，完成：

```text
查询条件输入 -> 查询参数校验 -> 拼接数据库条件 -> 返回分页结果 -> 记录查询历史 -> 记录审计日志 -> 支持导出与复核
```

后端 B 本阶段主责是“查询和业务接口层”，不是“数据清洗和导入层”。

## 3. 分工边界

| 角色 | 主责 | 说明 |
|---|---|---|
| 后端 A | 数据底座 | 项目表模型、Excel 导入、无效识别、金额解析、导出底层能力 |
| 后端 B | 业务 API | 查询、认证、审计、查询历史、复核、导出主流程 |
| 前端 | 页面和交互 | 登录页、查询页、表格、筛选、导出入口、审计页 |

后端 B 的实现原则：

- 不重复实现 Excel 解析和导入逻辑。
- 尽量复用后端 A 已有模型和 repository。
- 当 A 提供的方法不够用时，在 B 层新增 service/repository 扩展，不直接改动导入核心逻辑。

## 4. 本阶段目标

### 4.1 周一到周二目标

1. [x] ~~完成后端 B 真实路由骨架，替换现有 `501` 占位接口。~~
2. [x] ~~完成查询参数 schema、分页结构、统一响应结构。~~
3. [x] ~~完成项目查询 API 的第一版，可直接对 `projects` 表查询。~~
4. [x] ~~完成查询历史写入和删除。~~
5. [x] ~~完成审计日志写入机制。~~
6. [x] ~~完成登录接口最小闭环，可先使用本地用户表。~~
7. [x] ~~完成前端联调用 mock 到真实 API 的切换准备。~~

### 4.2 周三后的承接目标

1. 基于已导入的 SQLite 数据继续联调查询主链路。
2. 验证关键筛选结果正确性。
3. 跑通“筛选结果导出”主链路。
4. 在后端 A 修正日期问题后，补做日期区间相关验收。

## 5. 推荐目录结构

```text
backend/
  app/
    api/
      routes/
        auth_routes.py
        project_routes.py
        audit_routes.py
        query_history_routes.py
    schemas/
      auth.py
      common.py
      project_query.py
      audit.py
      query_history.py
    services/
      auth_service.py
      project_query_service.py
      audit_service.py
      query_history_service.py
    repositories/
      auth_repository.py          # 如需要单独拆分
      audit_repository.py         # 如需要单独拆分
      query_history_repository.py # 如需要单独拆分
```

如果当前仓库不想新增 `repositories/` 目录，也可以先继续沿用 `services + models + project_repository` 的方式，在已有结构上增量实现。

## 6. API 设计

### 6.1 登录认证

```http
POST /api/auth/login
Content-Type: application/json
```

请求体建议：

```json
{
  "username": "admin",
  "password": "******"
}
```

响应体建议：

```json
{
  "success": true,
  "data": {
    "access_token": "token-or-jwt",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "username": "admin",
      "display_name": "管理员",
      "role": "admin"
    }
  }
}
```

本阶段可先做简化版：

- 先用 `users` 表完成账号校验。
- token 可先做轻量实现，后续再换正式 JWT。
- 密码必须存 `password_hash`，不能明文。

### 6.2 项目查询

建议新增主查询接口：

```http
POST /api/projects/search
Content-Type: application/json
Authorization: Bearer <token>
```

请求体建议：

```json
{
  "keyword": "医院",
  "code": "P2026",
  "purchaser": "某采购人",
  "date_from": "2026-01-01",
  "date_to": "2026-12-31",
  "amount_min": 100,
  "amount_max": 500,
  "amount_field": "any",
  "invalid_mode": "all",
  "invalid_reason": null,
  "page": 1,
  "page_size": 20,
  "sort_by": "bid_open_date",
  "sort_order": "desc"
}
```

响应体建议：

```json
{
  "success": true,
  "data": {
    "items": [],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 0
    }
  }
}
```

### 6.3 查询结果导出

建议新增：

```http
POST /api/projects/export-by-query
```

处理方式：

1. 复用查询参数。
2. 在后端 B 内部先查出完整结果集。
3. 转成 `project_ids` 或 `Project` 列表。
4. 调用后端 A 已提供的导出服务。
5. 记录审计日志。

### 6.4 查询历史

建议接口：

```http
GET /api/query-history
POST /api/query-history
DELETE /api/query-history/{history_id}
```

用途：

- 保存最近查询条件。
- 支持前端一键复用历史筛选。
- 可限制每个用户只保留最近 N 条。

### 6.5 审计日志

建议接口：

```http
GET /api/audit/logs
```

最少记录的动作：

- 登录
- 导入
- 查询
- 导出
- 复核
- 删除查询历史

### 6.6 复核接口

建议接口：

```http
POST /api/projects/{project_id}/review
```

如果本期没有单独复核表，可先做最小版本：

- 只写审计日志。
- 记录谁复核了哪个项目、备注是什么。

如果业务明确要求保留复核状态，再追加 `project_reviews` 表。

## 7. 查询参数与筛选语义

### 7.1 查询参数

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

### 7.2 SQL 语义

无效模式：

| invalid_mode | 语义 |
|---|---|
| valid_only | `is_invalid = false` |
| all | 不加无效过滤 |
| invalid_only | `is_invalid = true` |

金额模式：

| amount_field | 语义 |
|---|---|
| commission | 用 `commission_num` 筛选 |
| max_price | 用 `max_price_num` 筛选 |
| bid_amount | 用 `bid_amount_num` 筛选 |
| any | 三个金额字段任一满足即可 |

排序建议白名单：

- `bid_open_date`
- `sheet_year`
- `project_code`
- `purchaser`
- `created_at`

不要直接接收前端任意字段名拼 SQL。

## 8. 数据模型设计

### 8.1 直接复用模型

后端 B 当前优先复用后端 A 已提供的三张业务相关表：

- `users`
- `audit_logs`
- `query_history`

### 8.2 现有字段已足够支撑的能力

| 表 | 当前可直接支撑能力 |
|---|---|
| users | 登录、角色、启停状态 |
| audit_logs | 操作留痕 |
| query_history | 保存查询条件与结果数量 |
| projects | 查询、统计、导出、复核目标对象 |

### 8.3 如需扩展的表

若复核需要持久状态而不是只记日志，可新增：

```text
project_reviews
```

建议字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| id | Integer | PK |
| project_id | FK | 关联项目 |
| reviewer_id | FK | 复核人 |
| review_status | String(20) | 通过/驳回/待确认 |
| review_comment | Text | 备注 |
| created_at | DateTime | 创建时间 |

本表不是周一到周二的必做项，先确认业务是否真的需要。

## 9. 服务设计

### 9.1 AuthService

负责：

- 用户查找
- 密码校验
- token 生成
- 登录日志记录

### 9.2 ProjectQueryService

负责：

- 参数校验后的查询条件拼装
- 分页
- 排序
- 查询结果封装
- 查询历史记录
- 查询审计记录

建议方法：

```python
def search_projects(payload: ProjectSearchRequest, user_id: int | None) -> ProjectSearchResponse:
    ...
```

### 9.3 AuditService

负责：

- 写入审计日志
- 查询审计日志列表

### 9.4 QueryHistoryService

负责：

- 保存查询条件
- 查询最近历史
- 删除历史

## 10. 与后端 A 的对接方式

### 10.1 可以直接复用的能力

- `ProjectRepository.search_base_query()`
- `ProjectRepository.get_by_id()`
- `ProjectRepository.list_by_ids()`
- `ProjectRepository.list_purchasers()`
- `ProjectRepository.count_invalid_by_reason()`
- `export_projects()`

### 10.2 后端 B 已补齐的能力

- `search_projects()` 组合筛选逻辑。
- 分页 total 统计。
- 导出前的查询结果集获取。
- 鉴权依赖。
- 查询/导出/复核的审计落库。

### 10.3 协作约定

1. 后端 B 不改 `projects` 字段含义。
2. 如果发现筛选语义与前端需求不一致，先改 B 层 query service，不回头破坏 A 的导入结构。
3. 若需要追加索引或扩展字段，应先同步 A，再更新初始化 SQL。

## 11. 周一到周二实施顺序

1. [x] ~~新增通用 schema：登录请求/响应、查询请求/响应、分页结构、通用成功/失败响应。~~
2. [x] ~~完成 `auth_routes.py`：登录接口、当前用户接口、鉴权依赖。~~
3. [x] ~~完成 `project_routes.py`：`POST /projects/search`、`POST /projects/export-by-query`，并保留已有 `GET /projects/{id}` 与按 id 导出。~~
4. [x] ~~完成 `query_history_routes.py`：列表、新增、删除。~~
5. [x] ~~完成 `audit_routes.py`：审计日志列表。~~
6. [x] ~~补齐 service：`AuthService`、`ProjectQueryService`、`AuditService`、`QueryHistoryService`。~~
7. [x] ~~用 SQLite 空库和伪数据做接口级测试，并完成真实接口冒烟验证。~~

## 12. 测试计划

### 12.1 单元测试

| 测试对象 | 覆盖点 |
|---|---|
| auth_service | 用户不存在、密码错误、禁用用户、登录成功 |
| project_query_service | 关键字、编号、采购人、日期、金额、无效模式、分页、排序 |
| audit_service | 查询/导出/登录日志写入 |
| query_history_service | 保存、列表、删除、条数限制 |

### 12.2 集成测试

建议至少覆盖：

1. 登录成功与失败。
2. 查询接口在空库下的正确响应。
3. 查询接口在样例数据下的分页与筛选。
4. 导出接口能调起后端 A 导出服务。
5. 查询后自动生成查询历史和审计日志。

### 12.3 联调验收

后端 A 完成真实 Excel 导入后，再补以下验收：

1. 金额范围筛选结果是否符合业务预期。
2. 无效数据切换是否正确。
3. 采购人筛选项是否与库中真实值一致。
4. 导出结果是否与查询结果一致。

## 13. 风险与处理

| 风险 | 表现 | 处理方式 |
|---|---|---|
| 后端 A 日期字段导入异常 | 日期筛选、排序、导出结果不可信 | 后端 B 先完成非日期主链路，日期验收待 A 修正后补做 |
| 查询条件语义反复变化 | 前后端联调口径不一致 | 先固定 request schema，再集中调整 service 逻辑 |
| 后端 A repository 能力不够 | B 层查询难写 | 在 B 层新增 query service，不回退重写 A 的导入模块 |
| 审计要求临时细化 | 字段不够 | 先保证 action + detail + user_id，细节后补 |
| 认证方案未最终确定 | 登录实现反复改 | 本期先做最小闭环，后续再替换正式 JWT |

## 14. 本阶段交付物

后端 B 本阶段应交付：

- 可调用的登录接口。
- 可查询的项目搜索接口。
- 可保存/删除的查询历史接口。
- 可查看的审计日志接口。
- 可按查询条件导出的主流程接口。
- 对前端稳定的请求/响应结构。
- 一组基础测试。

## 15. 当前结论

后端 B 现在不是“不能做”，而是“已经可以基于真实库开始开发和联调，但不能收口日期相关验收”。最合适的策略是：

1. 立刻基于 [backend/dev.db](/d:/Afile/excel/backend/dev.db) 开始 B 的 API、service、schema 开发和联调。
2. 先完成不依赖日期正确性的查询、审计、历史、导出主链路。
3. 等后端 A 修正日期字段后，再补做日期筛选和最终验收。
