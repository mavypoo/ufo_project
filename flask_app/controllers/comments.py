from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.comment import Comment


#add_comment_form - will sit in the sighting view page, dont need a comment page

#add_comment_db
@app.route("/comment/create/<int:sighting_id>/<int:user_id>", methods=["POST"])
def create_comment(sighting_id, user_id):
    #1 Validate, request form its a function fask 
    if not Comment.validate_comment(request.form):
        #2 Always  redirect to the reoute that you were at last!
        return redirect(f"/sighting/{sighting_id}")
    data = {
        "content": request.form["content"],
        "sighting_id": sighting_id,
        "user_id": user_id
    }
    print(Comment.add_comment(data))
    return redirect(f"/sighting/{sighting_id}")


#sighting_id redirects back; comment_id knows which one update etc
@app.route("/comment/update/<int:comment_id>/<int:sighting_id>", methods=["POST"])
def update_comment(comment_id, sighting_id):
    #1 Validate, request form its a function fask 
    if not Comment.validate_comment(request.form):
        #2 Always  redirect to the reoute that you were at last!
        return redirect(f"/sighting/{sighting_id}")
    data = {
        "id": comment_id,
        "content": request.form["content"]
    }
    Comment.update_comment(data)
    return redirect(f"/sighting/{sighting_id}")


@app.route("/comment/delete/<int:comment_id>/<int:sighting_id>")
def delete_comment(comment_id, sighting_id):
    data = {
        "id": comment_id
    }
    Comment.delete_comment(data)
    return redirect(f"/sighting/{sighting_id}")