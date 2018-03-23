#!/usr/bin/python
# -*- coding:utf-8 -*-

import time

from ext import get_con, model_conn
from consts import PROJECT_PATH


import re
import numpy
import pyspark
from pyspark.mllib.clustering import KMeans


# SPARK_MASTER = 'spark://dangerous-Lenovo-Product:7077'
SPARK_MASTER = 'spark://blade01:7077'
# SPARK_MASTER就是集群的master的url


def domodelspark(modelid):
    sql = 'select user,modelname,dataname from model where id = ' + modelid
    con = get_con()
    cur = con.cursor()
    cur.execute(sql)
    model = cur.fetchone()
    if model is None:
        return
    else:
        pass
    flag = 0
    if model[1] == 'KMeans':
        try:
            modelfile = dokmeans(model[0], model[2], modelid)
        except:
            flag = 1
    else:
        pass
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    if flag == 0:
        cur.execute('update model set status = ' + '1' + ', endtime = ' + '"' + now + '", modelfile = "' + modelfile + '" where id = ' + modelid)
    else:
        cur.execute('update model set status = ' + '2' + ', endtime = ' + '"' + now + '" where id = ' + modelid)
    con.commit()
    con.close()
    return 0


def dotaskspark(taskid):
    flag = 0
    sql = 'select user,modelname,testfile, modelfile from task where id = ' + taskid
    con = get_con()
    cur = con.cursor()
    cur.execute(sql)
    task = cur.fetchone()
    if task is None:
        return
    else:
        pass
    if task[1] == 'KMeans':
        try:
            modelfile = dotaskkmeans(task[0], task[2], taskid)
        except:
            flag = 1
    else:
        pass
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    if flag == 0:
        cur.execute('update task set status = ' + '1' + ', endtime = ' + '"' + now + '", resultfile = "' + modelfile + '" where id = ' + taskid)
    else:
        cur.execute('update task set status = ' + '2' + ', endtime = ' + '"' + now + '" where id = ' + taskid)
    con.commit()
    con.close()
    return 0


def dokmeans(user, datafile, modelid):
    # textfile = sc.textFile("file://files/" + user + "/train/" + datafile)
    # print textfile.collect()
    # textfile.saveAsTextFile("file://files/" + user + "/model/" + modelid)
    # time.sleep(15)
    # path1 = 'file://' + PROJECT_PATH + '/files/' + user + '/train/' + datafile
    path1 = 'hdfs://blade01:9000' + '/user/hadoop' + '/files/' + user + '/' + datafile
    path2 = 'file://' + PROJECT_PATH + '/files/' + user + '/model/' + modelid + '.txt'
    # with open(path1, 'rb+') as f:
    #     g = open(path2, 'ab+')
    #     g.write(f.read())
    #     g.close()
    kmeans_model(path1, path2)
    return str(modelid)


def dotaskkmeans(user, datafile, taskid):
    time.sleep(15)
    with open(PROJECT_PATH + '/files/' + user + '/train/' + datafile, 'rb+') as f:
        g = open(PROJECT_PATH + '/files/' + user + '/result/' + taskid, 'ab+')
        g.write(f.read())
        g.close()
    return str(taskid)


def kmeans_model(file_path, file_out):
    global SPARK_MASTER
    y = pyspark.SparkConf()
    y.setMaster(SPARK_MASTER)
    # y.setSparkHome('/usr/local/spark')
    print file_path
    print y.getAll()
    sc = pyspark.SparkContext(conf=y)
    # print sc.pythonExec
    # print sc.pythonVer
    textfile = sc.textFile(file_path)
    print textfile.collect()
    print textfile.count()
    y = textfile.map(lambda each: each.split(' ')[1:])
    p = re.compile('\d:')
    z = y.map(lambda x: transform(x, p))
    z = z.map(lambda x: [float(each) for each in x])
    print z.collect()
    model = KMeans.train(z, 2)
    print model.clusterCenters
    # textfile.saveAsTextFile(file_out)
    model.save(sc, file_out)
    sc.stop()
    """
        对输入的kmeans数据文件内容x进行处理，并且使用kmeans分类。
    """


def transform(list_in, p):
    x = []
    for i in range(len(list_in)):
        x.append(p.sub('', list_in[i]))
    return x


if __name__ == '__main__':
    while True:
        print 'start'
        model_id = model_conn.blpop('model')
        print model_id[1]
        domodelspark(model_id[1])
