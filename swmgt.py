# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifySwmgt(c):
    FailFlag = False
    tolog("<b>Verify swmgt </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify swmgt </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySwmgtList(c):
    FailFlag = False
    tolog("<b>Verify swmgt -a list </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify swmgt -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySwmgtStart(c):
    FailFlag = False
    tolog("<b>Verify swmgt -a start </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify swmgt -a start </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySwmgtStop(c):
    FailFlag = False
    tolog("<b>Verify swmgt -a stop </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify swmgt -a stop </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySwmgtMod(c):
    FailFlag = False
    tolog("<b>Verify swmgt -a mod </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify swmgt -a mod </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySwmgtAdd(c):
    FailFlag = False
    tolog("<b>Verify swmgt -a add</b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify swmgt -a add </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySwmgtDel(c):
    FailFlag = False
    tolog("<b>Verify swmgt -a del</b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify swmgt -a del </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySwmgtInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify swmgt invalid option</b>")
    command = ['swmgt -x', 'swmgt -a list -x', 'swmgt -a mod -x',
               'swmgt -a start -x ', 'swmgt -a stop -x', 'swmgt -a add -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify swmgt invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifySwmgtInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify swmgt invalid parameters</b>")
    command = ['swmgt test', 'swmgt -a list test', 'swmgt -a mod -n test',
               'swmgt -a start -n test ', 'swmgt -a stop -n test', 'swmgt -a add -n ssh -p test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify swmgt invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifySwmgtMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify swmgt missing parameters</b>")
    command = ['swmgt -a', 'swmgt -n ','swmgt -a start -n ', 'swmgt -a stop -n', 'swmgt -a mod -n snmp -t', 'swmgt -a del -n ']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify swmgt missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifySwmgt(c)
    verifySwmgtList(c)
    verifySwmgtStart(c)
    verifySwmgtStop(c)
    verifySwmgtMod(c)
    verifySwmgtAdd(c)
    verifySwmgtDel(c)
    verifySwmgtInvalidOption(c)
    verifySwmgtInvalidParameters(c)
    verifySwmgtMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped