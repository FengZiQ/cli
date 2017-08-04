# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyRc(c):
    FailFlag = False
    tolog("<b>Verify rc </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rc </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyRcList(c):
    FailFlag = False
    tolog("<b>Verify rc -a list </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rc -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyRcStart(c):
    FailFlag = False
    tolog("<b>Verify rc -a start </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rc -a start </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyRcStop(c):
    FailFlag = False
    tolog("<b>Verify rc -a stop </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rc -a stop </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyRcSpecifyInexistentId(c):
    FailFlag = False
    tolog("<b> Verify rc specify inexistent Id </b>")
    # -l <Pool ID> (0,255)

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rc specify inexistent Id </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


def verifyRcInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify rc invalid option</b>")
    command = ['rc -x', 'rc -a list -x', 'rc -a start -x', 'rc -a stop -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rc invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyRcInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify rc invalid parameters</b>")
    command = ['rc test', 'rc -a list test', 'rc -a start test', 'rc -a stop test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rc invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyRcMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify rc missing parameters</b>")
    command = ['rc -l ', 'rc -a list -l ', 'rc -a start -l ', 'rc -a stop -l']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rc missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyRc(c)
    verifyRcList(c)
    verifyRcStart(c)
    verifyRcStop(c)
    verifyRcSpecifyInexistentId(c)
    verifyRcInvalidOption(c)
    verifyRcInvalidParameters(c)
    verifyRcMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped