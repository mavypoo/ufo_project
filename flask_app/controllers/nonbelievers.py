from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.nonbeliever import Nonbeliever 

@app.route("/create/nonbeliever", methods=["POST"])
def add_nonbeliever():
    data = {
        "user_id": request.form["user_id"],
        "sighting_id": request.form["sighting_id"]
    }
    Nonbeliever.add_nonbeliever(data)
    return redirect(f"/sighting/{request.form['sighting_id']}")
    pass

@app.route("/delete/nonbeliever/<int:user_id>/<int:sighting_id>")
def remove_nonbeliever(user_id, sighting_id):
    data = {
        "user_id": user_id,
        "sighting_id": sighting_id
    }
    Nonbeliever.remove_nonbeliever(data)
    return redirect(f"/sighting/{sighting_id}")