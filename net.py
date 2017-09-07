# coding=utf-8

from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn

Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyNet(c):
    FailFlag = False
    tolog("<b>Verify net </b>")

    result = SendCmd(c, 'net')

    if 'Error (' in result or 'IPv4' not in result or 'IPv6' not in result:
        FailFlag = True
        tolog('<font color="red">Fail: net </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify net </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyNetList(c):
    FailFlag = False
    tolog("<b>Verify net -a list </b>")

    result = SendCmd(c, 'net -a list')

    if 'Error (' in result or 'IPv4' not in result or 'IPv6' not in result:
        FailFlag = True
        tolog('<font color="red">Fail: net -a list </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify net -a list</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyNetMod(c):
    FailFlag = False
    tolog("<b>Verify net -a mod</b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify net -a mod </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyNetEnable(c):
    FailFlag = False
    tolog("<b>Verify net -a enable</b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify net -a enable </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyNetDisable(c):
    FailFlag = False
    tolog("<b>Verify net -a disable</b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify net -a disable </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyNetSpecifyInexistentId(c):
    FailFlag = False
    tolog("<b> Verify net specify inexistent Id </b>")
    # -c <ctrl ID>
    # -p <portal ID>


    if FailFlag:
        tolog('\n<font color="red">Fail: Verify net specify inexistent Id </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyNetInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify net invalid option</b>")

    command = [
        'net -x',
        'net -a list -x',
        'net -a mod -x',
        'net -a enable -x',
        'net -a disable -x'
    ]

    for com in command:
        tolog('<b> Verify ' + com + '</b>')

        result = SendCmd(c, com)

        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify net invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyNetInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify net invalid parameters</b>")

    command = [
        'net test',
        'net -a list test',
        'net -a mod test',
        'net -a enable test',
        'net -a disable test'
    ]

    for com in command:
        tolog('<b> Verify ' + com + '</b>')

        result = SendCmd(c, com)

        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify net invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyNetMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify net missing parameters</b>")

    command = [
        'net -a enable -f',
        'net -a disable -f',
        'net -a mod -m',
        'net -a mod -f'
    ]

    for com in command:
        tolog('<b> Verify ' + com + '</b>')

        result = SendCmd(c, com)

        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify net missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyNet(c)
    verifyNetList(c)
    verifyNetMod(c)
    verifyNetEnable(c)
    verifyNetDisable(c)
    verifyNetSpecifyInexistentId(c)
    verifyNetInvalidOption(c)
    verifyNetInvalidParameters(c)
    verifyNetMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped