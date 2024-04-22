import re
from Flask_app.config.mysqlconnect import connectToMySQL
from flask import flash

DB_SCHEMA = 'northwest_pizza_schema'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        if len(user['state']) != 2:
            flash("State must be 2 characters.")
            is_valid = False
        if len(user['state']) != 2:
            flash("State must be 2 characters.")
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM User WHERE email = %(email)s;"
        result = connectToMySQL(DB_SCHEMA).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def save(cls, data):
        query = ("INSERT INTO User(first_name,last_name,email,address,city,state,password,created_at,updated_at)"
                 " VALUES (%(first_name)s,%(last_name)s,%(email)s,%(address)s,%(city)s,%(state)s,%(password)s,NOW(),NOW());")

        result = connectToMySQL(DB_SCHEMA).query_db(query, data)
        return result

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM User WHERE id = %(id)s ;"
        result = connectToMySQL(DB_SCHEMA).query_db(query, data)
        return cls(result[0])

    @classmethod
    def update(cls, data):
        query = ("UPDATE User SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,"
                 "address=%(address)s,city=%(city)s,state=%(state)s,updated_at=NOW() WHERE id=%(id)s;")
        return connectToMySQL(DB_SCHEMA).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM User WHERE id =  %(id)s;"
        return connectToMySQL(DB_SCHEMA).query_db(query, data)
