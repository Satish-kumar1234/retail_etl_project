# Retail Sales ETL Pipeline (Python + MySQL)

A small end-to-end data pipeline: raw sales CSV -> cleaned with Pandas -> loaded into a
MySQL star schema -> analysed with SQL (joins, CTEs, window functions).

## Pipeline
1. **Extract** - read `sales.csv` (500+ orders) with Pandas
2. **Transform** - remove duplicates, fix spacing/case, fill missing values, parse dates, compute `total_amount`
3. **Load** - insert into a star schema: `fact_sales` + `dim_customer`, `dim_product`, `dim_date`
4. **Analyse** - `queries.sql` (revenue by city, MoM growth, top products per category, running total)

## Run it
1. Install MySQL, then: `pip install -r requirements.txt`
2. `python generate_data.py`
3. Run `schema.sql` in MySQL (Workbench or `mysql -u root -p < schema.sql`)
4. Put your MySQL password in `etl.py`, then `python etl.py`
5. Run `queries.sql` and screenshot results for your portfolio / README
