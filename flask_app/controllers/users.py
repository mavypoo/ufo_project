from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("sign_in.html")

@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")

@app.route('/register_user', methods=['POST'])
def register_user():
    # Validate - check if email exists, if so, check if the password is correcct
    if not User.validate_user(request.form):
        #if the validation failes, redirect back to the route that has that form.
        return redirect('/sign_up')
    #bcrypt changes the password for security password, stores in hashpass as the password as oppose to the actual password
    hash_pass = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "user_name": request.form['user_name'],
        "email": request.form['email'],
        "password": hash_pass
    }
    id = User.add_user(data)
    # Save ID in session; so we can check the user ID is in session. 
    session['user_id'] = id
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['user_name'] = request.form['user_name']
    return redirect('/sightings')

# /login (INVISIBLE POSTcd route) - logs a user in 
@app.route('/login_user', methods=['POST'])
def login_user():
    data = {
        "email": request.form['email'],
    }
    #Validate - check if the email exist, if so, check if the password is correct
    this_user = User.get_user_by_email(data)
    if not this_user:
        flash("Invalid Email or Password")
        return redirect('/')
    if not bcrypt.check_password_hash(this_user.password, request.form['password']):
        flash("Invalid Email or Password")
        return redirect('/')
    # Savide ID in session
    session['user_id'] = this_user.id
    session['first_name'] = this_user.first_name
    session['last_name'] = this_user.last_name
    session['user_name'] = request.form['use_name']
    # Redirect to /sightings
    return redirect('/sightings')

@app.route("/sightings")
def success():
    #Check to see if someone is logged in -- if not, send them back to the login/registration page. If someones not logged in they cant access those pages. 
    if "user_id" not in session:
        flash("You must be logged in to view this page")
        return redirect("/")
    return render_template("sightings.html")

# /logout (INVISIBLE route) - clears session, sends the user back to login/registration page. 
@app.route("/logout")
def logout():
    # Clear session 
    session.clear() # Removes the user from session 
    # Redirect to login/registration route 
    return redirect("/")