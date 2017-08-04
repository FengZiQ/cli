# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyPing(c):
    FailFlag = False
    tolog("<b>Verify ping </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ping </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyPingSpecifyInexistentId(c):
    FailFlag = False
    tolog("<b> Verify ping specify inexistent Id </b>")
    # -l <CtrlId> (1,2)
    # -p <port ID> (1,4)


    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ping specify inexistent Id </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


def verifyPingInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify ping invalid option</b>")
    command = ['ping -x', 'ping -t fc -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ping invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyPingInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify ping invalid parameters</b>")
    command = ['ping test', 'ping -t test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ping invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyPingMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify ping missing parameters</b>")
    command = ['ping', 'ping -t ', 'ping -t iscsi -l']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ping missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyPing(c)
    verifyPingSpecifyInexistentId(c)
    verifyPingInvalidOption(c)
    verifyPingInvalidParameters(c)
    verifyPingMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped