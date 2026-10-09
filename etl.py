"""Simple ETL: sales.csv -> clean with Pandas -> load into MySQL star schema."""
import pandas as pd
import mysql.connector

DB = dict(host="localhost", user="root", password="enter", database="retail_dw")


# ---------- EXTRACT ----------
def extract(path="sales.csv"):
    df = pd.read_csv(path)
    print(f"Extracted {len(df)} rows")
    return df


# ---------- TRANSFORM ----------
def transform(df):
    df = df.drop_duplicates()                                   # remove duplicate rows
    df["customer_name"] = df["customer_name"].str.strip().str.title()   # fix spaces/case
    df["city"] = df["city"].str.strip().str.title()
    df["city"] = df["city"].fillna("Unknown")                   # missing city
    df["quantity"] = df["quantity"].fillna(1).astype(int)       # missing quantity -> 1
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["total_amount"] = df["quantity"] * df["unit_price"]      # derived column
    print(f"After cleaning: {len(df)} rows")
    return df


# ---------- LOAD ----------
def load(df):
    conn = mysql.connector.connect(**DB)
    cur = conn.cursor()

    # dimensions
    for _, r in df[["customer_name", "city"]].drop_duplicates().iterrows():
        cur.execute("INSERT IGNORE INTO dim_customer (customer_name, city) VALUES (%s, %s)",
                    (r.customer_name, r.city))
    for _, r in df[["product_name", "category"]].drop_duplicates().iterrows():
        cur.execute("INSERT IGNORE INTO dim_product (product_name, category) VALUES (%s, %s)",
                    (r.product_name, r.category))
    for d in df["order_date"].drop_duplicates():
        cur.execute("INSERT IGNORE INTO dim_date VALUES (%s, %s, %s, %s, %s)",
                    (int(d.strftime("%Y%m%d")), d.date(), d.year, d.month, d.strftime("%B")))
    conn.commit()

    # look-ups: natural key -> surrogate key
    cur.execute("SELECT customer_id, customer_name, city FROM dim_customer")
    cust = {(n, c): i for i, n, c in cur.fetchall()}
    cur.execute("SELECT product_id, product_name FROM dim_product")
    prod = {n: i for i, n in cur.fetchall()}

    # fact table
    rows = [(int(r.order_id), int(r.order_date.strftime("%Y%m%d")),
             cust[(r.customer_name, r.city)], prod[r.product_name],
             int(r.quantity), float(r.unit_price), float(r.total_amount))
            for r in df.itertuples()]
    cur.executemany("""INSERT INTO fact_sales
        (order_id, date_id, customer_id, product_id, quantity, unit_price, total_amount)
        VALUES (%s,%s,%s,%s,%s,%s,%s)""", rows)
    conn.commit()
    print(f"Loaded {len(rows)} rows into fact_sales")
    cur.close(); conn.close()


if __name__ == "__main__":
    load(transform(extract()))
