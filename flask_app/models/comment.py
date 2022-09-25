from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


db = "ufos_project"
# data holds a dictionary of all these attributes
class Comment:
    def __init__(self, data):
        self.id = data["id"]
        self.content = data["content"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod 
    def add_comment(cls, data):
        query = "INSERT into comments (content) VALUES (%(content)s);"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def get_comment_by_sighting_and_user(cls, data):
        query = "SELECT * FROM comments JOIN sightings on sighthings.id = comments.sightings_id JOIN users on users.id = comments.user_id WHERE comments.id = %(id)s;"  
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def updated_comment(cls, data):
        query = "UPDATE comments SET content = %(content)s WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def delete_comment(cls, data):
        query = "DELETE FROM comments WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return results


    @staticmethod
    def validate_comment(comment):
        is_valid = True 
        if len(comment["content"]) < 3:
            flash("Content must be atleast 3 characters long")
            is_valid = False
        return is_valid