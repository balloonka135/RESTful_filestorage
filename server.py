#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Flask app that allows uploading and downloading files from Amazon S3 service
by making request to REST API.
All the credentials are stored in config file.
List of endpoints:

- /api/v1.0/upload -- upload file to S3
- /api/v1.0/uploads -- list of uploaded files in S3
- /api/v1.0/uploads/<file> -- check whether file is uploaded to S3
- /api/v1.0/downloads/<file> -- download file to localhost

'''
from flask import Flask, abort, jsonify, request, redirect, render_template, flash, url_for
from werkzeug import secure_filename
from s3_storage import *
import config


ALLOWED_EXTENSIONS = ['txt', 'pdf', 'doc']


app = Flask(__name__)


def allowed_file(filename):
    '''
    Validate correct file extension.
    '''
    return filename[-3:].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return redirect(url_for('upload_to_bucket'))


@app.route(config.REST_API + config.FILE_POST, methods=['GET', 'POST'])
def upload_to_bucket():
    '''
    Uploading file by using s3_storage module functions.
    '''
    if request.method == 'POST':
        if 'file' not in request.files:
            abort(404, "No 'file' key in request.files")
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.filename = secure_filename(file.filename)

            # transfer parameters to back-end function
            result = upload_file(file, config.S3_BUCKET)
            return jsonify({'s3_url': str(result)})

    return render_template('index.html')


@app.route(config.REST_API + config.FILE_GET, methods=['GET'])
def download_file_from_bucket(filename):
    result = download_file(filename, config.S3_BUCKET)
    if result:
        return jsonify({'status': 200, 'msg': 'Success download.'})
    else:
        abort(404, "The object does not exist.")


@app.route(config.REST_API + config.FILES_LIST_GET, methods=['GET'])
def get_files_in_bucket():
    result = bucket_content(config.S3_BUCKET)
    if result[0]:
        return jsonify({'status': 200, 'objects': result[1]})
    else:
        abort(404, result[1])


@app.route(config.REST_API + config.FILE_CHECK_GET, methods=['GET'])
def check_file_in_bucket(filename):
    result = check_file(filename, config.S3_BUCKET)
    if result:
        return jsonify({'status': 200, 'msg': 'Object exists.'})
    else:
        abort(404, "The object does not exist.")
        # abort(404)


if __name__ == '__main__':
    app.run(debug=True)
