#!/usr/bin/python
# -*- coding:utf-8 -*-

import re
import pyspark
from pyspark.mllib.clustering import KMeans

# from consts import SPARK_MASTER

SPARK_MASTER = 'spark://dangerous-Lenovo-Product:7077'
# SPARK_MASTER就是集群的master的url


def kmeans_model(file_path, file_out):
    y = pyspark.SparkConf()
    y.setMaster(SPARK_MASTER)
    # y.setSparkHome('/usr/local/spark')
    sc = pyspark.SparkContext(conf=y)
    textfile = sc.textFile(file_path)
    print textfile.collect()
    print textfile.count()
    y = textfile.map(lambda each: each.split(' ')[1:])
    p = re.compile('\d:')
    z = y.map(lambda x: transform(x, p))
    print z
    model = KMeans.train(z, 2)
    print model.centers()
    # textfile.saveAsTextFile(file_out)
    model.save(sc, file_out)
    """
        对输入的kmeans数据文件内容x进行处理，并且使用kmeans分类。
    """


def transform(list_in, p):
    x = []
    for i in range(len(list_in)):
        x.append(p.sub('', list_in[i]))
    return x


if __name__ == '__main__':
    file_p = 'file:///home/dangerous/PycharmProjects/SparkWebProject/files/24/train/sample_kmeans_data.txt'
    file_o = 'file:///home/dangerous/PycharmProjects/test'
    # 这里的路径是hdfs上的路径
    kmeans_model(file_p, file_o)
