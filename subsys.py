# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifySubsys(c):
    FailFlag = False
    tolog("<b>Verify subsys </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify subsys </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySubsysList(c):
    FailFlag = False
    tolog("<b>Verify subsys -a list </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify subsys -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySubsysMod(c):
    FailFlag = False
    tolog("<b>Verify subsys -a mod </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify subsys -a mod </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySubsysLock(c):
    FailFlag = False
    tolog("<b>Verify subsys -a lock </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify subsys -a lock </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySubsysUnlock(c):
    FailFlag = False
    tolog("<b>Verify subsys -a unlock </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify subsys -a unlock </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySubsysChklock(c):
    FailFlag = False
    tolog("<b>Verify subsys -a chklock</b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify subsys -a chklock </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


def verifySubsysInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify subsys invalid option</b>")
    command = ['subsys -x', 'subsys -a list -x', 'subsys -a mod -x',
               'subsys -a lock -x ', 'subsys -a unlock -x', 'subsys -a chklock -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify subsys invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifySubsysInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify subsys invalid parameters</b>")
    command = ['subsys test', 'subsys -a list test', 'subsys -a mod test',
               'subsys -a lock test ', 'subsys -a unlock test', 'subsys -a chklock test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify subsys invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifySubsysMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify subsys missing parameters</b>")
    command = ['subsys -a', 'subsys -a mod -s',
               'subsys -a lock -r', 'subsys -a unlock -f ', 'subsys -a lock -r -t']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify subsys missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifySubsys(c)
    verifySubsysList(c)
    verifySubsysMod(c)
    verifySubsysLock(c)
    verifySubsysUnlock(c)
    verifySubsysChklock(c)
    verifySubsysInvalidOption(c)
    verifySubsysInvalidParameters(c)
    verifySubsysMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped