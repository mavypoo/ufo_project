from flask_app.config.mysqlconnection import connectToMySQL #from our flask app, from our config folder, from our mysqlconnection file import the function of connect to mysql
from flask import flash 
# from flask_app.models.user import User DO we need this? Are we calling anything from the Users class?

db = "ufos_project"
class User_Image:
    def __init__(self, data):
        self.id = data["id"]
        self.image_path = data["image_path"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

#I think this is wrong
    @classmethod
    def get_image_by_user(cls, data):
        query = "SELECT * FROM user_images WHERE user_id = %(user_id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod 
    def add_user_image(cls, data):
        query = "INSERT INTO user_images VALUES (%(image_path)s);"
        results = connectToMySQL(db).query_db(query, data)
        return results 


#circular import, remove the class and import the file vs the class. Its when you have it going both ways on both files. 