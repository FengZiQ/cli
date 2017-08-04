# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyTrunk(c):
    FailFlag = False
    tolog("<b>Verify trunk </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify trunk </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyTrunkList(c):
    FailFlag = False
    tolog("<b>Verify trunk -a list </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify trunk -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyTrunkAdd(c):
    FailFlag = False
    tolog("<b>Verify trunk -a add </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify trunk -a add </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyTrunkMod(c):
    FailFlag = False
    tolog("<b>Verify trunk -a mod </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify trunk -a mod </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyTrunkDel(c):
    FailFlag = False
    tolog("<b>Verify trunk -a del </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify trunk -a del </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyTrunkSpecifyInexistentId(c):
    FailFlag = False
    tolog("<b> Verify trunk specify inexistent Id </b>")
    # -i [<trunk id>]  (1,8)

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify trunk specify inexistent Id </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


def verifyTrunkInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify trunk invalid option</b>")
    command = ['trunk -x', 'trunk -a list -x', 'trunk -a add -x', 'trunk -a mod -x', 'trunk -a del -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify trunk invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyTrunkInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify trunk invalid parameters</b>")
    command = ['trunk test', 'trunk -a list test', 'trunk -a add -s test', 'trunk -a mod -s test', 'trunk -a del -i test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify trunk invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyTrunkMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify trunk missing parameters</b>")
    command = ['trunk -a ', 'trunk -a add -s ', 'trunk -a mod -s ', 'trunk -a del -i ']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify trunk missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyTrunk(c)
    verifyTrunkList(c)
    verifyTrunkAdd(c)
    verifyTrunkMod(c)
    verifyTrunkDel(c)
    verifyTrunkSpecifyInexistentId(c)
    verifyTrunkInvalidOption(c)
    verifyTrunkInvalidParameters(c)
    verifyTrunkMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped