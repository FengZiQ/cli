
# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
import random
import  re
Pass = "'result': 'p'"
Fail = "'result': 'f'"
# find information about different pd
def PDInfo(c,n):
    result = SendCmd(c, "phydrv")
    num = 4
    info = []
    while result.split("\r\n")[num] != 'administrator@cli> ':
        row = result.split("\r\n")[num]
        info.append(row.split()[n])
        num = num + 1
    return info
def verifyRcache(c):
    FailFlag = False
    tolog("<b>Verify rcache </b>")
    configStatus = PDInfo(c,-1)
    if configStatus.count('ReadCache') > 0:
        tolog('')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rcache </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyRcacheList(c):
    FailFlag = False
    tolog("<b>Verify rcache -a list</b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rcache -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyRcacheAdd(c):
    FailFlag = False
    tolog("<b>Verify rcache -a add</b>")
def verifyRcacheDel(c):
    FailFlag = False
    tolog("<b>Verify rcache -a add</b>")

def verifyRcacheSpecifyInexistentId(c):
    FailFlag = False
    tolog("<b> Verify rcache specify inexistent Id </b>")
    command1 = ['rcache -a add -p 512', 'rcache -a del -p 512']
    command2 = ['rcache -a add -p 513', 'rcache -a del -p 513']
    # verify max pd id
    result = SendCmd(c, command1[0])
    if 'Invalid physical drive id' not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: ' + command1[0] + '</font>')
    result = SendCmd(c, command1[1])
    if 'Fail to delete Read Cache' not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: ' + command1[1] + '</font>')
    # verify the pd id that exceeds the max
    for com in command2:
        result = SendCmd(c, com)
        if "invalid setting 513" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + '</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rcache specify inexistent Id </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyRcacheInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify rcache invalid option</b>")
    command = ['rcache -x', 'rcache -a list -x', 'rcache -a add -x', 'rcache -a del -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rcache invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyRcacheInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify rcache invalid parameters</b>")
    command = ['rcache test', 'rcache -a test', 'rcache -a add -p test', 'rcache -a del -p test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rcache invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyRcacheMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify rcache missing parameters</b>")
    command = ['rcache -a ', 'rcache -a add -p', 'rcache -a del -p']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rcache missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    # verifyRcache(c)
    # verifyRcacheList(c)
    # verifyRcacheAdd(c)
    # verifyRcacheDel(c)
    verifyRcacheSpecifyInexistentId(c)
    # verifyRcacheInvalidOption(c)
    # verifyRcacheInvalidParameters(c)
    # verifyRcacheMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped