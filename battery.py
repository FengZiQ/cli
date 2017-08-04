# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"
def findBId(c):
    result = SendCmd(c, 'battery')
    num = 4
    BId = []
    row = result.split('\r\n')
    for i in range(4, len(row)-2):
        BId.append(row[i].split()[0])
    return BId

def verifyBattery(c):
    FailFlag = False
    tolog("<b>Verify battery </b>")
    result = SendCmd(c, 'battery ')
    if 'Error (' in result or '' not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: battery </font>')
    tolog("<b>Verify battery -b</b>")
    BId = findBId(c)
    if len(BId) == 2:
        for b in BId:
            result = SendCmd(c, 'battery -b ' + b)
            if 'BId' not in result or 'Status' not in result or 'EstimatedBackupCycle' not in result or 'TotalPowerOnHours' not in result:
                FailFlag = True
                tolog('\n<font color="red">Fail: battery -b ' + b + '</font>')
    if len(BId) == 1:
        result = SendCmd(c, 'battery -b ' + BId[0])
        if 'BId' not in result or 'Status' not in result or 'EstimatedBackupCycle' not in result or 'TotalPowerOnHours' not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: battery -b ' + BId[0] + '</font>')

        tolog("<b>Verify battery -b invalid battery id</b>")
        b = str(int(BId[0]) - 1)
        result =SendCmd(c, 'battery -b ' + b)
        if 'invalid setting ' + b + ' (1,2)' in result:
            b = str(int(BId[0]) + 1)
            result = SendCmd(c, 'battery -b ' + b)
            if 'Invalid battery id' not in result or 'Error (' not in result:
                FailFlag = True
                tolog('\n<font color="red">Fail: battery -b ' + b + '</font>')
        elif 'Invalid battery id' not in result or 'Error (' not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: battery -b ' + b + '</font>')


    if FailFlag:
        tolog('\n<font color="red">Fail: Verify battery </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBatteryList(c):
    FailFlag = False
    tolog("<b>Verify battery -a list</b>")
    result = SendCmd(c, 'battery -a list')
    if 'Error (' in result or '' not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: battery -a list</font>')
    tolog("<b>Verify battery -a list -b</b>")
    BId = findBId(c)
    if len(BId) == 2:
        for b in BId:
            result = SendCmd(c, 'battery -a list -b ' + b)
            if 'BId' not in result or 'Status' not in result or 'EstimatedBackupCycle' not in result or 'TotalPowerOnHours' not in result:
                FailFlag = True
                tolog('\n<font color="red">Fail: battery -a list -b ' + b + '</font>')
    if len(BId) == 1:
        result = SendCmd(c, 'battery -a list -b ' + BId[0])
        if 'BId' not in result or 'Status' not in result or 'EstimatedBackupCycle' not in result or 'TotalPowerOnHours' not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: battery -a list -b ' + BId[0] + '</font>')

        tolog("<b>Verify battery -a list -b invalid battery id</b>")
        b = str(int(BId[0]) - 1)
        result =SendCmd(c, 'battery -a list -b ' + b)
        if 'invalid setting ' + b + ' (1,2)' in result:
            b = str(int(BId[0]) + 1)
            result = SendCmd(c, 'battery -a list -b ' + b)
            if 'Invalid battery id' not in result or 'Error (' not in result:
                FailFlag = True
                tolog('\n<font color="red">Fail: battery -a list -b ' + b + '</font>')
        elif 'Invalid battery id' not in result or 'Error (' not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: battery -a list -b ' + b + '</font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify battery -a list</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBatteryRecondition(c):
    FailFlag = False
    tolog("<b>Verify battery -a recondition</b>")
    BId = findBId(c)
    for b in BId:
        result = SendCmd(c, 'battery -a recondition -b ' + b)
        checkResult = SendCmd(c, 'battery -b ' + b)
        if "Error (" in result or 'Recondition' not in checkResult:
            FailFlag = True
            tolog('\n<font color="red">Fail: battery -a recondition -b ' + b + '</font>')

    if len(BId) == 1:
        tolog("<b>Verify battery -a recondition -b invalid battery id</b>")
        b = str(int(BId[0]) - 1)
        result =SendCmd(c, 'battery -a recondition -b ' + b)
        if 'invalid setting ' + b + ' (1,2)' in result:
            b = str(int(BId[0]) + 1)
            result = SendCmd(c, 'battery -a recondition -b ' + b)
            if 'Invalid battery id' not in result or 'Error (' not in result:
                FailFlag = True
                tolog('\n<font color="red">Fail: battery -a recondition -b ' + b + '</font>')
        elif 'Invalid battery id' not in result or 'Error (' not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: battery -a recondition -b ' + b + '</font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify battery -a recondition</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBatteryHelp(c):
    FailFlag = False
    tolog("<b>Verify battery -h </b>")
    result = SendCmd(c, 'battery -h')
    if 'Error (' in result or 'battery' not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: battery -h </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify battery -h </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBatterySpecifyInexistentId(c):
    FailFlag = False
    tolog("<b> Verify battery specify inexistent Id </b>")
    command = ['battery -b 3', 'battery -a list -b 3', 'battery -a recondition -b 3']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "invalid setting 3 (1,2)" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify battery specify inexistent Id </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBatteryInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify battery invalid option</b>")
    command = ['battery -x', 'battery -a list -x', 'battery -a recondition -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify battery invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBatteryInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify battery invalid parameters</b>")
    command = ['battery test', 'battery -a test', 'battery -a recondition -b test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify battery invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBatteryMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify battery missing parameters</b>")
    command = ['battery -b', 'battery -a recondition -b', 'battery -a list -b']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify battery missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


def bvt_verifyBattery(c):
    FailFlag = False
    tolog("Verify battery ")
    result = SendCmd(c, 'battery ')
    if 'Error (' in result or '' not in result:
        FailFlag = True
        tolog('Fail: battery ')

    tolog("Verify battery -b")
    BId = findBId(c)
    if len(BId) == 2:
        for b in BId:
            result = SendCmd(c, 'battery -b ' + b)
            if 'BId' not in result or 'Status' not in result or 'EstimatedBackupCycle' not in result or 'TotalPowerOnHours' not in result:
                FailFlag = True
                tolog('Fail: battery -b ' + b + '')
    if len(BId) == 1:
        result = SendCmd(c, 'battery -b ' + BId[0])
        if 'BId' not in result or 'Status' not in result or 'EstimatedBackupCycle' not in result or 'TotalPowerOnHours' not in result:
            FailFlag = True
            tolog('Fail: battery -b ' + BId[0] + '')

        tolog("Verify battery -b invalid battery id")
        b = str(int(BId[0]) - 1)
        result =SendCmd(c, 'battery -b ' + b)
        if 'invalid setting ' + b + ' (1,2)' in result:
            b = str(int(BId[0]) + 1)
            result = SendCmd(c, 'battery -b ' + b)
            if 'Invalid battery id' not in result or 'Error (' not in result:
                FailFlag = True
                tolog('Fail: battery -b ' + b + '')
        elif 'Invalid battery id' not in result or 'Error (' not in result:
            FailFlag = True
            tolog('Fail: battery -b ' + b + '')

    return FailFlag

def bvt_verifyBatteryList(c):
    FailFlag = False
    tolog("Verify battery -a list")
    result = SendCmd(c, 'battery -a list')
    if 'Error (' in result or '' not in result:
        FailFlag = True
        tolog('Fail: battery -a list')

    tolog("Verify battery -a list -b")
    BId = findBId(c)
    if len(BId) == 2:
        for b in BId:
            result = SendCmd(c, 'battery -a list -b ' + b)
            if 'BId' not in result or 'Status' not in result or 'EstimatedBackupCycle' not in result or 'TotalPowerOnHours' not in result:
                FailFlag = True
                tolog('Fail: battery -a list -b ' + b + '')
    if len(BId) == 1:
        result = SendCmd(c, 'battery -a list -b ' + BId[0])
        if 'BId' not in result or 'Status' not in result or 'EstimatedBackupCycle' not in result or 'TotalPowerOnHours' not in result:
            FailFlag = True
            tolog('Fail: battery -a list -b ' + BId[0] + '')

        tolog("Verify battery -a list -b invalid battery id")
        b = str(int(BId[0]) - 1)
        result =SendCmd(c, 'battery -a list -b ' + b)
        if 'invalid setting ' + b + ' (1,2)' in result:
            b = str(int(BId[0]) + 1)
            result = SendCmd(c, 'battery -a list -b ' + b)
            if 'Invalid battery id' not in result or 'Error (' not in result:
                FailFlag = True
                tolog('Fail: battery -a list -b ' + b + '')
        elif 'Invalid battery id' not in result or 'Error (' not in result:
            FailFlag = True
            tolog('Fail: battery -a list -b ' + b + '')

    return FailFlag

def bvt_verifyBatteryRecondition(c):
    FailFlag = False
    tolog("Verify battery -a recondition")
    BId = findBId(c)
    for b in BId:
        result = SendCmd(c, 'battery -a recondition -b ' + b)
        checkResult = SendCmd(c, 'battery -b ' + b)
        if "Error (" in result or 'Recondition' not in checkResult:
            FailFlag = True
            tolog('Fail: battery -a recondition -b ' + b + '')

    if len(BId) == 1:
        tolog("Verify battery -a recondition -b invalid battery id")
        b = str(int(BId[0]) - 1)
        result =SendCmd(c, 'battery -a recondition -b ' + b)
        if 'invalid setting ' + b + ' (1,2)' in result:
            b = str(int(BId[0]) + 1)
            result = SendCmd(c, 'battery -a recondition -b ' + b)
            if 'Invalid battery id' not in result or 'Error (' not in result:
                FailFlag = True
                tolog('Fail: battery -a recondition -b ' + b + '')
        elif 'Invalid battery id' not in result or 'Error (' not in result:
            FailFlag = True
            tolog('Fail: battery -a recondition -b ' + b + '')

    return FailFlag

def bvt_verifyBatteryHelp(c):
    FailFlag = False
    tolog("Verify battery -h ")
    result = SendCmd(c, 'battery -h')
    if 'Error (' in result or 'battery' not in result:
        FailFlag = True
        tolog('Fail: battery -h ')

    return FailFlag

def bvt_verifyBatterySpecifyInexistentId(c):
    FailFlag = False
    tolog(" Verify battery specify inexistent Id ")
    command = ['battery -b 3', 'battery -a list -b 3', 'battery -a recondition -b 3']
    for com in command:
        tolog(' Verify ' + com + '')
        result = SendCmd(c, com)
        if "Error (" not in result or "invalid setting 3 (1,2)" not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    return FailFlag

def bvt_verifyBatteryInvalidOption(c):
    FailFlag = False
    tolog("Verify battery invalid option")
    command = ['battery -x', 'battery -a list -x', 'battery -a recondition -x']
    for com in command:
        tolog(' Verify ' + com + '')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    return FailFlag

def bvt_verifyBatteryInvalidParameters(c):
    FailFlag = False
    tolog("Verify battery invalid parameters")
    command = ['battery test', 'battery -a test', 'battery -a recondition -b test']
    for com in command:
        tolog(' Verify ' + com + '')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    return FailFlag

def bvt_verifyBatteryMissingParameters(c):
    FailFlag = False
    tolog("Verify battery missing parameters")
    command = ['battery -b', 'battery -a recondition -b', 'battery -a list -b']
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
    bvt_verifyBattery(c)
    bvt_verifyBatteryList(c)
    bvt_verifyBatteryRecondition(c)
    bvt_verifyBatteryHelp(c)
    bvt_verifyBatterySpecifyInexistentId(c)
    bvt_verifyBatteryInvalidOption(c)
    bvt_verifyBatteryInvalidParameters(c)
    bvt_verifyBatteryMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped

