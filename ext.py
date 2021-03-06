#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask_mako import MakoTemplates, render_template  # noqa
# from flask_sqlalchemy import SQLAlchemy
import MySQLdb
from multiprocessing import Lock
# from pyspark import SparkContext, SparkConf
import redis


from consts import HOSTNAME, USERNAME, PASSWORD, DATABASE

# conn = redis.Redis()
model_conn = redis.Redis(host='localhost', port=6379)
mako = MakoTemplates()
# db = SQLAlchemy()


def get_con():
    return MySQLdb.connect(HOSTNAME, USERNAME, PASSWORD, DATABASE, charset="utf8")
# lock = Lock()
# cur = con.cursor()
# conf = SparkConf()
# conf.setMaster("local[*]")
# conf.setAppName("SparkWebProject")
# sc = SparkContext(conf=conf)
