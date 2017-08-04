# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyStats(c):
    FailFlag = False
    tolog("<b>Verify stats </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify stats </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyStatsList(c):
    FailFlag = False
    tolog("<b>Verify stats -a list </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify stats -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyStatsClear(c):
    FailFlag = False
    tolog("<b>Verify stats -a clear </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify stats -a clear </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyStatsSpecifyInexistentId(c):
    FailFlag = False
    tolog("<b> Verify stats specify inexistent Id </b>")
    # -i <devId> ( pd 0,512) (ctrl 1,2)

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify stats specify inexistent Id </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


def verifyStatsInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify stats invalid option</b>")
    command = ['stats -x', 'stats -a list -x', 'stats -a clear -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify stats invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyStatsInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify stats invalid parameters</b>")
    command = ['stats test', 'stats -a list test', 'stats -a clear test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify stats invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyStatsMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify stats missing parameters</b>")
    command = ['stats -a ', 'stats -a list -t ', 'stats -t ctrl -i ']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify stats missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyStats(c)
    verifyStatsList(c)
    verifyStatsClear(c)
    verifyStatsSpecifyInexistentId(c)
    verifyStatsInvalidOption(c)
    verifyStatsInvalidParameters(c)
    verifyStatsMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped