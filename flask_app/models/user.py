from flask_app.config.mysqlconnection import connectToMySQL #from our flask app, from our config folder, from our mysqlconnection file import the function of connect to mysql
from flask import flash 
import re
#added 10222
from flask_app.models.user_image import User_Image

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
        # self.user_images = []
#added 10222 I'm creating a place to store the user_images
#using this for function all_user_images_by_user

    #add user
    @classmethod 
    def add_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, user_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(user_name)s, %(email)s, %(password)s);"
        return connectToMySQL(db).query_db(query, data)

    #get user by id
    @classmethod 
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return results[0]


    #get user by email
    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query,data)
        # Didn't find a matching user
        #need this if statement to get a reply
        if len(result) < 1:
            return False
        return cls(result[0]) #0 because where only returning that one result

    #update user
    @classmethod
    def update_user(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, user_name = %(user_name)s, email = %(email)s, password = %(password)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)
        
# What kind of method do we need into order to perform our validations? check our data looks good first before we allow a new user to be registered in our database 
#staticmethod is where we put all of our validations
    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
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
        query = "SELECT * FROM users WHERE user_name = %(user_name)s"
        user_matches = connectToMySQL(db).query_db(query, {"user_name": user['user_name']})
        if len(user_matches) > 0:
            flash("Username is already being used. Please Try another name.")
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

#added 10222 https://www.youtube.com/watch?v=niUyT1Ohmcs 34:03
    #Check w/ peter
    # @classmethod
    # def all_user_images_by_user(cls, data):
    #     #left join statement will go here
    #     # get 1 user with all its images
    #     query = "SELECT * FROM user LEFT JOIN user_images ON user.id = user_images.user_id WHERE id = %(id)s;"
    #     results = connectToMySQL(db).query_db(query, data)
    #     #create a print statement if it ever fails, the print statement will help you figure out where it faled. 
    #     print("getting model all_user_images results:", results)
    #     user_images = []
    #     for row in results: 
    #         user_images_data = {
    #             "id": row["user_images.id"], #I want the user_images.id
    #             "image_path": row["image_path"],
    #             "created_at": row["created_at"],
    #             "updated_at": row["updated_at"],
    #             "user_id": row["user_id"],
    #         }
    #         #the top will be all the data coming back. 
    #         print("each row of user_images_data from Model: ", row)
    #         #append(add user_images data to the user_images =[])
    #         User.user_images.append(user_images_data)
    #         print("printing the list from Models: ", User)
    #     return User.user_images




#9/10 you will have 5 class methods for every model, possibly more, rarely less
#1)get_all, 2)get_one, 3)save, 4)update, 5)delete
# every class except for the get_all will always have cls, data because it is either taking something from a form or it is being passed in information.
# get_one and delete will have where clause
# update will have where clause but also value sections