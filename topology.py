# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyTopology(c):
    FailFlag = False
    tolog("<b>Verify topology </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify topology </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyTopologyList(c):
    FailFlag = False
    tolog("<b>Verify topology -a list </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify topology -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyTopologyV(c):
    FailFlag = False
    tolog("<b>Verify topology -a list -v</b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify topology -a list -v </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySyncInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify topology invalid option</b>")
    command = ['topology -x', 'topology -a list -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify topology invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifySyncInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify topology invalid parameters</b>")
    command = ['topology test', 'topology -a list test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify topology invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifySyncMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify topology missing parameters</b>")
    command = ['topology -a ']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify topology missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyTopology(c)
    verifyTopologyList(c)
    verifyTopologyV(c)
    verifySyncInvalidOption(c)
    verifySyncInvalidParameters(c)
    verifySyncMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped