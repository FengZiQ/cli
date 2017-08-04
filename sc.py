# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifySc(c):
    FailFlag = False
    tolog("<b>Verify sc </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify sc </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyScList(c):
    FailFlag = False
    tolog("<b>Verify sc -a list </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify sc -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyScStart(c):
    FailFlag = False
    tolog("<b>Verify sc -a start </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify sc -a start </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyScSpecifyInexistentId(c):
    FailFlag = False
    tolog("<b> Verify sc specify inexistent Id </b>")
    # -i <Spare ID> (0,255)

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify sc specify inexistent Id </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


def verifyScInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify sc invalid option</b>")
    command = ['sc -x', 'sc -a list -x', 'sc -a start -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify sc invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyScInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify sc invalid parameters</b>")
    command = ['sc test', 'sc -a list test', 'sc -a start test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify sc invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyScMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify sc missing parameters</b>")
    command = ['sc -i ', 'sc -a list -i ', 'sc -a start -i ']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify sc missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifySc(c)
    verifyScList(c)
    verifyScStart(c)
    verifyScSpecifyInexistentId(c)
    verifyScInvalidOption(c)
    verifyScInvalidParameters(c)
    verifyScMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped