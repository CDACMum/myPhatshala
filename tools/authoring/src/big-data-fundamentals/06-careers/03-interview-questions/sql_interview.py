"""Five classic data engineering SQL interview questions, solved and run
on a small orders table with SQLite (built into Python, nothing to install)."""
import sqlite3

db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE orders (order_id TEXT, customer TEXT, city TEXT, amount INTEGER, order_date TEXT);
INSERT INTO orders VALUES
 ('O1','Asha','Pune',320,'2026-10-01'), ('O2','Ravi','Pune',450,'2026-10-01'),
 ('O3','Meera','Thane',610,'2026-10-02'), ('O4','Asha','Pune',150,'2026-10-02'),
 ('O5','Kiran','Thane',610,'2026-10-03'), ('O6','Ravi','Pune',900,'2026-10-03'),
 ('O7','Zoya','Nashik',200,'2026-10-03'), ('O2','Ravi','Pune',450,'2026-10-01');
""")

questions = {
    "Q1. Second highest order amount (handles ties)":
        "SELECT MAX(amount) FROM orders WHERE amount < (SELECT MAX(amount) FROM orders)",
    "Q2. Find duplicate order_ids":
        "SELECT order_id, COUNT(*) AS n FROM orders GROUP BY order_id HAVING COUNT(*) > 1",
    "Q3. Top 2 orders per city (window function, ties share a rank)":
        """SELECT city, order_id, amount, rnk FROM (
             SELECT DISTINCT order_id, city, amount,
                    DENSE_RANK() OVER (PARTITION BY city ORDER BY amount DESC) AS rnk
             FROM orders) WHERE rnk <= 2 ORDER BY city, rnk""",
    "Q4. Running total of revenue by day":
        """SELECT order_date, SUM(amount) AS day_total,
                  SUM(SUM(amount)) OVER (ORDER BY order_date) AS running_total
           FROM (SELECT DISTINCT * FROM orders) GROUP BY order_date ORDER BY order_date""",
    "Q5. Customers who ordered on 2 or more different days":
        """SELECT customer, COUNT(DISTINCT order_date) AS days FROM orders
           GROUP BY customer HAVING COUNT(DISTINCT order_date) >= 2""",
}
for title, sql in questions.items():
    print(title)
    for row in db.execute(sql):
        print("   ", row)
