from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.believer import Believer 

@app.route("/create/believer", methods=["POST"])
def add_believer():
    data = {
        "user_id": request.form["user_id"],
        "sighting_id": request.form["sighting_id"]
    }
    Believer.add_believer(data)
    return redirect(f"/sighting/{request.form['sighting_id']}")
    pass

@app.route("/delete/believer/<int:user_id>/<int:sighting_id>")
def remove_believer(user_id, sighting_id):
    data = {
        "user_id": user_id,
        "sighting_id": sighting_id
    }
    Believer.remove_believer(data)
    return redirect(f"/sighting/{sighting_id}")