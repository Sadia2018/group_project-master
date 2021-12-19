from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask_app.models import product

class User:
    db = "gangsters_paradise"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.trays = [] 

    @classmethod
    def register_user(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL("gangsters_paradise").query_db(query, data)

    @classmethod
    def get_one_user(cls, data):
        query= "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL("gangsters_paradise").query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_user_by_email(cls, data):
        query= "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL("gangsters_paradise").query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def update_user(cls, data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, password=%(password)s, WHERE id = %(id)s"
        return connectToMySQL("gangsters_paradise").query_db(query, data)

    @classmethod
    def delete_user(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s"
        return connectToMySQL("gangsters_paradise").query_db(query, data)


    @staticmethod
    def validate_register(user):
        is_valid = True
        data = { "email" : user["email"] }
        if User.get_user_by_email(data):
            flash("Email already in use", "error")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First name must be at least 3 characters", "error")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 3 characters", "error")
            is_valid = False
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email", "error")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "error")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords must match", "error")
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        if len(user['email']) < 1:
            flash("Email cannot be blank", "error")
            is_valid = False
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email", "error")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "error")
            is_valid = False
        return is_valid
        
