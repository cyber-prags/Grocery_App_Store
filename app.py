from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Set a secret key for session management
app.secret_key = "123"  # Replace with a more secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Grocery_store.db'
db = SQLAlchemy(app)

class Customers(db.Model):
    Customer_ID = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    Name = db.Column(db.String)
    Username = db.Column(db.String)
    Email = db.Column(db.String)
    Password = db.Column(db.String)


class Managers(db.Model):
    Manager_ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    Username = db.Column(db.String)
    Email = db.Column(db.String)
    Password = db.Column(db.String)

class Categories(db.Model):
    Category_ID = db.Column(db.Integer, primary_key=True)
    Cat_name = db.Column(db.String)
    

class Products(db.Model):
    Product_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Product_Name = db.Column(db.String)
    Price = db.Column(db.Float)
    per_rate = db.Column(db.String)
    Expiry_Date = db.Column(db.String)
    Store_QTY = db.Column(db.Float)
    Availability = db.Column(db.Boolean)
    Category_ID = db.Column(db.Integer, db.ForeignKey('categories.Category_ID'))

class Purchases(db.Model):
    Purchase_ID = db.Column(db.Integer, primary_key=True)
    Category_ID = db.Column(db.ForeignKey('categories.Category_ID'))
    Product_ID = db.Column(db.ForeignKey('products.Product_ID'))
    Qty = db.Column(db.Integer)
    Tot_Price = db.Column(db.Integer)

# Function to establish a database connection and cursor
def get_db_cursor():
    connection = sqlite3.connect('Grocery_store.db')
    cursor = connection.cursor()
    return connection, cursor

# Function to check manager credentials
def valid_credentials(username, password):
    print(username, password)
    manager = Managers.query.filter_by(Username=username).first()

    print(manager)

    if manager is None:
        return False
    
    return True

# Landing page
@app.route('/')
def index():
    return render_template('index.html')

# Manager login route
@app.route('/manager_login', methods=['GET', 'POST'])
def manager_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        manager = Managers.query.filter_by(Username=username, Password=password).first()

        if manager is None:
            return "Login failed"
        
        session['username'] = username
        return redirect(url_for('manager_dashboard'))

    return render_template('manager_login.html')


# Manager dashboard route
@app.route('/manager_dashboard')
def manager_dashboard():
    # Check if the manager is logged in
    if 'username' in session:
        categories = Categories.query.all()
        products = Products.query.all()

        return render_template('manager_dashboard.html', categories=categories, products=products)
    else:
        return redirect(url_for('manager_login'))  # Redirect to manager login if not logged in
    
# Adding the 'add_category' route
@app.route('/add_category', methods=['POST'])
def add_category():
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        category_id = request.form.get('category_id')

        # Insert the new category into the database
        category = Categories(Category_ID=category_id, Cat_name=category_name)
        db.session.add(category)
        db.session.commit()

    return redirect(url_for('manager_dashboard'))

@app.route('/admin-category-products/<string:category_id>', methods=['GET', 'POST'])
def admin_category_products(category_id):
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        price = request.form.get('price')
        per_rate = request.form.get('per_rate')
        expiry_date = request.form.get('expiry_date')
        store_qty = request.form.get('store_qty')
        availability = request.form.get('availability')

        if availability == 'true':
            availability = True
        
        else:
            availability = False

        product = Products(Product_Name=product_name, Price=price, per_rate=per_rate, Expiry_Date=expiry_date, Store_QTY=store_qty, Availability=availability, Category_ID=category_id)
        db.session.add(product)
        db.session.commit()

        return redirect(url_for('admin_category_products', category_id=category_id))

    category = Categories.query.filter_by(Category_ID=category_id).first()
    products = Products.query.filter_by(Category_ID=category_id).all()
    return render_template('admin_category_products.html', products=products, category_id=category_id, category=category)

# edit category route
@app.route('/edit-category/<string:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    if request.method == 'POST':
        category_name = request.form.get('category_name')

        category = Categories.query.filter_by(Category_ID=category_id).first()
        category.Cat_name = category_name
        db.session.commit()

        return redirect(url_for('manager_dashboard'))

    category = Categories.query.filter_by(Category_ID=category_id).first()
    return render_template('edit-category.html', category=category, category_id=category_id)

@app.route('/delete-category/<string:category_id>', methods=['GET', 'POST'])
def delete_category(category_id):
    category = Categories.query.filter_by(Category_ID=category_id).first()
    db.session.delete(category)
    db.session.commit()

    return redirect(url_for('manager_dashboard'))

@app.route('/edit-product/<string:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if request.method == "POST":
        product_name = request.form.get('product_name')
        price = request.form.get('price')
        per_rate = request.form.get('per_rate')
        expiry_date = request.form.get('expiry_date')
        store_qty = request.form.get('store_qty')
        availability = request.form.get('availability')

        if availability == 'true':
            availability = True
        
        else:
            availability = False

        product = Products.query.filter_by(Product_ID=product_id).first()
        product.Product_Name = product_name
        product.Price = price
        product.per_rate = per_rate
        product.Expiry_Date = expiry_date
        product.Store_QTY = store_qty
        product.Availability = availability

        db.session.commit()

        return redirect(url_for('admin_category_products', category_id=product.Category_ID))
    
    product = Products.query.filter_by(Product_ID=product_id).first()

    return render_template('edit-product.html', product_id=product_id, product=product)

@app.route('/delete-product/<string:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    product = Products.query.filter_by(Product_ID=product_id).first()
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('admin_category_products', category_id=product.Category_ID))

#Route for plotting graphs   
@app.route('/analytics')
def analytics():
    # Query the database for product name and total quantity sold
    products_sold = db.session.query(Products.Product_Name, db.func.sum(Purchases.Qty))\
                              .join(Purchases, Products.Product_ID == Purchases.Product_ID)\
                              .group_by(Products.Product_Name)\
                              .order_by(db.func.sum(Purchases.Qty).desc())\
                              .all()

    if products_sold:
        # Unzip the data for plotting
        product_names, quantities = zip(*products_sold)

        # Create a bar plot for most sold products
        plt.figure(figsize=(10, 6))
        plt.bar(product_names, quantities)
        plt.xlabel('Product Name')
        plt.ylabel('Quantity Sold')
        plt.title('Most Sold Products')
        plt.xticks(rotation=45, ha="right")

    # Save the plot to a BytesIO object
    img_stream_most_sold = BytesIO()
    plt.savefig(img_stream_most_sold, format='png')
    img_stream_most_sold.seek(0)
    img_data_most_sold = base64.b64encode(img_stream_most_sold.read()).decode()

    # Query the database for category name and total quantity sold
    categories_sold = db.session.query(Categories.Cat_name, db.func.sum(Purchases.Qty)).join(Products, Categories.Category_ID == Products.Category_ID).join(Purchases, Products.Product_ID == Purchases.Product_ID).group_by(Categories.Cat_name).all()

    # Unzip the data for plotting
    category_names, quantities = zip(*categories_sold)

    # Create a bar plot for best-performing categories
    plt.figure(figsize=(10, 6))
    plt.bar(category_names, quantities)
    plt.xlabel('Category Name')
    plt.ylabel('Quantity Sold')
    plt.title('Best-Performing Categories')
    plt.xticks(rotation=45, ha="right")

    # Save the plot to a BytesIO object
    img_stream_best_categories = BytesIO()
    plt.savefig(img_stream_best_categories, format='png')
    img_stream_best_categories.seek(0)
    img_data_best_categories = base64.b64encode(img_stream_best_categories.read()).decode()

    return render_template('analytics.html', plot_data_most_sold=img_data_most_sold, plot_data_best_categories=img_data_best_categories)


#CUSTOMER SIDE routes

#route for user login
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Implement your user authentication logic here
        # For example:        
        user = Customers.query.filter_by(Username=username, Password=password).first()

        if user is None:
            return "Login failed"
        
        return redirect(url_for('user_dashboard'))
    
    return render_template('user_login.html')

@app.route('/user_signup', methods=['GET','POST'])
def user_signup():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = Customers(Name=name, Username=username, Email=email, Password=password)
        db.session.add(user)
        db.session.commit()
        
        # Render the success template after successful signup
        return render_template('user_signup_success.html')

    return render_template('user_signup.html')


@app.route('/category/<string:category_id>')
def category_products(category_id):
    category_id = str(category_id)
    category = Categories.query.filter_by(Category_ID=category_id).first()

    products = Products.query.filter_by(Category_ID=category.Category_ID).all()

    return render_template('category_products.html', category=category, products=products)


@app.route('/user_dashboard', methods=['GET', 'POST'])
def user_dashboard():
    if request.method == 'POST':
        selected_category_id = request.form.get('selected_category')
        selected_product_id = request.form.get('selected_product')
        
        # Placeholder logic to retrieve selected category and product names
        selected_category_name = "Selected Category"
        selected_product_name = "Selected Product"

        # Placeholder logic to process the selected data (print to console)
        print("Selected Category:", selected_category_name)
        print("Selected Product:", selected_product_name)

    # Fetch categories from the database
    categories = Categories.query.all()

    # Fetch products from the database
    products = Products.query.all()

    # Fetch user information from the session
    user_info = session.get('user_info')

    return render_template('grocery_store_dashboard.html', categories=categories, products=products, user_info=user_info)

# Profile page route
@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    if 'username' not in session:
        return redirect(url_for('index'))

    username = session['username']
    user = Customers.query.filter_by(Username=username).first()
    if user is None:
        user = Managers.query.filter_by(Username=username).first()

    if request.method == 'POST':
        # Handling profile editing
        new_name = request.form['name']
        new_username = request.form['username']
        new_email = request.form['email']
        new_password = request.form['password']

        # Updating the user information
        user.Name = new_name
        user.Username = new_username
        user.Email = new_email
        user.Password = new_password
        db.session.commit()

        # Redirecting back to the profile page with updated information
        return redirect(url_for('user_profile'))

    return render_template('profile.html', name=user.Name, username=user.Username, email=user.Email, password=user.Password)

# Route to select the quantity before purchasing
@app.route('/purchase_quantity/<string:category_id>/<string:product_id>')
def purchase_quantity(category_id, product_id):
    # Query the product details from the database
    product = Products.query.filter_by(Product_ID=product_id).first()
    print(product)

    # Render the purchase_quantity.html template with the product details
    return render_template('purchase_quantity.html', product=product, category_id=category_id)

# Define a dictionary to hold the cart items in the user's session
@app.before_request
def initialize_cart():
    if 'cart' not in session:
        session['cart'] = {}

# Route to add a product to the cart
@app.route('/add_to_cart/<string:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # Get the selected quantity from the form
    quantity = int(request.form.get('quantity', 1))
    
    # Query the product details from the database
    product = Products.query.filter_by(Product_ID=product_id).first()

    # Add the product and quantity to the cart
    if product:
        cart_item = {
            'id': product.Product_ID,
            'name': product.Product_Name,
            'price': product.Price,
            'store_qty': product.Store_QTY,
            'qty': quantity,
            'category_id': product.Category_ID
        }
        session['cart'][product_id] = cart_item
        session.modified = True

    # Redirect to the cart page
    return redirect(url_for('view_cart'))

# Route to view the cart
@app.route('/view_cart')
def view_cart():
    cart = session.get('cart', {})
    total_price = sum(item['price'] * item['qty'] for item in cart.values())
    return render_template('cart.html', cart=cart.values(), total_price=total_price)

@app.route('/update_cart/<string:product_id>', methods=['POST'])
def update_cart(product_id):
    quantity = int(request.form.get('quantity', 1))

    cart = session.get('cart', {})
    if quantity > 0:
        cart[product_id]['qty'] = quantity
        session['cart'] = cart
    else:
        del cart[product_id]
        session['cart'] = cart

    return redirect(url_for('view_cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():

    for item in session['cart'].values():
        purchase = Purchases(Category_ID=item['category_id'],Product_ID=item['id'], Qty=item['qty'], Tot_Price=item['price'])
        db.session.add(purchase)

        # decrease store qty
        product = Products.query.filter_by(Product_ID=item['id']).first()
        product.Store_QTY = product.Store_QTY - item['qty']

        db.session.commit()



    session['cart'] = {}
    return render_template('checkout.html')



@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('query')  # Getting the search term from the query parameters
    if search_term:
        # Querying products by name and including the category information
        products = db.session.query(Products, Categories.Cat_name)\
            .join(Categories, Products.Category_ID == Categories.Category_ID)\
            .filter(Products.Product_Name.like(f"%{search_term}%")).all()
        # Querying categories by name
        categories = db.session.query(Categories).filter(Categories.Cat_name.like(f"%{search_term}%")).all()
    else:
        products = []
        categories = []

    return render_template('search_results.html', products=products, categories=categories, query=search_term)





@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('index'))  # Redirect to the landing page or any other page

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
