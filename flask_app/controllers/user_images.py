from flask_app import app 
from flask import render_template, request, redirect, flash
import os
from werkzeug.utils import secure_filename
from flask_app.models.user_image import User_Image

UPLOAD_FOLDER = 'C:/coding_dojo/ufo_project/static/img'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/profile/image/<int:id>', methods=['GET', 'POST'])
def upload_file(id):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(f"/profile/{id}")
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(f"/profile/{id}")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = {
                "image_path": f"/static/img/{filename}"
            }
            User_Image.add_user_image(data) #adds image into the database
        return redirect(f'/users/{id}')