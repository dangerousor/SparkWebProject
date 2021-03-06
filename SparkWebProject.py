# -*- coding:utf-8 -*-

from flask import Flask, jsonify

from ext import get_con, mako, render_template

import Model
import Task


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
    con = get_con()
    cur = con.cursor()
    cur.execute("select * from trainfile where user = " + id)
    rows = cur.fetchall()
    con.close()
    namelist = []
    for row in rows:
        namelist.append(row[1])
    return jsonify({'fileNameList': namelist})


@app.route('/testfile/<id>', methods=['GET'])
def testfile(id):
    con = get_con()
    cur = con.cursor()
    cur.execute("select * from testfile where user = " + id)
    rows = cur.fetchall()
    con.close()
    namelist = []
    for row in rows:
        namelist.append(row[1])
    return jsonify({'fileNameList': namelist})


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


app.register_blueprint(Model.bp)
app.register_blueprint(Task.bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9990, debug=True)
