from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.product import Product 
from flask_bcrypt import Bcrypt
bcrypt =Bcrypt(app)

@app.route('/')
def log_and_reg():
    return render_template("log_and_reg.html")

@app.route("/users/register", methods=["POST"])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form['email'],
        "password" : pw_hash
    }
    users_id = User.register_user(data)
    session['users_id'] = users_id
    return redirect("/products")

@app.route("/users/login", methods=["POST"])
def login():
    print("Start of login function")
    if User.validate_login(request.form):
        data = { "email" : request.form["email"] }
        user_in_db = User.get_user_by_email(data)
        print(user_in_db)
        if not user_in_db:
            print("Did not find the email")
            flash("Email not found", "error")
        else:
            print("We found the email")
            if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
                flash("Invalid Email/Password" , "error")
            else:
                session['users_id'] = user_in_db.id
                return redirect("/products")
    return redirect('/')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

