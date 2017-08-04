# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyUser(c):
    FailFlag = False
    tolog("<b>Verify user </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify user </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyUserList(c):
    FailFlag = False
    tolog("<b>Verify user -a list </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify user -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyUserAdd(c):
    FailFlag = False
    tolog("<b>Verify user -a add </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify user -a add </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyUserMod(c):
    FailFlag = False
    tolog("<b>Verify user -a mod </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify user -a mod </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyUserDel(c):
    FailFlag = False
    tolog("<b>Verify user -a del </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify user -a del </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


def verifyUserInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify user invalid option</b>")
    command = ['user -x', 'user -a list -x', 'user -a mod -x', 'user -a add -x', 'user -a del -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify user invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyUserInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify user invalid parameters</b>")
    command = ['user test', 'user -a list test', 'user -a mod -s test', 'user -a ad -u testuser -p test', 'user -a add -t test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify user invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyUserMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify user missing parameters</b>")
    command = ['user -a ', 'user -a mod -s ', 'user -a add -u testuser -p ', 'user -a add -t ']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify user missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyUser(c)
    verifyUserList(c)
    verifyUserAdd(c)
    verifyUserMod(c)
    verifyUserDel(c)
    verifyUserInvalidOption(c)
    verifyUserInvalidParameters(c)
    verifyUserMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped