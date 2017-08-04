# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyFc(c):
    FailFlag = False
    command = ['fc -t node',
               'fc -t port',
               'fc -t SFP',
               'fc -t stats',
               'fc -t device',
               'fc -t fabricdevices',
               'fc',
               'fc -t port -p 3'
               ]
    for com in command:
        tolog('<b>Verify: ' + com + '</b>')
        result = SendCmd(c, com)
        if 'Error (' in result:
            FailFlag = True
            tolog('<font color="red">Fail: ' + com + '</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify fc </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyFcList(c):
    FailFlag = False
    command = ['fc -a list -t node',
               'fc -a list -t port',
               'fc -a list -t SFP',
               'fc -a list -t stats',
               'fc -a list -t device',
               'fc -a list -t fabricdevices',
               'fc -a list',
               'fc -a list -t port -p 3'
               ]
    for com in command:
        tolog('<b>Verify: ' + com + '</b>')
        result = SendCmd(c, com)
        if 'Error (' in result:
            FailFlag = True
            tolog('<font color="red">Fail: ' + com + '</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify fc -a list</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyFcListV(c):
    FailFlag = False
    command = ['fc -a list -t node -v',
               'fc -a list -t port -v',
               'fc -a list -t SFP -v',
               'fc -a list -t stats -v',
               'fc -a list -t device -v',
               'fc -a list -t fabricdevices -v',
               'fc -a list -v',
               'fc -a list -t port -p 3 -v'
               ]
    for com in command:
        tolog('<b>Verify: ' + com + '</b>')
        result = SendCmd(c, com)
        if 'Error (' in result:
            FailFlag = True
            tolog('<font color="red">Fail: ' + com + '</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify fc -a list -v</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyFcMod(c):
    FailFlag = False
    ctrlID = ['2']
    portID = ['1', '2', '3', '4']
    setting = ['"linkspeed=4gb,topology=nlport,hardalpa=0"',
               '"linkspeed=16gb,topology=nport,hardalpa=126"',
               '"linkspeed=auto,topology=auto,hardalpa=255"']
    checkpoint = [': 4 Gb/s', ': NL-Port', ': 0',
                  ': 16 Gb/s', ': N-Port', ': 126',
                  ': Auto', ': Auto', ': 255'
                  ]
    for p in portID:
        index = 0
        for s in setting:
            tolog('<b> Verify fc -a mod -i ' + ctrlID[0] + ' -t port -p ' + p + ' -s ' + s + '</b>')
            result = SendCmd(c, 'fc -a mod -i ' + ctrlID[0] + ' -t port -p ' + p + ' -s ' + s)
            if 'Controller is not accessible' not in result:
                checkResult = SendCmd(c, 'fc -t port -i ' + ctrlID[0] + ' -t port -p ' + p + ' -v')
                if 'Error (' in result:
                    FailFlag = True
                    tolog('<font color="red">Fail: fc -a mod -i ' + ctrlID[0] + ' -t port -p ' + p + ' -s ' + s + '</font>')
                for i in range(index, (index + 3)):
                    if checkpoint[i] not in checkResult:
                        FailFlag = True
                        tolog('<font color="red">Fail: fc -a mod -i ' + ctrlID[0] + ' -t port -p ' + p + ' -s ' + s + '</font>')
            index = index + 3
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify fc -a mod </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyFcReset(c):
    FailFlag = False
    ctrlID = ['2']
    portID = ['1', '2', '3', '4']
    for p in portID:
        tolog('<b>Verify: fc -a reset -i ' + ctrlID[0] + ' -p ' + p + '</b>')
        result = SendCmd(c, 'fc -a reset -i ' + ctrlID[0] + ' -p ' + p)
        checkResult = SendCmd(c, 'fc -v -t port -i ' + ctrlID[0] + ' -p ' +p)
        if "Error (" in result or checkResult.count(': Auto') != 2 or checkResult.count(': 255') !=1:
            FailFlag = True
            tolog('<font color="red">Fail: fc -a reset -i ' + ctrlID[0] + ' -p ' + p + '</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify fc -a reset </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyFcClear(c):
    FailFlag = False
    ctrlID = ['2']
    portID = ['1', '2', '3', '4']
    for p in portID:
        tolog('<b>Verify: fc -a clear -i ' + ctrlID[0] + ' -p ' + p + '</b>')
        result = SendCmd(c, 'fc -a clear -i ' + ctrlID[0] + ' -p ' + p)
        checkResult = SendCmd(c, 'fc -v -t stats -i ' + ctrlID[0] + ' -p ' + p)
        if "Error (" in result or checkResult.count(': 0') != 6:
            FailFlag = True
            tolog('<font color="red">Fail: fc -a clear -i ' + ctrlID[0] + ' -p ' + p + '</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify fc -a clear </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyFcInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify fc invalid option</b>")
    command = ['fc -x', 'fc -a list -x', 'fc -a mod -x', 'fc -a reset -x', 'fc -a clear -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify fc invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyFcInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify fc invalid parameters</b>")
    command = ['fc test',
               'fc -a list test',
               'fc -a mod test',
               'fc -a reset test',
               'fc -a clear test',
               'fc -i 3 -t port',
               'fc -i 2 -t port -p 5'
               ]
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify fc invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyFcMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify fc missing parameters</b>")
    command = ['fc -a list -p', 'fc -a mod -i', 'fc -a reset -i', 'fc -a clear -p']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify fc missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


def bvt_verifyFc(c):
    FailFlag = False
    command = ['fc -t node',
               'fc -t port',
               'fc -t SFP',
               'fc -t stats',
               'fc -t device',
               'fc -t fabricdevices',
               'fc',
               'fc -t port -p 3'
               ]
    for com in command:
        tolog('Verify: ' + com)
        result = SendCmd(c, com)
        if 'Error (' in result:
            FailFlag = True
            tolog('Fail: ' + com)

    return FailFlag

def bvt_verifyFcList(c):
    FailFlag = False
    command = ['fc -a list -t node',
               'fc -a list -t port',
               'fc -a list -t SFP',
               'fc -a list -t stats',
               'fc -a list -t device',
               'fc -a list -t fabricdevices',
               'fc -a list',
               'fc -a list -t port -p 3'
               ]
    for com in command:
        tolog('Verify: ' + com)
        result = SendCmd(c, com)
        if 'Error (' in result:
            FailFlag = True
            tolog('Fail: ' + com)

    return FailFlag

def bvt_verifyFcListV(c):
    FailFlag = False
    command = ['fc -a list -t node -v',
               'fc -a list -t port -v',
               'fc -a list -t SFP -v',
               'fc -a list -t stats -v',
               'fc -a list -t device -v',
               'fc -a list -t fabricdevices -v',
               'fc -a list -v',
               'fc -a list -t port -p 3 -v'
               ]
    for com in command:
        tolog('Verify: ' + com)
        result = SendCmd(c, com)
        if 'Error (' in result:
            FailFlag = True
            tolog('Fail: ' + com )

    return FailFlag

def bvt_verifyFcMod(c):
    FailFlag = False
    ctrlID = ['2']
    portID = ['1', '2', '3', '4']
    setting = ['"linkspeed=4gb,topology=nlport,hardalpa=0"',
               '"linkspeed=16gb,topology=nport,hardalpa=126"',
               '"linkspeed=auto,topology=auto,hardalpa=255"']
    checkpoint = [': 4 Gb/s', ': NL-Port', ': 0',
                  ': 16 Gb/s', ': N-Port', ': 126',
                  ': Auto', ': Auto', ': 255'
                  ]
    for p in portID:
        index = 0
        for s in setting:
            tolog('Verify: fc -a mod -i ' + ctrlID[0] + ' -t port -p ' + p + ' -s ' + s)
            result = SendCmd(c, 'fc -a mod -i ' + ctrlID[0] + ' -t port -p ' + p + ' -s ' + s)
            if 'Controller is not accessible' not in result:
                checkResult = SendCmd(c, 'fc -t port -i ' + ctrlID[0] + ' -t port -p ' + p + ' -v')
                if 'Error (' in result:
                    FailFlag = True
                    tolog('Fail: fc -a mod -i ' + ctrlID[0] + ' -t port -p ' + p + ' -s ' + s)
                for i in range(index, (index + 3)):
                    if checkpoint[i] not in checkResult:
                        FailFlag = True
                        tolog('Fail: fc -a mod -i ' + ctrlID[0] + ' -t port -p ' + p + ' -s ' + s )
            index = index + 3

    return FailFlag

def bvt_verifyFcReset(c):
    FailFlag = False
    ctrlID = ['2']
    portID = ['1', '2', '3', '4']
    for p in portID:
        tolog('Verify: fc -a reset -i ' + ctrlID[0] + ' -p ' + p )
        result = SendCmd(c, 'fc -a reset -i ' + ctrlID[0] + ' -p ' + p)
        checkResult = SendCmd(c, 'fc -v -t port -i ' + ctrlID[0] + ' -p ' +p)
        if "Error (" in result or checkResult.count(': Auto') != 2 or checkResult.count(': 255') !=1:
            FailFlag = True
            tolog('Fail: fc -a reset -i ' + ctrlID[0] + ' -p ' + p )

    return FailFlag

def bvt_verifyFcClear(c):
    FailFlag = False
    ctrlID = ['2']
    portID = ['1', '2', '3', '4']
    for p in portID:
        tolog('Verify: fc -a clear -i ' + ctrlID[0] + ' -p ' + p )
        result = SendCmd(c, 'fc -a clear -i ' + ctrlID[0] + ' -p ' + p)
        checkResult = SendCmd(c, 'fc -v -t stats -i ' + ctrlID[0] + ' -p ' + p)
        if "Error (" in result or checkResult.count(': 0') != 6:
            FailFlag = True
            tolog(' Fail: fc -a clear -i ' + ctrlID[0] + ' -p ' + p )

    return FailFlag

def bvt_verifyFcInvalidOption(c):
    FailFlag = False
    tolog(" Verify fc invalid option ")
    command = ['fc -x', 'fc -a list -x', 'fc -a mod -x', 'fc -a reset -x', 'fc -a clear -x']
    for com in command:
        tolog(' Verify:' + com)
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('Fail: ' + com )

    return FailFlag

def bvt_verifyFcInvalidParameters(c):
    FailFlag = False
    tolog("Verify : fc invalid parameters")
    command = ['fc test',
               'fc -a list test',
               'fc -a mod test',
               'fc -a reset test',
               'fc -a clear test',
               'fc -i 3 -t port',
               'fc -i 2 -t port -p 5'
               ]
    for com in command:
        tolog('Verify ' + com )
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('Fail: ' + com )

    return FailFlag

def bvt_verifyFcMissingParameters(c):
    FailFlag = False
    tolog("Verify fc missing parameters")
    command = ['fc -a list -p', 'fc -a mod -i', 'fc -a reset -i', 'fc -a clear -p']
    for com in command:
        tolog('Verify ' + com )
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('Fail: ' + com )

    return FailFlag



if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    bvt_verifyFc(c)
    bvt_verifyFcList(c)
    bvt_verifyFcListV(c)
    bvt_verifyFcMod(c)
    bvt_verifyFcReset(c)
    bvt_verifyFcClear(c)
    bvt_verifyFcInvalidOption(c)
    bvt_verifyFcInvalidParameters(c)
    bvt_verifyFcMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped