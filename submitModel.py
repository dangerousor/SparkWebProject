#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint, request, jsonify
# from numpy import array
# from pyspark.mllib.clustering import KMeans, KMeansModel, SparkContext
import time

from ext import con

bp = Blueprint('model', __name__, url_prefix='/model')


@bp.route('/<user>', methods=['POST', 'GET'])
def model(user):
    # now = str(int(time.time()))
    # sc = SparkContext(appName="model")
    # # Load and parse the data
    # data = sc.textFile("data/mllib/kmeans_data.txt")
    # parseddata = data.map(lambda line: array([float(x) for x in line.split(' ')]))
    # # Build the model (cluster the data)
    # clusters = KMeans.train(parseddata, 2, maxIterations=10, initializationMode="random")
    # clusters.save(sc, "files/" + id + '/model/' + now)
    if request.method == 'POST':
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        data = request.form
        if data['comment'] == '':
            comment = 'null'
        else:
            comment = '"' + data['comment'] + '"'
        value = '("' + user + '", "' + data["modelName"] + '","' + data["dataName"] + '",' + comment + ',"' + now + '",0 , 0)'
        sql = 'insert into model (user, modelname, dataname, comment, subtime, status, category) values ' + value
        print sql
        with con as cur:
            try:
                cur.execute(sql)
                return jsonify({'status': 1})
            except:
                return jsonify({'status': -1})
    else:
        with con as cur:
            cur.execute('select * from model where user = ' + user)
            rows = cur.fetchall()
            result = {'size': len(rows)}
            content = []
            for row in rows:
                tmp = dict()
                tmp['comment'] = row[4]
                tmp['modelName'] = row[2]
                tmp['trainData'] = row[3]
                tmp['submitTime'] = row[5]
                tmp['endTime'] = row[6]
                tmp['status'] = row[7]
                tmp['modelCategory'] = row[8]
                content.append(tmp)
            result['content'] = content
        return jsonify(result)
