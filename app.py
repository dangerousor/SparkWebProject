#!/usr/bin/python
# -*- coding:utf-8 -*-
import os

from werkzeug.wsgi import SharedDataMiddleware
from flask import abort, Flask, request, jsonify, redirect, send_file

from ext import db, mako, render_template
from models import InputFile
from utils import get_file_path, humanize_bytes

ONE_MONTH = 60 * 60 * 24 * 30

app = Flask(__name__, template_folder='templates',
            static_folder='static')
app.config.from_object('config')

app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/i/': get_file_path()
})

mako.init_app(app)
db.init_app(app)


@app.route('/d/<filehash>', methods=['GET'])
def download(filehash):
    input_file = InputFile.get_by_filehash(filehash)

    return send_file(open(input_file.path, 'rb'),
                     mimetype='application/octet-stream',
                     cache_timeout=ONE_MONTH,
                     as_attachment=True,
                     attachment_filename=input_file.filename.encode('utf-8'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        w = request.form.get('w')
        h = request.form.get('h')
        if not uploaded_file:
            return abort(400)

        if w and h:
            input_file = InputFile.rsize(uploaded_file, w, h)
        else:
            input_file = InputFile.create_by_upload_file(uploaded_file)
        db.session.add(input_file)
        db.session.commit()

        return jsonify({
            'url_d': input_file.url_d,
            'url_i': input_file.url_i,
            'url_s': input_file.url_s,
            'url_p': input_file.url_p,
            'filename': input_file.filename,
            'size': humanize_bytes(input_file.size),
            'time': str(input_file.uploadtime),
            'type': input_file.type,
            'quoteurl': input_file.quoteurl
        })
    return render_template('index.html', **locals())


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/j', methods=['POST'])
def j():
    uploaded_file = request.files['file']

    if uploaded_file:
        input_file = InputFile.create_by_upload_file(uploaded_file)
        db.session.add(input_file)
        db.session.commit()
        width, height = input_file.image_size

        return jsonify({
            'url': input_file.url_i,
            'short_url': input_file.url_s,
            'origin_filename': input_file.filename,
            'hash': input_file.filehash,
            'width': width,
            'height': height
        })

    return abort(400)


@app.route('/p/<filehash>')
def preview(filehash):
    input_file = InputFile.get_by_filehash(filehash)

    if not input_file:
        filepath = get_file_path(filehash)
        if not(os.path.exists(filepath) and (not os.path.islink(filepath))):
            return abort(404)

        input_file = InputFile.create_by_old_paste(filehash)
        db.session.add(input_file)
        db.session.commit()

    return render_template('success.html', p=input_file)


@app.route('/s/<symlink>')
def s(symlink):
    input_file = InputFile.get_by_symlink(symlink)

    return redirect(input_file.url_p)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
