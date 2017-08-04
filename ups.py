# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyUps(c):
    FailFlag = False
    tolog("<b>Verify ups </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ups </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyUpsList(c):
    FailFlag = False
    tolog("<b>Verify ups -a list </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ups -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyUpsV(c):
    FailFlag = False
    tolog("<b>Verify ups -a list -v </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ups -a list -v </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyUpsMod(c):
    FailFlag = False
    tolog("<b>Verify ups -a mod </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ups -a mod </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


def verifyUpsInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify ups invalid option</b>")
    command = ['ups -x', 'ups -a list -x', 'ups -a mod -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ups invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyUpsInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify ups invalid parameters</b>")
    command = ['ups test', 'ups -a list test', 'ups -a mod -s test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ups invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyUpsMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify ups missing parameters</b>")
    command = ['ups -a ', 'ups -a mod -s ']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ups missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyUps(c)
    verifyUpsList(c)
    verifyUpsV(c)
    verifyUpsMod(c)
    verifyUpsInvalidOption(c)
    verifyUpsInvalidParameters(c)
    verifyUpsMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped