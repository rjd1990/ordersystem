# db_utils.py
import os
import sqlite3

# create a default path to connect to and create (if necessary) a database
# called 'database.sqlite3' in the same directory as this script


def createDB():
    DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'shopDatabase.sqlite3')
    with(sqlite3.connect(DEFAULT_PATH, timeout=10)) as con:
        return con
        # try:
        #     create_products_table(con)
        #     create_categories_table(con)
        #     create_products_bridge_table(con)
        #     create_customers_table(con)
        #     create_orders_table(con)
        #     create_table_line_items(con)
        #     con.commit()

        # except:

        #     con.rollback()
        #     raise RuntimeError("issue with db")
        
    

def create_orders_table(con):
    cur = con.cursor()
    create_orders = """CREATE TABLE orders ( id integer PRIMARY KEY AUTOINCREMENT, status text NOT NULL, dateCreated text NOT NULL, customer_id integer, 
    FOREIGN KEY (customer_id) REFERENCES customers (id))"""
    cur.execute(create_orders)


def create_table_line_items(con): 
    cur = con.cursor()
    create_li = """CREATE TABLE line_items ( id integer PRIMARY KEY AUTOINCREMENT, amount real NOT NULL, product_id integer, order_id integer,
    FOREIGN KEY (product_id) REFERENCES products (id), FOREIGN KEY (order_id) REFERENCES orders (id))"""
    cur.execute(create_li)


def create_products_table(con):
    cur = con.cursor()
    cur.execute("""CREATE TABLE products ( id integer PRIMARY KEY AUTOINCREMENT, name text NOT NULL, price real NOT NULL)""")


def create_categories_table(con):
    cur = con.cursor()
    cur.execute("CREATE TABLE categories ( id integer PRIMARY KEY AUTOINCREMENT, name text NOT NULL)")

def create_products_bridge_table(con):
    cur = con.cursor()
    create_bridge = """CREATE TABLE PRODUCTS_CATEGORIES ( product_id integer, category_id integer, FOREIGN KEY (product_id) REFERENCES products (id),
    FOREIGN KEY (category_id) REFERENCES categories (id))"""
    cur.execute(create_bridge)

def create_customers_table(con):
    cur = con.cursor()
    create_customers = """CREATE TABLE customers ( id integer PRIMARY KEY, first_name text NOT NULL, last_name text NOT NULL)"""
    cur.execute(create_customers)
    

def displayCustomers(con):
    cur = con.cursor()
    customers_sql = """SELECT * FROM CUSTOMERS"""
    cur.execute(customers_sql)
    return cur.fetchall()

def displayOrders(con):
    cur = con.cursor()
    orders_sql = """SELECT * FROM ORDERS"""
    cur.execute(orders_sql)
    return cur.fetchall()

def displayProducts(con):
    cur = con.cursor()
    products_sql = """SELECT * FROM PRODUCTS"""
    cur.execute(products_sql)
    return cur.fetchall()

def displayLineItems(con, orderID):
    cur = con.cursor()
    line_items_sql = """SELECT * FROM LINE_ITEMS WHERE ORDER_ID = ?"""
    cur.execute(line_items_sql, str(orderID))
    return cur.fetchall()

def displayProductsCategories(con):
    cur = con.cursor()
    productsCat_sql = """SELECT * FROM PRODUCTS_CATEGORIES"""
    cur.execute(productsCat_sql)
    return cur.fetchall()

def displayCategories(con):
    cur = con.cursor()
    categories_sql = """SELECT * FROM CATEGORIES"""
    cur.execute(categories_sql)
    return cur.fetchall()


if __name__ == "__main__":

    createDB()