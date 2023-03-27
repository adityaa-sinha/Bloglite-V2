from flask import current_app as  app
from flask import request
from application.jobs import tasks
from flask_security import auth_required, current_user
from flask import send_from_directory, url_for



# User-triggered backend job


@app.route('/exports/<filename>')
def download_exported_file(filename):
    return send_from_directory(app.config["EXPORT_FOLDER"], filename, as_attachment = True)


@app.route('/export')
@auth_required('token')
def export():
    if request.method == 'GET':
        username = current_user.username
        try:
            res = tasks.export_as_csv.delay(username)
            filename = res.get()
            return {
                "download_link" : url_for('download_exported_file', filename = filename)
            }
        except:
            return '', 500

