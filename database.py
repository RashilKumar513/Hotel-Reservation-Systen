import sqlite3
import os
from datetime import datetime
import pandas as pd

DB_FILE = os.path.join(os.path.dirname(__file__), "restaurant.db")

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    # Table: Menu
    c.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            item TEXT NOT NULL UNIQUE,
            price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 50,
            active INTEGER NOT NULL DEFAULT 1
        )
    """)
    
    # Table: Bills
    c.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_no TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL,
            customer TEXT NOT NULL,
            phone TEXT,
            order_type TEXT NOT NULL,
            table_no TEXT,
            payment TEXT NOT NULL,
            subtotal REAL NOT NULL,
            discount REAL NOT NULL,
            tax REAL NOT NULL,
            total REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Completed',
            notes TEXT
        )
    """)
    
    # Table: Bill Items
    c.execute("""
        CREATE TABLE IF NOT EXISTS bill_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_no TEXT NOT NULL,
            item TEXT NOT NULL,
            category TEXT NOT NULL,
            qty INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            amount REAL NOT NULL
        )
    """)
    
    # Table: Customers
    c.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT UNIQUE,
            visits INTEGER NOT NULL DEFAULT 0,
            total_spent REAL NOT NULL DEFAULT 0,
            last_visit TEXT
        )
    """)
    
    conn.commit()
    
    # Seed default menu items if menu table is empty
    c.execute("SELECT COUNT(*) FROM menu")
    if c.fetchone()[0] == 0:
        default_menu = [
            # Starters
            ("Starters", "Samosa", 20.0, 50, 1),
            ("Starters", "Paneer Tikka", 50.0, 50, 1),
            ("Starters", "Chicken Tikka", 60.0, 50, 1),
            ("Starters", "Vegetable Pakora", 80.0, 50, 1),
            ("Starters", "Papdi Chaat", 50.0, 50, 1),
            ("Starters", "Tomato Soup", 90.0, 50, 1),
            ("Starters", "Masala Papad", 100.0, 50, 1),
            # Main Course
            ("Main Course", "Butter Chicken", 200.0, 50, 1),
            ("Main Course", "Pasta", 150.0, 50, 1),
            ("Main Course", "Basmati Rice", 100.0, 50, 1),
            ("Main Course", "Paneer Masala", 180.0, 50, 1),
            ("Main Course", "Palak Paneer", 170.0, 50, 1),
            ("Main Course", "Dal Makhani", 100.0, 50, 1),
            ("Main Course", "Chole Bhature", 220.0, 50, 1),
            # Snacks
            ("Snacks", "Noodles", 80.0, 50, 1),
            ("Snacks", "Aloo Tikki Chaat", 180.0, 50, 1),
            ("Snacks", "Dahi Vada", 130.0, 50, 1),
            ("Snacks", "Pav Bhaji", 150.0, 50, 1),
            ("Snacks", "Bhel Puri", 100.0, 50, 1),
            ("Snacks", "Spring Roll", 120.0, 50, 1),
            # Beverages
            ("Beverages", "Fresh Lime Soda", 60.0, 50, 1),
            ("Beverages", "Cold Coffee", 100.0, 50, 1),
            ("Beverages", "Mango Juice", 80.0, 50, 1),
            ("Beverages", "Masala Tea", 40.0, 50, 1),
            ("Beverages", "Mineral Water", 20.0, 50, 1),
            # Desserts
            ("Desserts", "Gulab Jamun", 80.0, 50, 1),
            ("Desserts", "Ice Cream", 100.0, 50, 1),
            ("Desserts", "Sizzling Brownie", 120.0, 50, 1),
            ("Desserts", "Fruit Salad", 90.0, 50, 1)
        ]
        c.executemany("""
            INSERT INTO menu (category, item, price, stock, active)
            VALUES (?, ?, ?, ?, ?)
        """, default_menu)
        conn.commit()

    conn.close()

# ----------------------------- MENU CRUD --------------------------

def get_all_menu(active_only=False):
    conn = get_connection()
    query = "SELECT * FROM menu"
    if active_only:
        query += " WHERE active = 1"
    query += " ORDER BY category, item"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def add_menu_item(category, item, price, stock=50, active=1):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO menu (category, item, price, stock, active)
            VALUES (?, ?, ?, ?, ?)
        """, (category, item, price, stock, active))
        conn.commit()
        success = True
        msg = f"Added '{item}' successfully!"
    except sqlite3.IntegrityError:
        success = False
        msg = f"Item '{item}' already exists in the menu."
    finally:
        conn.close()
    return success, msg

def update_menu_item(item_id, category, item, price, stock, active):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("""
            UPDATE menu
            SET category = ?, item = ?, price = ?, stock = ?, active = ?
            WHERE id = ?
        """, (category, item, price, stock, active, item_id))
        conn.commit()
        success = True
        msg = f"Updated '{item}' successfully!"
    except Exception as e:
        success = False
        msg = str(e)
    finally:
        conn.close()
    return success, msg

def delete_menu_item(item_id):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("DELETE FROM menu WHERE id = ?", (item_id,))
        conn.commit()
        success = True
        msg = "Item deleted successfully."
    except Exception as e:
        success = False
        msg = str(e)
    finally:
        conn.close()
    return success, msg

# ----------------------------- BILLING --------------------------

def save_bill(bill_no, customer, phone, order_type, table_no, payment, subtotal, discount, tax, total, notes, items):
    conn = get_connection()
    c = conn.cursor()
    now_str = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    
    try:
        # 1. Insert into bills
        c.execute("""
            INSERT INTO bills (bill_no, created_at, customer, phone, order_type, table_no, payment, subtotal, discount, tax, total, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (bill_no, now_str, customer, phone, order_type, table_no or "-", payment, subtotal, discount, tax, total, notes or "-"))
        
        # 2. Insert into bill_items & update stock
        for item in items:
            c.execute("""
                INSERT INTO bill_items (bill_no, item, category, qty, unit_price, amount)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (bill_no, item['Item'], item['Category'], item['Qty'], item['Unit Price'], item['Amount']))
            
            c.execute("""
                UPDATE menu
                SET stock = MAX(0, stock - ?)
                WHERE item = ?
            """, (item['Qty'], item['Item']))

        # 3. Update or Insert Customer record
        if phone:
            c.execute("SELECT visits, total_spent FROM customers WHERE phone = ?", (phone,))
            cust = c.fetchone()
            if cust:
                new_visits = cust['visits'] + 1
                new_spent = cust['total_spent'] + total
                c.execute("""
                    UPDATE customers
                    SET name = ?, visits = ?, total_spent = ?, last_visit = ?
                    WHERE phone = ?
                """, (customer, new_visits, new_spent, now_str, phone))
            else:
                c.execute("""
                    INSERT INTO customers (name, phone, visits, total_spent, last_visit)
                    VALUES (?, ?, 1, ?, ?)
                """, (customer, phone, total, now_str))

        conn.commit()
        return True, "Bill saved to database successfully!"
    except Exception as e:
        conn.rollback()
        return False, f"Failed to save bill: {str(e)}"
    finally:
        conn.close()

def get_bills():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM bills ORDER BY id DESC", conn)
    conn.close()
    return df

def get_bill_by_no(bill_no):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM bills WHERE bill_no = ?", (bill_no,))
    bill_row = c.fetchone()
    if not bill_row:
        conn.close()
        return None, None
    
    items_df = pd.read_sql_query("""
        SELECT category AS Category, item AS Item, qty AS Qty, unit_price AS "Unit Price", amount AS Amount
        FROM bill_items
        WHERE bill_no = ?
    """, conn, params=(bill_no,))
    conn.close()
    return dict(bill_row), items_df

def get_customers():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM customers ORDER BY total_spent DESC", conn)
    conn.close()
    return df

def find_customer_by_phone(phone):
    if not phone or len(phone.strip()) < 3:
        return None
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM customers WHERE phone LIKE ?", (f"%{phone.strip()}%",))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

# ----------------------------- ANALYTICS --------------------------

def get_analytics_summary():
    conn = get_connection()
    
    bills_df = pd.read_sql_query("SELECT * FROM bills", conn)
    items_df = pd.read_sql_query("SELECT * FROM bill_items", conn)
    
    conn.close()
    
    if bills_df.empty:
        return {
            "total_sales": 0.0,
            "total_bills": 0,
            "avg_bill": 0.0,
            "items_sold": 0,
            "payment_counts": pd.Series(dtype=int),
            "order_type_counts": pd.Series(dtype=int),
            "top_items": pd.DataFrame(),
            "bills_df": bills_df
        }

    total_sales = bills_df["total"].sum()
    total_bills = len(bills_df)
    avg_bill = bills_df["total"].mean()
    items_sold = items_df["qty"].sum() if not items_df.empty else 0
    
    payment_counts = bills_df["payment"].value_counts()
    order_type_counts = bills_df["order_type"].value_counts()
    
    if not items_df.empty:
        top_items = items_df.groupby("item")["qty"].sum().reset_index().sort_values(by="qty", ascending=False).head(5)
    else:
        top_items = pd.DataFrame(columns=["item", "qty"])

    return {
        "total_sales": total_sales,
        "total_bills": total_bills,
        "avg_bill": avg_bill,
        "items_sold": items_sold,
        "payment_counts": payment_counts,
        "order_type_counts": order_type_counts,
        "top_items": top_items,
        "bills_df": bills_df
    }
