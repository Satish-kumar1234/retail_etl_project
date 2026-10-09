CREATE DATABASE IF NOT EXISTS retail_dw;
USE retail_dw;

DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_customer (
    customer_id   INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    city          VARCHAR(50),
    UNIQUE (customer_name, city)
);

CREATE TABLE dim_product (
    product_id   INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) UNIQUE,
    category     VARCHAR(50)
);

CREATE TABLE dim_date (
    date_id    INT PRIMARY KEY,          -- e.g. 20250314
    full_date  DATE,
    year       INT,
    month      INT,
    month_name VARCHAR(15)
);

CREATE TABLE fact_sales (
    sale_id      INT AUTO_INCREMENT PRIMARY KEY,
    order_id     INT,
    date_id      INT,
    customer_id  INT,
    product_id   INT,
    quantity     INT,
    unit_price   DECIMAL(10,2),
    total_amount DECIMAL(12,2),
    FOREIGN KEY (date_id)     REFERENCES dim_date(date_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (product_id)  REFERENCES dim_product(product_id)
);

CREATE INDEX idx_fact_date ON fact_sales(date_id);


