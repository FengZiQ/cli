# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyChangePassword(c):
    FailFlag = False
    tolog('\n<font color="red"> Need to manually test </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify change password </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyPasswordSpecifyInexistentUsername(c):
    FailFlag = False
    tolog("<b> Verify password specify inexistent username </b>")
    result = SendCmd(c, 'password -u inexistentusername')
    if 'Username not found'not in result:
        FailFlag =True
        tolog('\n<font color="red">Fail: password -u inexistentusername </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify password specify inexistent username </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyPasswordInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify password invalid option</b>")
    command = ['password -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify password invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyPasswordInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify password invalid parameters</b>")
    command = ['password test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify password invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyPasswordMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify password missing parameters</b>")
    command = ['password -u ', 'password -u snmpuser -t', 'password -u snmpuser -t snmp -p']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify password missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)



def bvt_verifyChangePassword(c):
    FailFlag = False
    tolog('\n Need to manually test ')

    return FailFlag

def bvt_verifyPasswordSpecifyInexistentUsername(c):
    FailFlag = False
    tolog(" Verify password specify inexistent username ")
    result = SendCmd(c, 'password -u inexistentusername')
    if 'Username not found'not in result:
        FailFlag =True
        tolog('Fail: password -u inexistentusername ')

    return FailFlag

def bvt_verifyPasswordInvalidOption(c):
    FailFlag = False
    tolog("Verify password invalid option")
    command = ['password -x']
    for com in command:
        tolog(' Verify ' + com )
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('Fail: ' + com )

    return FailFlag

def bvt_verifyPasswordInvalidParameters(c):
    FailFlag = False
    tolog("Verify password invalid parameters")
    command = ['password test']
    for com in command:
        tolog(' Verify ' + com )
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('Fail: ' + com )

    return FailFlag

def bvt_verifyPasswordMissingParameters(c):
    FailFlag = False
    tolog("Verify password missing parameters")
    command = ['password -u ', 'password -u snmpuser -t', 'password -u snmpuser -t snmp -p']
    for com in command:
        tolog(' Verify ' + com )
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('Fail: ' + com )

    return FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    bvt_verifyChangePassword(c)
    bvt_verifyPasswordSpecifyInexistentUsername(c)
    bvt_verifyPasswordInvalidOption(c)
    bvt_verifyPasswordInvalidParameters(c)
    bvt_verifyPasswordMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped