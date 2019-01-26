#!/usr/bin/python
# -*- coding:utf-8 -*-

# from ext import cur
#
#
# cur.execute('select * from model')
# res = cur.fetchone()
# print res


# import re
#
# x = [u'0 1:0.0 2:0.0 3:0.0', u'1 1:0.1 2:0.1 3:0.1', u'2 1:0.2 2:0.2 3:0.2', u'3 1:9.0 2:9.0 3:9.0', u'4 1:9.1 2:9.1 3:9.1', u'5 1:9.2 2:9.2 3:9.2']
#
# y = map(lambda each: each.split(' ')[1:], x)
# print y
# p = re.compile('\d:')
# for i in range(len(y)):
#     for j in range(len(y[i])):
#         y[i][j] = p.sub('', y[i][j])
# print y
