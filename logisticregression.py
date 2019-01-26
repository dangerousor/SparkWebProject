#!/usr/bin/python
# -*- coding:utf-8 -*-
import pyspark
from pyspark.mllib.classification import LabeledPoint, LogisticRegressionWithLBFGS
import time


def doLogisticRegression(user, datafile, modelid, y):
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
    logistic_model(path1, path2, y)
    return str(modelid)


def doTaskLogisticRegression(user, datafile, taskid):
    time.sleep(15)
    # with open(PROJECT_PATH + '/files/' + user + '/train/' + datafile, 'rb+') as f:
    #     g = open(PROJECT_PATH + '/files/' + user + '/result/' + taskid, 'ab+')
    #     g.write(f.read())
    #     g.close()
    return str(taskid)


def logistic_model(file_path, file_out, co):
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
    y = textfile.map(lambda x: x.encode('utf-8').replace('\n', '').split('\x01')).filter(lambda x: len(x) == 7 and x[0].isdigit() and x[1].isdigit() and x[2].isdigit() and x[3].isdigit() and x[4].isdigit() and x[5].isdigit() and x[6].isdigit())
    # z = y.map(lambda x: [float(x[4])-20150301, float(x[1]), float(x[3])])
    z = y.map(lambda x : [int(each) for each in x])
    print z.take(10)
    # z = z.map(lambda x: LabeledPoint(x[0], x[1:]))
    z = z.map(lambda x: LabeledPoint((lambda t: t - 20150401+31 if t>20150331 else t - 20150301)(x[0]), x[1:]))    
    print z.take(10)
    # print "partition:", z.getNumPartitions()
    # z = z.repartition(100 * int(z.getNumPartitions()))
    model = LogisticRegressionWithLBFGS.train(z, numClasses=61)
    print "done"
    # textfile.saveAsTextFile(file_out)
    model.save(sc, file_out)
    sc.stop()

