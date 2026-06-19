CREATE TABLE IF NOT EXISTS companies (
    id TEXT PRIMARY KEY,
    company_name TEXT,
    website TEXT,
    face_value REAL,
    book_value REAL,
    roce_percentage REAL,
    roe_percentage REAL
);

CREATE TABLE IF NOT EXISTS profitandloss (
    company_id TEXT,
    year TEXT,
    sales REAL,
    expenses REAL,
    operating_profit REAL,
    net_profit REAL,
    eps REAL,
    PRIMARY KEY (company_id, year)
);

CREATE TABLE IF NOT EXISTS balancesheet (
    company_id TEXT,
    year TEXT,
    equity_capital REAL,
    reserves REAL,
    borrowings REAL,
    total_assets REAL,
    total_liabilities REAL,
    PRIMARY KEY (company_id, year)
);

CREATE TABLE IF NOT EXISTS cashflow (
    company_id TEXT,
    year TEXT,
    operating_activity REAL,
    investing_activity REAL,
    financing_activity REAL,
    net_cash_flow REAL,
    PRIMARY KEY (company_id, year)
);

CREATE TABLE IF NOT EXISTS analysis (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    compounded_sales_growth REAL,
    compounded_profit_growth REAL,
    stock_price_cagr REAL,
    roe REAL
);

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year TEXT,
    annual_report TEXT
);

CREATE TABLE IF NOT EXISTS prosandcons (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    pros TEXT,
    cons TEXT
);

CREATE TABLE IF NOT EXISTS sectors (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    broad_sector TEXT,
    sub_sector TEXT,
    index_weight_pct REAL,
    market_cap_category TEXT
);

CREATE TABLE IF NOT EXISTS stock_prices (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    date TEXT,
    open_price REAL,
    high_price REAL,
    low_price REAL,
    close_price REAL,
    volume INTEGER,
    adjusted_close REAL
);

CREATE TABLE IF NOT EXISTS market_cap (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year INTEGER,
    market_cap_crore REAL,
    enterprise_value_crore REAL,
    pe_ratio REAL,
    pb_ratio REAL,
    ev_ebitda REAL,
    dividend_yield_pct REAL
);

CREATE TABLE IF NOT EXISTS financial_ratios (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year TEXT,
    net_profit_margin_pct REAL,
    operating_profit_margin_pct REAL,
    return_on_equity_pct REAL,
    debt_to_equity REAL,
    interest_coverage REAL,
    asset_turnover REAL,
    free_cash_flow_cr REAL,
    capex_cr REAL,
    earnings_per_share REAL,
    book_value_per_share REAL,
    dividend_payout_ratio_pct REAL,
    total_debt_cr REAL,
    cash_from_operations_cr REAL
);

CREATE TABLE IF NOT EXISTS peer_groups (
    id INTEGER PRIMARY KEY,
    peer_group_name TEXT,
    company_id TEXT,
    is_benchmark BOOLEAN
);