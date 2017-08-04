# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifySpareAdd(c):
    FailFlag = False
    tolog("<b>Verify spare -a add </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify spare -a add </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySpare(c):
    FailFlag = False
    tolog("<b>Verify spare </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify spare </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySpareList(c):
    FailFlag = False
    tolog("<b>Verify spare -a list </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify spare -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySpareDel(c):
    FailFlag = False
    tolog("<b>Verify spare -a del </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify spare -a del </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySpareSpecifyInexistentId(c):
    FailFlag = False
    tolog("<b> Verify spare specify inexistent Id </b>")
    # -p <PD ID> (0,512)
    # -d <POOL ID or POOL ID List>  (0, 255)

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify spare specify inexistent Id </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


def verifySpareInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify spare invalid option</b>")
    command = ['spare -x', 'spare -a list -x', 'spare -a add -x', 'spare -a del -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify spare invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifySpareInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify spare invalid parameters</b>")
    command = ['spare test', 'spare -a list test', 'spare -a add test', 'spare -a del test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify spare invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifySpareMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify spare missing parameters</b>")
    command = ['spare -d ', 'spare -a list -d ', 'spare -a add -p ', 'spare -a del -p']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify spare missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifySpareAdd(c)
    verifySpare(c)
    verifySpareList(c)
    verifySpareDel(c)
    verifySpareSpecifyInexistentId(c)
    verifySpareInvalidOption(c)
    verifySpareInvalidParameters(c)
    verifySpareMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped