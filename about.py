# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
import random
import  re
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyAbout(c):
    FailFlag = False
    tolog("<b>Verify about</b>")
    result = SendCmd(c, "about")
    if "Version: 12.00.9999.92" not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: about</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify about</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

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

def bvt_verifyAbout(c):
    FailFlag = False
    tolog("Verify about")
    result = SendCmd(c, "about")
    if "Version: " not in result:
        FailFlag = True
        tolog('Fail: about')

    return FailFlag

def bvt_verifyAboutHelp(c):
    FailFlag = False
    tolog("Verify about -h")
    result = SendCmd(c, "about -h")
    if "Usage" not in result or "Summary" not in result or "about" not in result:
        FailFlag = True
        tolog('Fail: about -h')

    return FailFlag

def bvt_verifyAboutInvalidOption(c):
    FailFlag = False
    tolog("Verify about Invalid Option")
    command = ['about -x']
    for com in command:
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid" not in result:
            FailFlag = True
            tolog('Fail: ' + com + '')

    return FailFlag

def bvt_verifyAboutInvalidParameters(c):
    FailFlag = False
    tolog("Verify about Invalid Parameters")
    result = SendCmd(c, "about x")
    if "Error (" not in result or "Invalid setting parameters" not in result:
        FailFlag = True
        tolog('Fail: about x')

    return FailFlag



if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    bvt_verifyAbout(c)
    bvt_verifyAboutHelp(c)
    bvt_verifyAboutInvalidOption(c)
    bvt_verifyAboutInvalidParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped