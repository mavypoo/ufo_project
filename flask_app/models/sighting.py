from lib2to3.pytree import _Results
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

db = "ufos_project"
# data holds a dictionary of all these attributes
class Sighting:
    def __init__(self, data):
        self.id = data["id"]
        self.location = data["location"]
        self.date = data["date"]
        self.time = data["time"]
        self.description = data["description"]
        self.Intensity = data["Intensity"]
        self.num_of_activities = data["num_of_activities"]
        self.reaction = data["reaction"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    # cls gets all the attributes from the class to the method
    # Method to add a sighting to the database
    @classmethod
    def add_sighting(cls):
        query = "INSERT INTO sightings (location, date, time, description, Intensity, num_of_activities, reaction, user_id) VALUES (%(location)s, %(date)s, %(time)s, %(description)s, %(Intensity)s, %(num_of_activities)s, %(reaction)s, %(user_id)s);"
        results = connectToMySQL
        # returning to see if the data was entered to the database
        return results

    # Need to include data because we need to pull the data to be able to update the data
    @classmethod
    def update_sighting(cls, data):
        query = "UPDATE sightings SET location = %(location)s, date = %(date)s, time = %(time)s, description = %(description)s, Intensity = %(Intensity)s, num_of_activities = %(num_of_activities)s, reaction = %(reaction)s WHERE id = %(id)s;"
        # the id of the sighting, since we're making changes to the sighting (we need to know what changes have been made to the sighting)
        return connectToMySQL(db).query_db(query, data)


    # Get one sighting made by the user
    # View sighting page
    @classmethod
    def get_one_sighting_by_user(cls, data):
        query = "SELECT * FROM sightings JOIN users on users.id = sightings.user_id WHERE sightings.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return results

    # Main page - cards - all sightings by users
    @classmethod
    def get_all_sightings_by_users(cls, data):
        query = "SELECT * FROM sightings JOIN users on users.id = sightings.user_id;"
        results = connectToMySQL(db).query_db(query, data)
        return results

    # User dashboard
    @classmethod
    def get_all_sightings_by_user(cls, data):
        query = "SELECT * from sightings JOIN users on users.id = sightings.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return results


    # Need to include data because we need to pull the data to be able to update the data
    @classmethod
    def delete_sighting(cls, data):
        query = "DELETE FROM sightings WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return results

    #
    @staticmethod 
    def validate_sighting(sighting):
        is_valid = True 
        #if its true, it will store the data into the database
        if len(sighting["location"]) < 3:
            flash("Location must be at least 3 characters long")
            is_valid = False 
        if not sighting["date"]: #if date not filled in
            flash("Date must be filled in")
            is_valid = False
        if not sighting["time"]: #if date not filled in
            flash("Time must be filled in") 
            is_valid = False
        if len(sighting["description"]) < 3:
            flash("Description must be at least 3 characters long")
            is_valid = False 
        if sighting["num_of_activities"] < 1:
            flash("number of activities must be atleast 1")
            is_valid = False 
        if len(sighting["reaction"]) < 3:
            flash("Reaction must be at least 3 characters long")
            is_valid = False 
        return is_valid




        

#The Static methods are used to do some utility tasks, and class methods are used for factory methods
