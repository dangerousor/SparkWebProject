#!/usr/bin/python
# -*- coding:utf-8 -*-
import pyspark
from pyspark.mllib.clustering import KMeans
import time


def doKmeans(user, datafile, modelid, y):
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


def doTaskKmeans(user, datafile, taskid):
    time.sleep(15)
    # with open(PROJECT_PATH + '/files/' + user + '/train/' + datafile, 'rb+') as f:
    #     g = open(PROJECT_PATH + '/files/' + user + '/result/' + taskid, 'ab+')
    #     g.write(f.read())
    #     g.close()
    return str(taskid)


def kmeans_model(file_path, file_out, co):
    # global SPARK_MASTER
    # y = pyspark.SparkConf()
    # y.setMaster(SPARK_MASTER)
    # y.setSparkHome('/usr/local/spark')
    # print file_path
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
    model.save(sc, file_out)
    sc.stop()
    """
        对输入的kmeans数据文件内容x进行处理，并且使用kmeans分类。
    """
