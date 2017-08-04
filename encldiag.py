# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyEncldiag(c):
    FailFlag = False
    tolog("<b>Verify encldiag </b>")
    result = SendCmd(c, 'encldiag')
    checkPoint = ['EnclosureId             PSUId             Type              Wattage',
                  'EnclosureId                 Type                   PowerOnTime']
    if checkPoint[0] not in result or checkPoint[1] not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: encldiag  </font>')
    command = ['encldiag -t all', 'encldiag -e 1 -t all',
               'encldiag -t psu', 'encldiag -e 1 -t psu',
               'encldiag -t powerontime', 'encldiag -e 1 -t powerontime']
    for com in command[0:2]:
        tolog('<b>Verify ' + com + ' </b>')
        result = SendCmd(c, com)
        if "Error (" in result or checkPoint[0] not in result or checkPoint[1] not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    for com in command[2:4]:
        tolog('<b>Verify ' + com + ' </b>')
        result = SendCmd(c, com)
        if "Error (" in result or checkPoint[0] not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    for com in command[4:6]:
        tolog('<b>Verify ' + com + ' </b>')
        result = SendCmd(c, com)
        if "Error (" in result or checkPoint[1] not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify encldiag  </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyEncldiagList(c):
    FailFlag = False
    tolog("<b>Verify encldiag -a list</b>")
    result = SendCmd(c, 'encldiag -a list')
    checkPoint = ['EnclosureId             PSUId             Type              Wattage',
                  'EnclosureId                 Type                   PowerOnTime']
    if checkPoint[0] not in result or checkPoint[1] not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: encldiag -a list </font>')
    command = ['encldiag -a list -t all', 'encldiag -a list -e 1 -t all',
               'encldiag -a list -t psu', 'encldiag -a list -e 1 -t psu',
               'encldiag -a list -t powerontime', 'encldiag -a list -e 1 -t powerontime']
    for com in command[0:2]:
        tolog('<b>Verify ' + com + ' </b>')
        result = SendCmd(c, com)
        if "Error (" in result or checkPoint[0] not in result or checkPoint[1] not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    for com in command[2:4]:
        tolog('<b>Verify ' + com + ' </b>')
        result = SendCmd(c, com)
        if "Error (" in result or checkPoint[0] not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    for com in command[4:6]:
        tolog('<b>Verify ' + com + ' </b>')
        result = SendCmd(c, com)
        if "Error (" in result or checkPoint[1] not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify encldiag -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyEncldiagHelp(c):
    FailFlag = False
    tolog("<b>Verify encldiag -h </b>")
    result = SendCmd(c, 'encldiag -h')
    if "Error (" in result or 'encldiag' not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: encldiag -h </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify encldiag -h </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyEncldiagSpecifyInexistentId(c):
    FailFlag = False
    tolog("<b> Verify encldiag specify inexistent Id </b>")
    # -e <enclosure ID> (1,16)
    checkPoint = ['SEP not present', 'Invalid setting parameters']
    command = ['encldiag -a list -e 15 -t all', 'encldiag -e 15 -t powerontime',
               'encldiag -a list -e 17 -t all', 'encldiag -e 17 -t powerontime']
    for com in command[0:2]:
        tolog('<b>Verify ' + com + ' </b>')
        result = SendCmd(c, com)
        if "Error (" not in result or checkPoint[0] not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    for com in command[2:4]:
        tolog('<b>Verify ' + com + ' </b>')
        result = SendCmd(c, com)
        if "Error (" not in result or checkPoint[1] not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify encldiag specify inexistent Id </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyEncldiagInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify encldiag invalid option</b>")
    command = ['encldiag -x', 'encldiag -a list -x', 'encldiag -a -e 1 -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify encldiag invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyEncldiagInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify encldiag invalid parameters</b>")
    command = ['encldiag test', 'encldiag -a test', 'encldiag -a list -e test', 'encldiag -a list -e 1 -t test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify encldiag invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyEncldiagMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify encldiag missing parameters</b>")
    command = ['encldiag -a ', 'encldiag -a list -e', 'encldiag -a list -e 1 -t']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify encldiag missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


def bvt_verifyEncldiag(c):
    FailFlag = False
    tolog("Verify encldiag ")
    result = SendCmd(c, 'encldiag')
    checkPoint = ['EnclosureId             PSUId             Type              Wattage',
                  'EnclosureId                 Type                   PowerOnTime']

    if checkPoint[0] not in result or checkPoint[1] not in result:
        FailFlag = True
        tolog('Fail: encldiag  ')
    command = ['encldiag -t all', 'encldiag -e 1 -t all',
               'encldiag -t psu', 'encldiag -e 1 -t psu',
               'encldiag -t powerontime', 'encldiag -e 1 -t powerontime']

    for com in command[0:2]:
        tolog('Verify ' + com + ' ')
        result = SendCmd(c, com)
        if "Error (" in result or checkPoint[0] not in result or checkPoint[1] not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    for com in command[2:4]:
        tolog('Verify ' + com + ' ')
        result = SendCmd(c, com)
        if "Error (" in result or checkPoint[0] not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    for com in command[4:6]:
        tolog('Verify ' + com + ' ')
        result = SendCmd(c, com)
        if "Error (" in result or checkPoint[1] not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    return FailFlag

def bvt_verifyEncldiagList(c):
    FailFlag = False
    tolog("Verify encldiag -a list")
    result = SendCmd(c, 'encldiag -a list')
    checkPoint = ['EnclosureId             PSUId             Type              Wattage',
                  'EnclosureId                 Type                   PowerOnTime']

    if checkPoint[0] not in result or checkPoint[1] not in result:
        FailFlag = True
        tolog('Fail: encldiag -a list ')
    command = ['encldiag -a list -t all', 'encldiag -a list -e 1 -t all',
               'encldiag -a list -t psu', 'encldiag -a list -e 1 -t psu',
               'encldiag -a list -t powerontime', 'encldiag -a list -e 1 -t powerontime']

    for com in command[0:2]:
        tolog('Verify ' + com + ' ')
        result = SendCmd(c, com)
        if "Error (" in result or checkPoint[0] not in result or checkPoint[1] not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    for com in command[2:4]:
        tolog('Verify ' + com + ' ')
        result = SendCmd(c, com)
        if "Error (" in result or checkPoint[0] not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    for com in command[4:6]:
        tolog('Verify ' + com + ' ')
        result = SendCmd(c, com)
        if "Error (" in result or checkPoint[1] not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    return FailFlag

def bvt_verifyEncldiagHelp(c):
    FailFlag = False
    tolog("Verify encldiag -h ")
    result = SendCmd(c, 'encldiag -h')
    if "Error (" in result or 'encldiag' not in result:
        FailFlag = True
        tolog('Fail: encldiag -h ')

    return FailFlag

def bvt_verifyEncldiagSpecifyInexistentId(c):
    FailFlag = False
    tolog(" Verify encldiag specify inexistent Id ")
    # -e <enclosure ID> (1,16)
    checkPoint = ['SEP not present', 'Invalid setting parameters']
    command = ['encldiag -a list -e 15 -t all', 'encldiag -e 15 -t powerontime',
               'encldiag -a list -e 17 -t all', 'encldiag -e 17 -t powerontime']

    for com in command[0:2]:
        tolog('Verify ' + com + ' ')
        result = SendCmd(c, com)
        if "Error (" not in result or checkPoint[0] not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    for com in command[2:4]:
        tolog('Verify ' + com + ' ')
        result = SendCmd(c, com)
        if "Error (" not in result or checkPoint[1] not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    return FailFlag

def bvt_verifyEncldiagInvalidOption(c):
    FailFlag = False
    tolog("Verify encldiag invalid option")
    command = ['encldiag -x', 'encldiag -a list -x', 'encldiag -a -e 1 -x']

    for com in command:
        tolog(' Verify ' + com + '')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    return FailFlag

def bvt_verifyEncldiagInvalidParameters(c):
    FailFlag = False
    tolog("Verify encldiag invalid parameters")
    command = ['encldiag test', 'encldiag -a test', 'encldiag -a list -e test', 'encldiag -a list -e 1 -t test']

    for com in command:
        tolog(' Verify ' + com + '')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    return FailFlag

def bvt_verifyEncldiagMissingParameters(c):
    FailFlag = False
    tolog("Verify encldiag missing parameters")
    command = ['encldiag -a ', 'encldiag -a list -e', 'encldiag -a list -e 1 -t']

    for com in command:
        tolog(' Verify ' + com + '')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    return FailFlag



if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    bvt_verifyEncldiag(c)
    bvt_verifyEncldiagList(c)
    bvt_verifyEncldiagHelp(c)
    bvt_verifyEncldiagSpecifyInexistentId(c)
    bvt_verifyEncldiagInvalidOption(c)
    bvt_verifyEncldiagInvalidParameters(c)
    bvt_verifyEncldiagMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped