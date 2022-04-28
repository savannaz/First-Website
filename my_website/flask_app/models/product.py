from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Product:
    db = "online-website"
    __tablename__ = 'products'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.label = db_data['label']
        self.price = db_data['price']
        self.quantity = db_data['quantity']
        self.category = db_data['category']
        self.description = db_data['description']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save_product(cls, data):
        query = "INSERT INTO products (label, price, quantity, category, description, user_id, created_at) VALUES(%(label)s, %(price)s, %(quantity)s, %(category)s, %(description)s, %(user_id)s, NOW());"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def all_products(cls):
        query = "SELECT * FROM products;"
        return connectToMySQL(cls.db).query_db(query)

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM products WHERE id = %(id)s;"
        results =  connectToMySQL(cls.db).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE products SET label=%(label)s, price=%(price)s, quantity=%(quantity)s, category=%(category)s, description=%(description)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM products WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)


    @classmethod
    def add_to_cart(cls,data):
        query = "INSERT INTO carts (user_id, product_id, qty) VALUES (%(user_id)s, %(product_id)s, 1);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def items_in_cart(cls,data):
        query = "SELECT users.id, users.first_name, users.last_name, users.email, carts.user_id, carts.product_id, carts.qty, products.id, products.label, products.price, products.quantity FROM products JOIN carts ON products.id = carts.product_id LEFT JOIN users on carts.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return results

    @classmethod
    def remove_product_from_cart(cls, data):
        query = "DELETE FROM carts WHERE user_id = %(user_id)s AND product_id = %(product_id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_total_in_cart():
        pass

    @staticmethod
    def validate_product(product):
        is_valid = True
        if len(product['label']) < 1:
            flash("Please enter valid label","product")
            is_valid=False
        if len(product['price']) < 1 :
            is_valid = False
            flash("Please enter a price","product")
        if len(product['description']) < 1 or len(product['description']) > 800:
            is_valid = False
            flash("Description max is 800 characters", "product")
        if len(product['category']) < 1:
            is_valid = False
            flash("Please enter a category","product")
        return is_valid