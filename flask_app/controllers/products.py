from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.product import Product


@app.route('/products')
def dashboard():
    if "users_id" not in session:
        return redirect("/")
    data = {
        "id": session["users_id"]
    }
    products = Product.get_all_products_with_user()
    user = User.get_one_user(data)
    return render_template("dashboard.html", user=user, products = products)


@app.route("/products/create", methods=["POST"])
def create_tray():
    if "users_id" not in session:
        return redirect('/')
    if not Product.validate_product(request.form):
        return redirect("/products/new")
    valid = Product.validate_product(request.form)
    if valid:
        data = {
            'name': request.form['name'],
            'price': request.form['price'],
            'description': request.form['description'],
            'users_id' : session['users_id']
        }
        Product.make_product(data)
    return  redirect("/products")

@app.route("/products/new")
def new_product_paige():
    if "users_id" not in session:
        return redirect('/products')
    return render_template("add_product.html")


@app.route("/products/<int:id>")
def show_new_product(id):
    if "users_id" not in session:
        return redirect('/products')
    data = {
        'id': id
    }
    products = Product.get_one_with_users(data)
    return render_template("show.html", products = products)


@app.route("/products/<int:id>/update", methods=["POST"])
def update_product(id):
    if "users_id" not in session:
        return redirect('/')
    if not Product.validate_product(request.form):
        return redirect("/products/new")
    valid = Product.validate_product(request.form)
    if valid:
        data = {
            'prod_id': id,
            'name': request.form['name'],
            'price': request.form['price'],
            'description': request.form['description'],
            'users_id' : session.get('users_id') #this is incase if session is empty. 
            }
        Product.update_product(data)
    return redirect('/products')


@app.route('/products/<int:id>/edit')
def edit_product(id):
    data = {
        'id': id
    }
    products = Product.get_one_product(data)
    return render_template('edit.html', products = products)


@app.route("/products/<int:id>/delete")
def delete_product(id):
    data={
        "id": id
    } 
    Product.delete_product(data)
    return redirect('/products')
