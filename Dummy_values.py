from flask import Flask
import sqlite3

app = Flask(__name__)

# Create or connect to the database
connection = sqlite3.connect("Grocery_store.db")
cursor = connection.cursor()


# Insert dummy values into categories table
cursor.execute("""
    INSERT INTO categories (Category_ID, Cat_name)
    VALUES
        ('F1','Fruits'),
        ('V1','Vegetables'),
        ('D1','Dairy'),
        ('B1','Bakery')
""")
# Insert dummy values into products table
cursor.execute("""
    INSERT INTO products (Product_ID, Product_Name, Category_ID, Price, per_rate, Expiry_Date, Store_QTY, Availability)
    VALUES
        ('P001', 'Apple', 1, 300, 'Kg', '2023-12-31', 100, 1),
        ('P002', 'Carrot', 2, 200, 'Kg', '2023-12-31', 150, 1),
        ('P003', 'Milk', 3, 130, 'Litre', '2023-12-15', 50, 1),
        ('P004', 'Bread', 4, 20, 'Unit', '2023-08-31', 80, 1)
""")
# Insert dummy values into customers table
cursor.execute("""
    INSERT INTO customers (Customer_ID, Name, Username, Email, Password)
    VALUES
        ('C001', 'Upashrita Das', 'Upa', 'upa@gmail.com', '6969'),
        ('C002', 'Jane Smith', 'jane_smith', 'jane@example.com', 'hashed_password')
""")
# Insert dummy values into managers table
cursor.execute("""
    INSERT INTO managers (Manager_ID, Name, Username, Email, Password)
    VALUES
        ('M001', 'Viraj Desai', 'manager_one', 'manager1@example.com', 'managerpass1'),
        ('M002', 'Sunil Chetri', 'manager_two', 'manager2@example.com', 'hashed_password')
""")

# Commit the changes
connection.commit()

# Close the connection
connection.close()

