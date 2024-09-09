import sqlite3
import random
import datetime
from faker import Faker

fake = Faker()

create_sales_table = '''CREATE TABLE sales (
                        sale_id INTEGER PRIMARY KEY,
                        sale_date DATE,
                        customer_id INTEGER,
                        product_id INTEGER,
                        quantity INTEGER,
                        unit_price DECIMAL(10, 2),
                        total_price DECIMAL(10, 2),
                        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                        FOREIGN KEY (product_id) REFERENCES products(product_id)
                     )'''

create_products_table = '''CREATE TABLE products (
                            product_id INTEGER PRIMARY KEY,
                            product_name TEXT,
                            unit_cost DECIMAL(10, 2)
                         )'''

create_customers_table = '''CREATE TABLE customers (
                            customer_id INTEGER PRIMARY KEY,
                            first_name TEXT,
                            last_name TEXT,
                            email TEXT,
                            phone TEXT
                         )'''

insert_products_data = '''INSERT INTO products (product_name, unit_cost) VALUES (?, ?)'''

insert_sales_data = '''INSERT INTO sales (sale_date, customer_id, product_id, quantity, unit_price, total_price) VALUES (?, ?, ?, ?, ?, ?)'''

insert_customers_data = '''INSERT INTO customers (first_name, last_name, email, phone) VALUES (?, ?, ?, ?)'''

products = [('Product A', 50.00), ('Product B', 25.00), ('Product C', 75.00), ('Product D', 40.00), ('Product E', 60.00)]

customers = []

for _ in range(1000):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    phone = fake.phone_number()
    customers.append((first_name, last_name, email, phone))

start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 12, 31)

with sqlite3.connect('sales.db') as conn:
    conn.execute(create_sales_table)

    conn.execute(create_products_table)

    conn.execute(create_customers_table)

    for product in products:
        conn.execute(insert_products_data, product)

    for customer in customers:
                conn.execute(insert_customers_data, customer)

    for i in range(1000):
        sale_date = start_date + datetime.timedelta(days=random.randint(0, 364))
        customer_id = random.randint(1, len(customers))
        product_id = random.randint(1, len(products))
        quantity = random.randint(1, 10)
        unit_price = products[product_id-1][1]
        total_price = quantity * unit_price
        conn.execute(insert_sales_data, (sale_date, customer_id, product_id, quantity, unit_price, total_price))

    conn.commit()

    print("Database successfully created!")

