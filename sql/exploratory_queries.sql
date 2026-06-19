-- 1. Total companies
SELECT COUNT(*) AS total_companies
FROM companies;

-- 2. Row count by table
SELECT COUNT(*) AS profitandloss_rows
FROM profitandloss;

-- 3. Balance sheet row count
SELECT COUNT(*) AS balancesheet_rows
FROM balancesheet;

-- 4. Cashflow row count
SELECT COUNT(*) AS cashflow_rows
FROM cashflow;

-- 5. Distinct companies in P&L
SELECT COUNT(DISTINCT company_id)
FROM profitandloss;

-- 6. Year coverage per company
SELECT company_id,
       COUNT(DISTINCT year) AS years_available
FROM profitandloss
GROUP BY company_id
ORDER BY years_available DESC;

-- 7. Companies with missing website
SELECT id, company_name
FROM companies
WHERE website IS NULL;

-- 8. Average sales by company
SELECT company_id,
       AVG(sales) AS avg_sales
FROM profitandloss
GROUP BY company_id
ORDER BY avg_sales DESC;

-- 9. Top 10 companies by net profit
SELECT company_id,
       MAX(net_profit) AS max_profit
FROM profitandloss
GROUP BY company_id
ORDER BY max_profit DESC
LIMIT 10;

-- 10. Market cap summary
SELECT company_id,
       AVG(market_cap_crore) AS avg_market_cap
FROM market_cap
GROUP BY company_id
ORDER BY avg_market_cap DESC;