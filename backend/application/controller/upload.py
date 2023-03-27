import os
from flask import current_app as  app
from application.data.database import db
from flask import send_from_directory, request, jsonify, url_for
from werkzeug.utils import secure_filename
from flask_security import auth_required, current_user
from uuid import uuid4


def unique_name(string):
    ident = uuid4().__str__()
    return f"{ident}-{string}"

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# app.add_url_rule(
#     "/uploads/<filename>", endpoint="download_file", build_only=True
# )


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload-blog-image', methods=['GET', 'POST'])
@auth_required('token')
def upload_blog_image():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp

        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            resp = jsonify({'message': 'No file selected for uploading'})
            resp.status_code = 400
            return resp

        if file and allowed_file(file.filename):
            original_filename = secure_filename(file.filename)
            unique_filename = unique_name(original_filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            resp = jsonify({'link': url_for('download_file', filename=unique_filename)})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify({'message': 'Allowed file types png, jpg, jpeg'})
            resp.status_code = 400
            return resp


@app.route('/upload-dp', methods=['GET', 'POST'])
@auth_required('token')
def upload_dp():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp

        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            resp = jsonify({'message': 'No file selected for uploading'})
            resp.status_code = 400
            return resp

        if file and allowed_file(file.filename):
            original_filename = secure_filename(file.filename)
            unique_filename = unique_name(original_filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            current_user.dp_url = url_for('download_file', filename=unique_filename)
            db.session.commit()
            resp = jsonify({'link': url_for('download_file', filename=unique_filename)})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify({'message': 'Allowed file types png, jpg, jpeg'})
            resp.status_code = 400
            return resp