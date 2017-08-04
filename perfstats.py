# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyPerfstatsStart(c):
    FailFlag = False
    tolog("<b>Verify perfstats -a start </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify perfstats -a start </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyPerfstats(c):
    FailFlag = False
    tolog("<b>Verify perfstats </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify perfstats </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyPerfstatsList(c):
    FailFlag = False
    tolog("<b>Verify perfstats -a list </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify perfstats -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyPerfstatsInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify perfstats invalid option</b>")
    command = ['perfstats -x', 'perfstats -a list -x', 'perfstats -a start -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify perfstats invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyPerfstatsInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify perfstats invalid parameters</b>")
    command = ['perfstats test', 'perfstats -a test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify perfstats invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyPerfstatsMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify perfstats missing parameters</b>")
    command = ['perfstats -a ', 'perfstats -a list -t']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify perfstats missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyPerfstatsStart(c)
    verifyPerfstats(c)
    verifyPerfstatsList(c)
    verifyPerfstatsInvalidOption(c)
    verifyPerfstatsInvalidParameters(c)
    verifyPerfstatsMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped