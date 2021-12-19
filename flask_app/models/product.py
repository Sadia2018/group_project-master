from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Product:
    db = "gangsters_paradise"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.price = data['price']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None 


    @classmethod
    def make_product(cls, form_data):
        query = "INSERT INTO products(name, price, description, users_id) VALUES (%(name)s, %(price)s, %(description)s,%(users_id)s)"
        return connectToMySQL("gangsters_paradise").query_db(query, form_data)

    @classmethod
    def get_all_products(cls):
        query= "SELECT * FROM products"
        results = connectToMySQL("gangsters_paradise").query_db(query)
        products = []
        for row in results:
            products.append(cls(row))
        return products

    @classmethod
    def get_one_product(cls, data):
        query= "SELECT * FROM products WHERE id = %(id)s"
        results = connectToMySQL("gangsters_paradise").query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_all_products_with_user(cls):
        query = "SELECT * FROM products JOIN users ON users_id = users.id"
        products = connectToMySQL("gangsters_paradise").query_db(query)
        results = []
        for product in products:
            print(product)
            a_product = cls(product)
            creator_data = {
                "id" : product["users.id"],
                "first_name": product["first_name"],
                "last_name": product["last_name"],
                "email": product["email"],
                "password": product["password"],
                "created_at": product["users.created_at"],
                "updated_at": product["users.updated_at"]
            }
            user_instacne = user.User(creator_data)
            a_product.creator = user_instacne
            results.append(a_product)
        return results

    @classmethod
    def get_one_with_users(cls,data):
        query= "SELECT * FROM products JOIN users on users.id = products.users_id WHERE products.id = %(id)s;"
        product_from_db = connectToMySQL("gangsters_paradise").query_db(query, data)
        product_instance = cls(product_from_db[0])
        user_dictionary = {
        'id':product_from_db[0]['users.id'],
        'first_name' :product_from_db[0]['first_name'],
        'last_name' :product_from_db[0]['last_name'],
        'email':product_from_db[0]['email'],
        'password' :product_from_db[0]['password'],
        'created_at' :product_from_db[0]['users.created_at'],
        'updated_at' :product_from_db[0]['users.updated_at'],
        }
        this_user = user.User(user_dictionary)
        product_instance.creator = this_user 
        return product_instance


    @classmethod
    def update_product (cls, data):
        query = "UPDATE products SET name=%(name)s, price=%(price)s, "\
        "description=%(description)s  WHERE products.id = %(prod_id)s"
        return connectToMySQL("gangsters_paradise").query_db(query, data)

    @classmethod
    def delete_product(cls, data):
        query = "DELETE FROM products WHERE id = %(id)s"
        return connectToMySQL("gangsters_paradise").query_db(query, data)


    @staticmethod
    def validate_product(data):
        is_valid = True
        if len(data['name']) < 1:
            flash("Name of product has to be atleast 1 character", "error")
            is_valid = False
#        if int(data['price']) < 1:
#            flash("Product cannot be worth 0.00", "error")
#            is_valid = False
        if len(data['description']) < 1:
            flash("Must have a description", "error")
            is_valid = False
        return is_valid

