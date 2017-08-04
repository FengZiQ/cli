# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifySync(c):
    FailFlag = False
    tolog("<b>Verify sync </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify sync </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySyncList(c):
    FailFlag = False
    tolog("<b>Verify sync -a list </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify sync -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySyncSpecifyInexistentId(c):
    FailFlag = False
    tolog("<b> Verify sync specify inexistent Id </b>")
    # -l <Pool ID>(0,255)

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify sync specify inexistent Id </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


def verifySyncInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify sync invalid option</b>")
    command = ['sync -x', 'sync -a list -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify sync invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifySyncInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify sync invalid parameters</b>")
    command = ['sync test', 'sync -a list test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify sync invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifySyncMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify sync missing parameters</b>")
    command = ['sync -l ', 'sync -a list -l ']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify sync missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifySync(c)
    verifySyncList(c)
    verifySyncSpecifyInexistentId(c)
    verifySyncInvalidOption(c)
    verifySyncInvalidParameters(c)
    verifySyncMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped