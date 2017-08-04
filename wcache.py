# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"
# find information about different pd
def PDInfo(n):
    result = SendCmd(c, "phydrv")
    num = 4
    info = []
    while result.split("\r\n")[num] != 'administrator@cli> ':
        row = result.split("\r\n")[num]
        info.append(row.split()[n])
        num = num + 1
    return info

def verifyWcache(c):
    FailFlag = False
    tolog("<b>Verify wcache </b>")


    if FailFlag:
        tolog('\n<font color="red">Fail: Verify wcache </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyWcacheList(c):
    FailFlag = False
    tolog("<b>Verify wcache -a list</b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify wcache -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyWcacheAdd(c):
    FailFlag = False
    tolog("<b>Verify wcache -a add</b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify wcache -a add </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyWcacheMod(c):
    FailFlag = False
    tolog("<b>Verify wcache -a mod</b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify wcache -a mod </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyWcacheDel(c):
    FailFlag = False
    tolog("<b>Verify wcache -a del</b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify wcache -a del</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


def verifyWcacheSpecifyInexistentId(c):
    FailFlag = False
    tolog("<b> Verify wcache specify inexistent Id </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify wcache specify inexistent Id </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyWcacheInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify wcache invalid option</b>")
    command = ['wcache -x', 'wcache -a list -x', 'wcache -a add -x', 'wcache -a mod -x', 'wcache -a del -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify wcache invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyWcacheInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify wcache invalid parameters</b>")
    command = ['wcache test', 'wcache -a test', 'wcache -a add -p test', 'wcache -a mod -i test', 'wcache -a del -p test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify wcache invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyWcacheMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify wcache missing parameters</b>")
    command = ['wcache -a', 'wcache -a add -p', 'wcache -a mod -i' 'wcache -a del -p']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify wcache missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyWcache(c)
    verifyWcacheList(c)
    verifyWcacheAdd(c)
    verifyWcacheMod(c)
    verifyWcacheDel(c)
    verifyWcacheSpecifyInexistentId(c)
    verifyWcacheInvalidOption(c)
    verifyWcacheInvalidParameters(c)
    verifyWcacheMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped