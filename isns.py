# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyIsns(c):
    FailFlag = False
    tolog("<b>Verify isns </b>")
    result = SendCmd(c, 'isns')
    if 'Error (' in result or 'Mgmt' not in result or result.count(' Portal ') != 2:
        FailFlag = True
        tolog('\n<font color="red">Fail: isns </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify isns </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyIsnsList(c):
    FailFlag = False
    tolog("<b>Verify isns -a list </b>")
    result = SendCmd(c, 'isns -a list')
    if 'Error (' in result or 'Mgmt' not in result or result.count(' Portal ') != 2:
        FailFlag = True
        tolog('\n<font color="red">Fail: isns -a list </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify isns -a list</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyIsnsMod(c):
    FailFlag = False
    p = SendCmd(c, 'iscsi -a add -t portal -r 2 -p 2 -m phy  -s "iptype=4,dhcp=enable"')
    if "Error (" in p:
        tolog('<font color="red"> To add iscsi portal is failed </font>')
    else:
        pInfor = SendCmd(c, 'iscsi -t portal')
        pID = pInfor.split('\r\n')[-3][0]

        tolog('<b> Verify: isns -a mod -t portal -g ' + pID[0] + ' -s "isns=enable,serverip=1.1.1.1,serverport=65535" </b>')
        result = SendCmd(c, 'isns -a mod -t portal -g ' + pID[0] + ' -s "isns=enable,serverip=1.1.1.1,serverport=65535"')
        checkResult = SendCmd(c, 'isns')
        if 'Error (' in result or 'Enabled' not in checkResult or '1.1.1.1' not in checkResult:
            FailFlag = True
            tolog('<font color="red">Fail: isns -a mod -t portal -g ' + pID[0] + ' -s "isns=enable,serverip=1.1.1.1" </font>')

        tolog('<b> Verify: isns -a mod -t mgmt -s "isns=enable,serverip=1.1.1.1,serverport=1" </b>')
        result = SendCmd(c, 'isns -a mod -t mgmt -s "isns=enable,serverip=255.255.255.255,serverport=1"')
        checkResult = SendCmd(c, 'isns')
        if 'Error (' in result or 'Enabled' not in checkResult or '255.255.255.255' not in checkResult:
            FailFlag = True
            tolog('<font color="red"> Fail: isns -a mod -t mgmt -s "isns=enable,serverip=1.1.1.1,serverport=1" </font>')

        tolog('<b> cleaning environment </b>')
        SendCmd(c, 'isns -a mod -t portal -s "isns=disable" -g ' + pID[0])
        SendCmd(c, 'iscsi -a del -t portal -i ' + pID[0])

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify isns -a mod </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyIsnsSpecifyInexistentId(c):
    FailFlag = False
    pInfor = SendCmd(c, 'iscsi -t portal')
    if 'No portal in the subsystem' in pInfor:
        result = SendCmd(c, 'isns -a mod -t portal -g 1 -s "isns=enable,serverip=1.1.1.1,serverport=65535"')
        if 'Error (' not in result or 'Invalid iSCSI portal id' not in result:
            tolog(' <font color="red">Fail: isns specify inexistent Id </font>')
    else:
        pID = pInfor.split('\r\n')[-3][0]
        if int(pID[0]) < 31:
            tolog('<b> isns -a mod -t portal -g ' + str(int(pID[0]) + 1) + ' -s "isns=enable,serverip=1.1.1.1,serverport=65535" </b>')
            result = SendCmd(c, 'isns -a mod -t portal -g ' + str(int(pID[0]) + 1) + ' -s "isns=enable,serverip=1.1.1.1,serverport=65535"')
            if 'Error (' not in result or 'Invalid iSCSI portal id' not in result:
                tolog(' <font color="red">Fail: isns specify inexistent Id </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify isns specify inexistent Id </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyIsnsInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify isns invalid option</b>")
    command = ['isns -x', 'isns -a list -x', 'isns -a mod -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify isns invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyIsnsInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify isns invalid parameters</b>")
    command = ['isns test', 'isns -a list test', 'isns -a mod test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify isns invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyIsnsMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify isns missing parameters</b>")
    command = ['isns -g', 'iscsi -a mod -t', 'iscsi -a mod -s']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify isns missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)



def bvt_verifyIsns(c):
    FailFlag = False
    tolog("Verify isns ")
    result = SendCmd(c, 'isns')
    if 'Error (' in result or 'Mgmt' not in result or result.count(' Portal ') != 2:
        FailFlag = True
        tolog('Fail: isns ')

    return FailFlag

def bvt_verifyIsnsList(c):
    FailFlag = False
    tolog("Verify isns -a list ")
    result = SendCmd(c, 'isns -a list')
    if 'Error (' in result or 'Mgmt' not in result or result.count(' Portal ') != 2:
        FailFlag = True
        tolog('Fail: isns -a list ')

    return FailFlag

def bvt_verifyIsnsMod(c):
    FailFlag = False
    p = SendCmd(c, 'iscsi -a add -t portal -r 2 -p 2 -m phy  -s "iptype=4,dhcp=enable"')
    if 'Error (' in p:
        tolog('To add iscsi portal is failed')
    else:
        pInfor = SendCmd(c, 'iscsi -t portal')
        pID = pInfor.split('\r\n')[-3][0]

        tolog(' Verify: isns -a mod -t portal -g ' + pID[0] + ' -s "isns=enable,serverip=1.1.1.1,serverport=65535" ')
        result = SendCmd(c, 'isns -a mod -t portal -g ' + pID[0] + ' -s "isns=enable,serverip=1.1.1.1,serverport=65535"')
        checkResult = SendCmd(c, 'isns')
        if 'Error (' in result or 'Enabled' not in checkResult or '1.1.1.1' not in checkResult:
            FailFlag = True
            tolog(
                'Fail: isns -a mod -t portal -g ' + pID[0] + ' -s "isns=enable,serverip=1.1.1.1" ')

        tolog(' Verify: isns -a mod -t mgmt -s "isns=enable,serverip=1.1.1.1,serverport=1" ')
        result = SendCmd(c, 'isns -a mod -t mgmt -s "isns=enable,serverip=255.255.255.255,serverport=1"')
        checkResult = SendCmd(c, 'isns')
        if 'Error (' in result or 'Enabled' not in checkResult or '255.255.255.255' not in checkResult:
            FailFlag = True
            tolog(' Fail: isns -a mod -t mgmt -s "isns=enable,serverip=1.1.1.1,serverport=1" ')

        tolog(' cleaning environment ')
        SendCmd(c, 'isns -a mod -t portal -s "isns=disable" -g ' + pID[0])
        SendCmd(c, 'iscsi -a del -t portal -i ' + pID[0])

    return FailFlag

def bvt_verifyIsnsSpecifyInexistentId(c):
    FailFlag = False
    pInfor = SendCmd(c, 'iscsi -t portal')
    if 'No portal in the subsystem' in pInfor:
        result = SendCmd(c, 'isns -a mod -t portal -g 1 -s "isns=enable,serverip=1.1.1.1,serverport=65535"')
        if 'Error (' not in result or 'Invalid iSCSI portal id' not in result:
            tolog(' Fail: isns specify inexistent Id ')
    else:
        pID = pInfor.split('\r\n')[-3][0]
        if int(pID[0]) < 31:
            tolog(' isns -a mod -t portal -g ' + str(int(pID[0]) + 1) + ' -s "isns=enable,serverip=1.1.1.1,serverport=65535" ')
            result = SendCmd(c, 'isns -a mod -t portal -g ' + str(int(pID[0]) + 1) + ' -s "isns=enable,serverip=1.1.1.1,serverport=65535"')
            if 'Error (' not in result or 'Invalid iSCSI portal id' not in result:
                tolog(' Fail: isns specify inexistent Id ')

    return FailFlag

def bvt_verifyIsnsInvalidOption(c):
    FailFlag = False
    tolog("Verify isns invalid option")
    command = ['isns -x', 'isns -a list -x', 'isns -a mod -x']
    for com in command:
        tolog(' Verify ' + com + '')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('Fail: ' + com )

    return FailFlag

def bvt_verifyIsnsInvalidParameters(c):
    FailFlag = False
    tolog("Verify isns invalid parameters")
    command = ['isns test', 'isns -a list test', 'isns -a mod test']
    for com in command:
        tolog(' Verify ' + com + '')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('Fail: ' + com )

    return FailFlag

def bvt_verifyIsnsMissingParameters(c):
    FailFlag = False
    tolog("Verify isns missing parameters")
    command = ['isns -g', 'iscsi -a mod -t', 'iscsi -a mod -s']
    for com in command:
        tolog(' Verify ' + com + '')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('Fail: ' + com )

    return FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    bvt_verifyIsns(c)
    bvt_verifyIsnsList(c)
    bvt_verifyIsnsMod(c)
    bvt_verifyIsnsSpecifyInexistentId(c)
    bvt_verifyIsnsInvalidOption(c)
    bvt_verifyIsnsInvalidParameters(c)
    bvt_verifyIsnsMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped