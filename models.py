from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Grocery_store.db'
db = SQLAlchemy(app)

class Customers(db.Model):
    Customer_ID = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    Name = db.Column(db.String)
    Username = db.Column(db.String)
    Email = db.Column(db.String)
    Password = db.Column(db.String)

class Managers(db.Model):
    Manager_ID = db.Column(db.String, primary_key=True)
    Name = db.Column(db.String)
    Username = db.Column(db.String)
    Email = db.Column(db.String)
    Password = db.Column(db.String)

class Categories(db.Model):
    Category_ID = db.Column(db.String, primary_key=True)
    Cat_name = db.Column(db.String)

class Products(db.Model):
    Product_ID = db.Column(db.String, primary_key=True)
    Product_Name = db.Column(db.String)
    Price = db.Column(db.Float)
    per_rate = db.Column(db.String)
    Expiry_Date = db.Column(db.Date)
    Store_QTY = db.Column(db.Float)
    Availability = db.Column(db.Boolean)
    Category_ID = db.Column(db.ForeignKey('categories.Category_ID'))

class Purchases(db.Model):
    Purchase_ID = db.Column(db.Integer, primary_key=True)
    Category_ID = db.Column(db.ForeignKey('categories.Category_ID'))
    Product_ID = db.Column(db.ForeignKey('products.Product_ID'))
    Qty = db.Column(db.Integer)
    Tot_Price = db.Column(db.Integer)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
