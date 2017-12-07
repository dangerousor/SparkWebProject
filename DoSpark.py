#!/usr/bin/python
# -*- coding:utf-8 -*-

import time

from ext import cur, lock
from consts import PROJECT_PATH


def domodelspark(modelid):
    lock.acquire()
    sql = 'select user,modelname,dataname from model where id = ' + modelid
    cur.execute(sql)
    model = cur.fetchone()
    if model is None:
        lock.release()
        return
    else:
        pass
    flag = 0
    if model[1] == 'KMeans':
        try:
            modelfile = dokmeans(model[0], model[2], modelid)
        except:
            flag = 1
    else:
        pass
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    if flag == 0:
        cur.execute('update model set status = ' + '1' + ', endtime = ' + '"' + now + '", modelfile = "' + modelfile + '" where id = ' + modelid)
    else:
        cur.execute('update model set status = ' + '2' + ', endtime = ' + '"' + now + '" where id = ' + modelid)
    lock.release()
    return 0


def dotaskspark(taskid):
    lock.acquire()
    flag = 0
    sql = 'select user,modelname,testfile, modelfile from task where id = ' + taskid
    cur.execute(sql)
    task = cur.fetchone()
    if task is None:
        lock.release()
        return
    else:
        pass
    if task[1] == 'KMeans':
        try:
            modelfile = dotaskkmeans(task[0], task[2], taskid)
        except:
            flag = 1
    else:
        pass
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    if flag == 0:
        cur.execute('update task set status = ' + '1' + ', endtime = ' + '"' + now + '", resultfile = "' + modelfile + '" where id = ' + taskid)
    else:
        cur.execute('update task set status = ' + '2' + ', endtime = ' + '"' + now + '" where id = ' + taskid)
    lock.release()
    return 0


def dokmeans(user, datafile, modelid):
    # textfile = sc.textFile("file://files/" + user + "/train/" + datafile)
    # print textfile.collect()
    # textfile.saveAsTextFile("file://files/" + user + "/model/" + modelid)
    time.sleep(15)
    path1 = PROJECT_PATH + '/files/' + user + '/train/' + datafile
    path2 = PROJECT_PATH + '/files/' + user + '/model/' + modelid
    with open(path1, 'rb+') as f:
        g = open(path2, 'ab+')
        g.write(f.read())
        g.close()
    return str(modelid)


def dotaskkmeans(user, datafile, taskid):
    time.sleep(15)
    with open(PROJECT_PATH + '/files/' + user + '/train/' + datafile, 'rb+') as f:
        g = open(PROJECT_PATH + '/files/' + user + '/result/' + taskid, 'ab+')
        g.write(f.read())
        g.close()
    return str(taskid)
