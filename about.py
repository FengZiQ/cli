# coding=utf-8

from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn

Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyAbout(c):
    FailFlag = False
    tolog("<b>Verify about</b>")
    result = SendCmd(c, "about")
    if "Version: " not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: about</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify about</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyAboutHelp(c):
    FailFlag = False
    tolog("<b>Verify about -h</b>")
    result = SendCmd(c, "about -h")
    if "Usage" not in result or "Summary" not in result or "about" not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: about -h</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify about -h</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyAboutInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify about Invalid Option</b>")
    command = ['about -x']
    for com in command:
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + '</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify about Invalid Option</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyAboutInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify about Invalid Parameters</b>")
    result = SendCmd(c, "about x")
    if "Error (" not in result or "Invalid setting parameters" not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: about x</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify about Invalid Parameters</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyAbout(c)
    verifyAboutHelp(c)
    verifyAboutInvalidOption(c)
    verifyAboutInvalidParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped