# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyRb(c):
    FailFlag = False
    tolog("<b>Verify rb </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rb </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyRbList(c):
    FailFlag = False
    tolog("<b>Verify rb -a list </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rb -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyRbSpecifyInexistentId(c):
    FailFlag = False
    tolog("<b> Verify rb specify inexistent Id </b>")
    # -l <Pool ID> (0,255)

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rb specify inexistent Id </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


def verifyRbInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify rb invalid option</b>")
    command = ['rb -x', 'rb -a list -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rb invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyRbInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify rb invalid parameters</b>")
    command = ['rb test', 'rb -a list test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rb invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyRbMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify rb missing parameters</b>")
    command = ['rb -l ', 'rb -a list -l ']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rb missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyRb(c)
    verifyRbList(c)
    verifyRbSpecifyInexistentId(c)
    verifyRbInvalidOption(c)
    verifyRbInvalidParameters(c)
    verifyRbMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped