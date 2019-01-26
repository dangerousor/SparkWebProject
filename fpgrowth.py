#!/usr/bin/python
# -*- coding:utf-8 -*-
import pyspark
from pyspark.mllib.fpm import FPGrowth
import time


def doFPGrowth(user, datafile, modelid, y):
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
    fpgrowth_model(path1, path2, y)
    return str(modelid)


def doTaskFPGrowth(user, datafile, taskid):
    time.sleep(15)
    # with open(PROJECT_PATH + '/files/' + user + '/train/' + datafile, 'rb+') as f:
    #     g = open(PROJECT_PATH + '/files/' + user + '/result/' + taskid, 'ab+')
    #     g.write(f.read())
    #     g.close()
    return str(taskid)


def fpgrowth_model(file_path, file_out, co):
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
    y = textfile.map(lambda x: set(x.encode('utf-8').replace('\n', '').split('\x01')))
    # print "partition:", z.getNumPartitions()
    # z = z.repartition(100 * int(z.getNumPartitions()))
    model = FPGrowth.train(y, 0.01, y.getNumPartitions())
    print sorted(model.freqItemsets().collect())
    # textfile.saveAsTextFile(file_out)
    model.save(sc, file_out)
    sc.stop()
