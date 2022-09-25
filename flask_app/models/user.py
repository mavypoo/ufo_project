from flask_app.config.mysqlconnection import connectToMySQL #from our flask app, from our config folder, from our mysqlconnection file import the function of connect to mysql
from flask import flash 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')  
# PASSWORD REGEX = re.compile() # https://www.ocpsoft.org/tutorials/regular-expressions/password-regular-expression/

#the only time order matters is in your sql statements and even that does not have to match the ERD, it just has to match itself.

db = "ufos_project"
class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.user_name = data["user_name"]
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at'] 


    @classmethod 
    def add_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(db).query_db(query, data)


    @classmethod 
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        if len(results) == 0:
            return None
        else: 
            return cls(results[0])

    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])


# What kind of method do we need into order to perform our validations? check our data looks good first before we allow a new user to be registered in our database 
    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s"
        email_matches = connectToMySQL(db).query_db(query, {"email": user['email']})
        if len(email_matches) > 0:
            flash("Email is already registered")
            is_valid = False
        if len(user['first_name']) < 3:
            flash('First name must be at least 3 characters long.')
            is_valid = False
        if len(user['last_name']) < 3:
            flash('Last name must be at least 3 characters long.')
            is_valid = False
        if len(user['user_name']) < 3:
            flash("Username must be at least 3 characters long.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid Email Address!')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters long.')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash('Passwords do not match!')
            is_valid = False
        return is_valid


#9/10 you will have 5 class methods for every model, possibly more, rarely less
#1)get_all, 2)get_one, 3)save, 4)update, 5)delete
# every class except for the get_all will always have cls, data because it is either taking something from a form or it is being passed in information.
# get_one and delete will have where clause
# update will have where clause but also value sections