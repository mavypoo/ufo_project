from flask_app import app #need this for the app.route. We need to know what the app part is before we can start using it.
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.sighting import Sighting
from flask_app.models.user_image import User_Image
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#sign in page. 
@app.route("/")
def index():
    return render_template("sign_in.html")

#sign up page
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
    # Save ID in session
    session['user_id'] = this_user.id
    session['first_name'] = this_user.first_name
    session['last_name'] = this_user.last_name
    # session['user_name'] = request.form['user_name']
    # Redirect to /sightings
    return redirect('/sightings')

@app.route("/sightings")
def success():
    #Check to see if someone is logged in -- if not, send them back to the login/registration page. If someones not logged in they cant access those pages. 
    if "user_id" not in session:
        flash("You must be logged in to view this page")
        return redirect("/")
    all_post = Sighting.get_all_sightings_by_users()
    return render_template("sightings.html", all_post=all_post)



@app.route("/user/<int:id>")
def user_dashboard(id):
    data = {
        "id": id
    }
    this_user = User.get_user(data)
    # this_user_image = User_Image.get_image_by_user(data)
    this_user_posts = Sighting.get_all_sightings_by_user(data)
    print(this_user_posts)
    return render_template("user.html", this_user = this_user, this_user_posts = this_user_posts)

@app.route("/profile/<int:id>")
def profile_page(id):
    data = {
        "id": id
    }
    this_user = User.get_user(data)
    this_user_image = User_Image.get_image_by_user(data)
    return render_template("profile.html", this_user = this_user, this_user_image = this_user_image)

@app.route("/profile/update/<int:id>")
def update_profile(id):
    # Validate 
    if not User.validate_user(request.form):
        #if the validation failes, redirect back to the profile
        return redirect('/profile/{id}')
    #bcrypt changes the password for security password, stores in hashpass as the password as oppose to the actual password
    hash_pass = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "id": id,
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "user_name": request.form['user_name'],
        "email": request.form['email'],
        "password": hash_pass
    }
    User.update_user(data)
    return redirect("/user/{id}")


@app.route("/contact")
def contact():
    return render_template("contact.html")

# /logout (INVISIBLE route) - clears session, sends the user back to login/registration page. 
@app.route("/logout")
def logout():
    # Clear session 
    session.clear() # Removes the user from session 
    # Redirect to login/registration route 
    return redirect("/")