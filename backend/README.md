# 后端 A 使用说明

## 安装依赖

```powershell
cd D:\白玉京\五洲开发\backend
python -m pip install -r requirements.txt
```

当前代码依赖 `sqlalchemy` 和 `openpyxl`。若未安装，Excel 导入、导出、数据库模型和完整测试无法运行。

如果 pip 使用系统临时目录过慢或出现 `PermissionError`，可使用本项目已验证的 wheel 解压方案：

```powershell
cd D:\白玉京\五洲开发\backend

# 先将 wheel 下载到 wheels\，再解压到 .deps\
# 已验证包版本：SQLAlchemy 2.0.36、greenlet 3.1.1、openpyxl 3.1.5、et_xmlfile 2.0.0
$env:PYTHONPATH='.deps'

# 运行代码或测试时带上 .deps
pytest tests -q -p no:cacheprovider
```

本仓库当前已在 `.deps` 中解压上述依赖，可直接通过 `PYTHONPATH=.deps` 使用。

## 初始化数据库

```powershell
python scripts\init_db.py
```

默认使用 `sqlite:///./dev.db`，可复制 `.env.example` 为 `.env` 后调整配置。
等价初始化 SQL 位于 `migrations\001_initial_schema.sql`，便于现场部署或后续迁移工具接管。

## 启动服务

```powershell
uvicorn app.main:app --reload
```

服务启动后可访问：

- `GET /health`
- `POST /api/import/upload`
- Swagger 文档：`/docs`

## 命令行导入 Excel

```powershell
python scripts\import_excel.py "D:\path\项目清单-脱敏模板.xlsx"
```

该命令会初始化数据库、读取 Excel、识别年度 Sheet、校验表头、解析金额、识别黄色无效行并写入 `projects` 表。

## 测试

```powershell
pytest tests -q -p no:cacheprovider
```

若依赖通过 `.deps` 提供：

```powershell
$env:PYTHONPATH='.deps'
$env:PYTHONDONTWRITEBYTECODE='1'
pytest tests -q -p no:cacheprovider
```

若本机尚未安装 `sqlalchemy` 和 `openpyxl`，可先运行不依赖第三方 Excel/数据库包的基础测试：

```powershell
pytest tests\test_amount_parser.py tests\test_invalid_classifier.py -q -p no:cacheprovider
```

只做语法级检查可运行：

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -c "from pathlib import Path; import ast; [ast.parse(p.read_text(encoding='utf-8'), filename=str(p)) for p in Path('.').rglob('*.py') if '.venv' not in p.parts and '.deps' not in p.parts]; print('AST syntax check passed')"
```
