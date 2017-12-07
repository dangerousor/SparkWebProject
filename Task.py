#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint, request, jsonify
from multiprocessing import Process
# from numpy import array
# from pyspark.mllib.clustering import KMeans, KMeansModel, SparkContext
import time

from ext import con
# from ext import conn
from DoSpark import dotaskspark

bp = Blueprint('task', __name__, url_prefix='/task')


@bp.route('/<modelid>', methods=['POST', 'GET'])
def task(modelid):
    if request.method == 'POST':
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        data = request.form
        if len(data) == 0:
            with con as cur:
                sql = 'select user, modelname, dataname from model where id = ' + modelid
                cur.execute(sql)
                row = cur.fetchone()
                sql = 'insert task (modelid, subtime, status, testfile, modelname, category, user) values (' + modelid + ',"' + now + '",0,' + '"' + row[2] + '","' + row[1] + '",0,"' + row[0] + '")'
                # if row[3] is None:
                #     sql = 'insert task (modelid, subtime, status, testfile, modelname, category, user) values (' + modelid + ',"' + now + '",0,' + '"' + row[2] + '","' + row[1] + '",0,"' + row[0] + '")'
                # else:
                #     sql = 'insert task (modelid, subtime, status, testfile, comment, modelname, category, user) values (' + modelid + ',"' + now + '",0,' + '"' + row[2] + '","' + row[3] + '","' + row[1] + '",0,"' + row[0] + '")'
                try:
                    cur.execute(sql)
                    sql = 'select id from task where subtime = "' + now + '"'
                    cur.execute(sql)
                    row = cur.fetchone()
                    p = Process(target=dotaskspark, args=(str(row[0]),))
                    p.start()
                    return jsonify({'status': 1})
                except:
                    return jsonify({'status': 0})
        else:
            with con as cur:
                sql = 'select user, modelname, modelfile from model where id = ' + modelid
                cur.execute(sql)
                row = cur.fetchone()
                if data['comment'] == '':
                    sql = 'insert task (modelid, subtime, status, testfile, modelname, category, user, modelfile) values (' + modelid + ',"' + now + '",0,' + '"' + data['dataName'] + '","' + row[1] + '",0,"' + row[0] + '","' + row[2] + '")'
                else:
                    sql = 'insert task (modelid, subtime, status, testfile, comment, modelname, category, user, modelfile) values (' + modelid + ',"' + now + '",0,' + '"' + data['dataName'] + '","' + data['comment'] + '","' + row[1] + '",0,"' + row[0] + '","' + row[2] + '")'
                try:
                    cur.execute(sql)
                    sql = 'select id from task where subtime = "' + now + '"'
                    cur.execute(sql)
                    row = cur.fetchone()
                    p = Process(target=dotaskspark, args=(str(row[0]),))
                    p.start()
                    return jsonify({'status': 1})
                except:
                    return jsonify({'status': 0})
    else:
        with con as cur:
            cur.execute('select * from task where user = ' + modelid)
            rows = cur.fetchall()
            result = {'size': len(rows)}
            content = []
            for row in rows:
                tmp = dict()
                tmp['comment'] = row[6]
                tmp['modelName'] = row[7]
                tmp['testData'] = None
                tmp['submitTime'] = row[2]
                tmp['endTime'] = row[3]
                tmp['status'] = row[4]
                if row[8] != 0:
                    tmp['testData'] = row[5]
                tmp['id'] = row[0]
                content.append(tmp)
            result['content'] = content
        return jsonify(result)


@bp.route('/td/<taskid>', methods=['POST'])
def td(taskid):
    pass


@bp.route('/download/<taskid>', methods=['GET'])
def download(taskid):
    pass
