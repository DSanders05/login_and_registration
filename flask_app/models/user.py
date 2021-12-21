from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_user_by_email(User, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('login_and_registration_schema').query_db(query, data)

        if len(result) == 0:
            return None

        else:
            return User(result[0])

    @classmethod
    def create_new_user(User, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL('login_and_registration_schema').query_db(query, data)
        return result

    @staticmethod
    def validate_user(data):
        is_valid = True

        if len(data['first_name']) > 50 or len(data['first_name']) < 3:
            is_valid = False
            flash("User first name must be 2 to 50 characters long.")

        if len(data['last_name']) > 50 or len(data['last_name']) < 3:
            is_valid = False
            flash("User last name must be 2 to 50 characters long.")

        if not email_regex.match(data['email']):
            is_valid = False
            flash("Please provide a valid email address")

        elif User.get_user_by_email(data) != None:
            is_valid = False
            flash("Email is already in use.")
        
        if len(data['password']) < 8:
            is_valid = False
            flash("Password must be at least 8 characters in length.")

        if data['password'] != data['confirm_password']:
            is_valid = False
            flash("Please ensure passwords match.")

        return is_valid