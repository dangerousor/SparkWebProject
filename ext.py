#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask_mako import MakoTemplates, render_template  # noqa
from flask_sqlalchemy import SQLAlchemy
import MySQLdb

from consts import HOSTNAME, USERNAME, PASSWORD, DATABASE


mako = MakoTemplates()
db = SQLAlchemy()
con = MySQLdb.connect(HOSTNAME, USERNAME, PASSWORD, DATABASE, charset="utf8")
