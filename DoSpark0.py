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
            modelfile = dokmeans(model[0], model[2], modelid, y)
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
            modelfile = dotaskkmeans(task[0], task[2], taskid, y)
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


def dokmeans(user, datafile, modelid, y):
    # textfile = sc.textFile("file://files/" + user + "/train/" + datafile)
    # print textfile.collect()
    # textfile.saveAsTextFile("file://files/" + user + "/model/" + modelid)
    # time.sleep(15)
    # path1 = 'file://' + PROJECT_PATH + '/files/' + user + '/train/' + datafile
    path1 = 'hdfs://blade01:9000' + '/user/hadoop' + '/files/' + user + '/train/' + datafile
    path2 = 'hdfs://blade01:9000/user/hadoop/files/' + user + '/model/' + modelid
    print datafile
    if datafile == 'tbdata':
        path1 = 'hdfs://blade01:9000/user/hadoop/tbdata'
    if datafile == 'totaldata':
        path1 = 'hdfs://blade01:9000/user/hadoop/totaldata'
    # with open(path1, 'rb+') as f:
    #     g = open(path2, 'ab+')
    #     g.write(f.read())
    #     g.close()
    kmeans_model(path1, path2, y)
    return str(modelid)


def dotaskkmeans(user, datafile, taskid):
    time.sleep(15)
    with open(PROJECT_PATH + '/files/' + user + '/train/' + datafile, 'rb+') as f:
        g = open(PROJECT_PATH + '/files/' + user + '/result/' + taskid, 'ab+')
        g.write(f.read())
        g.close()
    return str(taskid)


def kmeans_model(file_path, file_out, co):
    # global SPARK_MASTER
    # y = pyspark.SparkConf()
    # y.setMaster(SPARK_MASTER)
    # y.setSparkHome('/usr/local/spark')
    print file_path
    # print y.getAll()
    sc = pyspark.SparkContext(conf=co)
    # print sc.pythonExec
    # print sc.pythonVer
    textfile = sc.textFile(file_path)
    # print textfile.collect()
    # print textfile.count()
    # y = textfile.map(lambda each: each.split(' ')[1:])
    # p = re.compile('\d:')
    # z = y.map(lambda x: transform(x, p))
    # z = z.map(lambda x: [float(each) for each in x])
    # print z.collect()
    y = textfile.map(lambda x: x.encode('utf-8').replace('\n', '').split('\x01')).filter(lambda x: len(x)==7 and x[0].isdigit() and x[1].isdigit() and x[2].isdigit() and x[3].isdigit() and x[4].isdigit() and x[5].isdigit() and x[6].isdigit())
    z = y.map(lambda x: [int(each) for each in x])
    # print "partition:", z.getNumPartitions()
    # z = z.repartition(100 * int(z.getNumPartitions()))
    model = KMeans.train(z, 8)
    print [[int(every) for every in list(each)] for each in model.clusterCenters]
    # textfile.saveAsTextFile(file_out)
    # model.save(sc, file_out)
    print "done"
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
    t = pyspark.SparkConf()
    t.setMaster(SPARK_MASTER)
    print 'start'
    while True:
        print 'waiting'
        model_id = model_conn.blpop('model')
        print model_id[1]
        domodelspark(model_id[1], t)

    # from pyspark.mllib.classification import LabeledPoint
    # import numpy as np
    # from pyspark.mllib.classification import LogisticRegressionWithSGD
    # from pyspark.mllib.classification import LogisticRegressionWithLBFGS
    # import time
    #
    # rdd = sc.textFile("tbdata").map(lambda row: [row.split('\x01')[1], row.split('\x01')[3], row.split('\x01')[4]])
    # station = []
    #
    #
    # def filter_out(sta):
    #     return (float(sta[0]) / 10000 >= 5) and ((sta[1] in station)) and (sta[2] in station)
    #
    #
    # f = open("/home/hadoop/datasetCardRecord/data/tbl_edw_dpa_dim_line_station/000000_0")
    # for line in f:
    #     station += [(line.split('\x01')[2])]
    # f.close()
    # reasonrdd = rdd.filter(filter_out)
    #
    # timema = np.identity(19)
    # stopma = np.identity(15)
    # reasonrdd2 = reasonrdd.map(lambda line: [int(line[0]) / 10000, int(line[1]) / 100, int(line[2]) / 100])
    #
    #
    # def mapfunct(line):
    #     instop = line[1]
    #     if (instop == 16):
    #         instop = 14
    #     if (instop == 22):
    #         instop = 15
    #     feature = np.hstack((timema[line[0] - 5], stopma[instop - 1]))
    #     label = line[2]
    #     if (line[2] == 16):
    #         label = 14
    #     if (line[2] == 22):
    #         label = 15
    #     return LabeledPoint(label - 1, feature)
    #
    #
    # reasonrdd3 = reasonrdd2.map(mapfunct)
    # reasonrdd3.persist()
    # reasonrdd3.first()
    # start_time = time.time()
    # lrm = LogisticRegressionWithLBFGS.train(reasonrdd3, iterations=10, numClasses=15)
    # print ('used ' + str(time.time() - start_time) + ' seconds')
