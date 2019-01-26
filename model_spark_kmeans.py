#!/usr/bin/python
# -*- coding:utf-8 -*-

import pyspark

# from consts import SPARK_MASTER

SPARK_MASTER = 'spark://dangerous-Lenovo-Product:7077'
# SPARK_MASTER就是集群的master的url


def kmeans_model(file_path):
    y = pyspark.SparkConf()
    y.setMaster(SPARK_MASTER)
    # y.setSparkHome('/usr/local/spark')
    sc = pyspark.SparkContext(conf=y)
    x = sc.textFile(file_path)
    #
    #
    # 对输入的kmeans数据文件内容x进行处理，并且使用kmeans分类。
    #
    #
    # 
    print x.count()
    print x.first()


if __name__ == '__main__':
    file_p = 'hdfs://localhost:9000/user/dangerous/my_libsvm_test.txt'
    # 这里的路径是hdfs上的路径
    kmeans_model(file_p)