#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask_mako import MakoTemplates, render_template  # noqa
# from flask_sqlalchemy import SQLAlchemy
import MySQLdb
from multiprocessing import Lock
# from pyspark import SparkContext, SparkConf
# import redis


from consts import HOSTNAME, USERNAME, PASSWORD, DATABASE

# conn = redis.Redis()
mako = MakoTemplates()
# db = SQLAlchemy()
con = MySQLdb.connect(HOSTNAME, USERNAME, PASSWORD, DATABASE, charset="utf8")
lock = Lock()
# conf = SparkConf()
# conf.setMaster("local[*]")
# conf.setAppName("SparkWebProject")
# sc = SparkContext(conf=conf)
