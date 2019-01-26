#!/usr/bin/python
# -*- coding:utf-8 -*-

import time

from ext import get_con, model_conn
# from consts import PROJECT_PATH

# LogisticRegression xgboost random-forest
# Kmeans dbscan
# apriori fpgrowth prefixspan

import re
import numpy
import pyspark
from pyspark.mllib.clustering import KMeans

from kmeans import doKmeans, doTaskKmeans
from fpgrowth import doFPGrowth, doTaskFPGrowth
from logisticregression import doLogisticRegression, doTaskLogisticRegression


# SPARK_MASTER = 'spark://dangerous-Lenovo-Product:7077'
SPARK_MASTER = 'spark://blade01:7077'
# SPARK_MASTER就是集群的master的url


def domodelspark(modelid, y):
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
            modelfile = doKmeans(model[0], model[2], modelid, y)
        except:
            flag = 1
    elif model[1] == 'LogisticRegression':
        try:
            modelfile = doLogisticRegression(model[0], model[2], modelid, y)
        except:
            flag = 1
    elif model[1] == 'FPGrowth':
        try:
            modelfile = doFPGrowth(model[0], model[2], modelid, y)
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


def dotaskspark(taskid, y):
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
            modelfile = doTaskKmeans(task[0], task[2], taskid, y)
        except:
            flag = 1
    elif task[1] == 'LogisticRegression':
        try:
            modelfile = doTaskLogisticRegression(task[0], task[2], y)
        except:
            flag = 1
    elif task[1] == 'FPGrowth':
        try:
            modelfile = doTaskFPGrowth(task[0], task[2], y)
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


def transform(list_in, p):
    x = []
    for i in range(len(list_in)):
        x.append(p.sub('', list_in[i]))
    return x


if __name__ == '__main__':
    t = pyspark.SparkConf()
    t.setMaster(SPARK_MASTER)
    print 'start'
    while True:
        print 'waiting'
        model_id = model_conn.blpop('model')
        print model_id[1]
        domodelspark(model_id[1], t)
