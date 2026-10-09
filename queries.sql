USE retail_dw;

-- 1. Total revenue by city
SELECT c.city, SUM(f.total_amount) AS revenue
FROM fact_sales f JOIN dim_customer c ON f.customer_id = c.customer_id
GROUP BY c.city ORDER BY revenue DESC;

-- 2. Revenue by category (only categories above 100000)
SELECT p.category, SUM(f.total_amount) AS revenue
FROM fact_sales f JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.category HAVING SUM(f.total_amount) > 100000
ORDER BY revenue DESC;

-- 3. Monthly revenue and month-over-month growth % (CTE + LAG window function)
WITH monthly AS (
    SELECT d.year, d.month, SUM(f.total_amount) AS revenue
    FROM fact_sales f JOIN dim_date d ON f.date_id = d.date_id
    GROUP BY d.year, d.month
)
SELECT year, month, revenue,
       LAG(revenue) OVER (ORDER BY year, month) AS prev_month,
       ROUND((revenue - LAG(revenue) OVER (ORDER BY year, month))
             / LAG(revenue) OVER (ORDER BY year, month) * 100, 2) AS growth_pct
FROM monthly;

-- 4. Top 2 products per category (RANK window function)
SELECT * FROM (
    SELECT p.category, p.product_name, SUM(f.total_amount) AS revenue,
           RANK() OVER (PARTITION BY p.category ORDER BY SUM(f.total_amount) DESC) AS rnk
    FROM fact_sales f JOIN dim_product p ON f.product_id = p.product_id
    GROUP BY p.category, p.product_name
) t WHERE rnk <= 2;

-- 5. Running (cumulative) revenue by month
WITH monthly AS (
    SELECT d.year, d.month, SUM(f.total_amount) AS revenue
    FROM fact_sales f JOIN dim_date d ON f.date_id = d.date_id
    GROUP BY d.year, d.month
)
SELECT year, month, revenue,
       SUM(revenue) OVER (ORDER BY year, month) AS running_total
FROM monthly;

-- 6. Top 3 customers by spend
SELECT c.customer_name, SUM(f.total_amount) AS total_spent
FROM fact_sales f JOIN dim_customer c ON f.customer_id = c.customer_id
GROUP BY c.customer_name ORDER BY total_spent DESC LIMIT 3;
