from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 

db = "ufos_project"
class Believer:
    def __init__(self, data):
        self.id = data["id"]
        self.created_at = data["id"]
        self.updated_at = data["id"]


    @classmethod 
    def get_all_believers(cls):
        query = "SELECT * FROM believers"
        results = connectToMySQL(db).query_db(query)
        return results

    @classmethod 
    def get_num_believers(cls, data):
        query = "SELECT COUNT(sighting_id) FROM believers"
        results = connectToMySQL(db).query_db(query, data)
        return results[0]['COUNT(sighting_id)']

    @classmethod 
    def add_believer(cls, data):
        query = "INSERT INTO believers (user_id, sighting_id) VALUES (%(user_id)s, %(sighting_id)s);"
        results = connectToMySQL(db).query_db(query, data)
        return results


    @classmethod
    def remove_believer(cls, data):
        query = "DELETE FROM believers WHERE user_id=%(user_id)s AND sighting_id=%(sighting_id)s"
        results = connectToMySQL(db).query_db(query, data)
        return results


