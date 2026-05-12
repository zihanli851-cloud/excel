CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'viewer',
    display_name VARCHAR(50),
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seq_no INTEGER,
    project_name TEXT NOT NULL,
    project_code VARCHAR(50),
    purchaser TEXT,
    bid_open_date DATE,
    commission_amount TEXT,
    commission_num NUMERIC(18, 4),
    max_price TEXT,
    max_price_num NUMERIC(18, 4),
    bid_amount TEXT,
    bid_amount_num NUMERIC(18, 4),
    bid_amount_detail TEXT,
    sheet_year SMALLINT NOT NULL,
    is_invalid BOOLEAN NOT NULL DEFAULT 0,
    invalid_reason VARCHAR(50),
    source_file VARCHAR(255),
    source_sheet VARCHAR(100),
    source_row INTEGER,
    row_hash VARCHAR(64) NOT NULL UNIQUE,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    CONSTRAINT uq_projects_code_year UNIQUE (project_code, sheet_year)
);

CREATE INDEX IF NOT EXISTS ix_projects_project_code ON projects (project_code);
CREATE INDEX IF NOT EXISTS ix_projects_purchaser ON projects (purchaser);
CREATE INDEX IF NOT EXISTS ix_projects_bid_open_date ON projects (bid_open_date);
CREATE INDEX IF NOT EXISTS ix_projects_sheet_year ON projects (sheet_year);
CREATE INDEX IF NOT EXISTS ix_projects_is_invalid ON projects (is_invalid);
CREATE INDEX IF NOT EXISTS ix_projects_invalid_reason ON projects (invalid_reason);
CREATE INDEX IF NOT EXISTS ix_projects_row_hash ON projects (row_hash);

CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action VARCHAR(50) NOT NULL,
    detail JSON,
    ip_address VARCHAR(45),
    created_at DATETIME NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS query_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    query_params JSON NOT NULL,
    result_count INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users (id)
);
