"""Creates a small, slightly messy sales.csv so the ETL has something to clean."""
import random
import pandas as pd

random.seed(42)
products = {
    "Laptop": ("Electronics", 55000), "Headphones": ("Electronics", 2500),
    "Smartphone": ("Electronics", 18000), "T-Shirt": ("Clothing", 600),
    "Jeans": ("Clothing", 1500), "Sneakers": ("Footwear", 3000),
    "Notebook": ("Stationery", 80), "Pen Pack": ("Stationery", 120),
}
customers = ["Ravi Kumar", "Anita Rao", "Suresh Reddy", "Priya Sharma",
             "Kiran Patel", "Meena Iyer", "Arjun Singh", "Divya Nair"]
cities = ["Hyderabad", "Chennai", "Bengaluru", "Mumbai", "Delhi"]

rows = []
for i in range(1, 501):
    p = random.choice(list(products))
    rows.append({
        "order_id": 1000 + i,
        "order_date": f"2025-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
        "customer_name": random.choice(customers),
        "city": random.choice(cities),
        "product_name": p,
        "category": products[p][0],
        "quantity": random.randint(1, 5),
        "unit_price": products[p][1],
    })
df = pd.DataFrame(rows)

# add "dirty" data on purpose
df.loc[5, "city"] = None
df.loc[9, "quantity"] = None
df.loc[20, "customer_name"] = "  ravi kumar "
df.loc[30, "city"] = "HYDERABAD"
df = pd.concat([df, df.iloc[[2, 3, 4]]], ignore_index=True)  # duplicates
df.to_csv("sales.csv", index=False)
print("sales.csv created with", len(df), "rows")
