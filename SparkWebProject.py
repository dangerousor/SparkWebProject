# -*- coding:utf-8 -*-

from flask import Flask, jsonify

from ext import con, mako, render_template

import submitModel


app = Flask(__name__, template_folder='templates',
            static_folder='static')
app.config.from_object('config')


mako.init_app(app)


@app.route('/')
def hello_world():
    return render_template('index.html')
    # return 'Hello World!'


@app.route('/trainfile/<id>', methods=['GET'])
def trainfile(id):
    with con as cur:
        cur.execute("select * from trainfile where user = " + id)
        rows = cur.fetchall()
        namelist = []
        for row in rows:
            namelist.append(row[1])
    return jsonify({'fileNameList': namelist})


@app.route('/testfile/<id>', methods=['GET'])
def testfile(id):
    with con as cur:
        cur.execute("select * from testfile where user = " + id)
        rows = cur.fetchall()
        namelist = []
        for row in rows:
            namelist.append(row[1])
    return jsonify({'fileNameList': namelist})


app.register_blueprint(submitModel.bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
