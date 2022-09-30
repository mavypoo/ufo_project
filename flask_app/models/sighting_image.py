from flask_app.config.mysqlconnection import connectToMySQL #from our flask app, from our config folder, from our mysqlconnection file import the function of connect to mysql
from flask import flash 

db = "ufos_project"
class Sighting_Image:
    def __init__(self, data):
        self.id = data["id"]
        self.image_path = data["image_path"]
        self.image_description = data["image_description"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
