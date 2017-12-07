#!/usr/bin/python
# -*- coding:utf-8 -*-

import time

from ext import con, lock


def domodelspark(modelid):
    lock.acquire()
    with con as cur:
        sql = 'select user,modelname,dataname from model where id = ' + modelid
        cur.execute(sql)
        model = cur.fetchone()
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
    with con as cur:
        sql = 'select user,modelname,testfile, modelfile from task where id = ' + taskid
        cur.execute(sql)
        model = cur.fetchone()
        if model[1] == 'KMeans':
            try:
                modelfile = dotaskkmeans(model[0], model[2], taskid)
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
    print './files/' + user + '/train/' + datafile
    # with open('./files/' + user + '/train/' + datafile, 'rb+') as f:
    #     g = open('./files/' + user + '/model/' + datafile, 'ab+')
    #     g.write(f.read())
    #     g.close()
    return str(modelid)


def dotaskkmeans(user, datafile, taskid):
    time.sleep(15)
    print 'files/' + user + '/result/' + taskid
    return str(taskid)
