from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.sighting import Sighting
from flask_app.models.comment import Comment


#add_sighing_form
@app.route("/sighting/add")
def add_sighting_page():
    if "user_id" not in session:
        flash("You must be logged in to view this page")
        return redirect("/")
    return render_template("sighting_create.html")


#add_sighting to db
@app.route("/sighting/create", methods=["POST"])
def create_sighting():
    #1. Validate; request.form its a function flask
    if not Sighting.validate_sighting(request.form):
        #2. Always redirect to the route that you were at last!!
        return redirect("/sighting/add")
    #Why we need this? data prevents SQL injection, the process of using the data in the url to execute commands in the database
    data = {
        "location": request.form["location"],
        "date": request.form["date"],
        "time": request.form["time"],
        "description": request.form["description"],
        "Intensity": request.form["Intensity"],
        "num_of_activities": request.form["num_of_activities"],
        "reaction": request.form["reaction"],
        "title": request.form["title"],
        "user_id": session["user_id"]
    }
    #call the function that does the query, pass in data to edit th database
    #call the sighting class and the add_sighting function
    Sighting.add_sighting(data)
    return redirect("/sightings")


#edit_sighting_form
@app.route("/sighting/edit/<int:id>")
def edit_sighting_page(id):
    if "user_id" not in session:
        flash("You must be logged in to view this page")
        return redirect("/")
    #passing in id; so we need to create a data dictionary
    data = {
        "id": id
    }
    this_sighting = Sighting.get_one_sighting_by_user(data)
    return render_template("sighting_edit.html", this_sighting=this_sighting)


#edit_sighting_db
@app.route("/sighting/update/<int:id>", methods=["POST"])
def update_sighting_page(id):
        #1. Validate; request.form its a function flask
    if not Sighting.validate_sighting(request.form):
        #2. Always redirect to the route that you were at last!!
        return redirect(f"/sighting/edit/{id}")
    #Why we need this? data prevents SQL injection, the process of using the data in the url to execute commands in the database
    data = {
        "id": id,
        "location": request.form["location"],
        "date": request.form["date"],
        "time": request.form["time"],
        "description": request.form["description"],
        "Intensity": request.form["Intensity"],
        "num_of_activities": request.form["num_of_activities"],
        "reaction": request.form["reaction"],
        "title": request.form["title"]
    }
    #call the function that does the query, pass in data to edit the database
    #call the sighting class and the add_sighting function
    Sighting.update_sighting(data)
    return redirect(f'/sighting/{id}')


#view sightings, Route that will show an individual game - visible route 
@app.route("/sighting/<int:id>")
def view_sighting(id):
    #1 Check to see if someone is logged in 
    if "user_id" not in session:
        flash("You must be logged in to view this page")
        return redirect("/")
    data = {
        "id": id,
    }
    this_sighting = Sighting.get_one_sighting_by_user(data)
    all_comments = Comment.get_comment_by_sighting_and_user(data)
    return render_template("sighting_view.html", this_sighting = this_sighting, all_comments = all_comments)


#Route that will delete a game, Need the id of the game to delete 
@app.route("/sighting/delete/<int:id>")
def delete_sighting(id):
    #1 check to see if someone is logged in 
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id, # ID of the sighting
    }
    Sighting.delete_sighting(data)
    return redirect("/")



# #users dashboard
# @app.route("/user")

# #view everyones post on dashboard
# @app.route("/dashboard")


#sql_injection