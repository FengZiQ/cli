# coding=utf-8

from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn

Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyIscsi(c):
    FailFlag = False
    tolog("<b> Verify iscsi </b>")

    # Test default iscsi list
    result = SendCmd(c, 'iscsi')

    if 'Error (' in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: iscsi </font>')

    tolog("<b> Verify iscsi -v </b>")
    result = SendCmd(c, 'iscsi -v')

    if 'AssnPortalIds: ' not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: iscsi -v </font>')

    # Test iscsi list by type
    command = [
        'iscsi -t target',
        'iscsi -t port',
        'iscsi -t portal -c 32',
        'iscsi -t session',
        'iscsi -t device'
    ]

    for com in command:
        tolog('<b>' + com + '</b>')

        result = SendCmd(c, com)

        if 'Error (' in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + '</font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify iscsi </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyIscsiList(c):
    FailFlag = False
    tolog("Verify iscsi -a list")

    result = SendCmd(c, 'iscsi -a list')

    if 'Error (' in result:
        FailFlag = True
        tolog('\nFail: iscsi -a list')

    tolog("Verify iscsi -a list -v ")
    result = SendCmd(c, 'iscsi -a list -v')

    if 'AssnPortalIds: ' not in result:
        FailFlag = True
        tolog('\nFail: iscsi -a list -v ')

    command = [
        'iscsi -a list -t target',
        'iscsi -a list -t port',
        'iscsi -a list -t portal -c 1',
        'iscsi -a list -t session',
        'iscsi -a list -t device'
    ]

    for com in command:
        tolog('' + com)

        result = SendCmd(c, com)

        if 'Error (' in result:
            FailFlag = True
            tolog('\nFail: ' + com)

    if FailFlag:
        tolog('\n<font color="red">Fail: iscsi -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyIscsiAdd(c):
    FailFlag = False
    checkTrunk = False
    tolog("Create trunk")

    # SendCmd(c, 'iscsi -a mod -t port -r 1 -p 1 -s "port=enable"')
    # SendCmd(c, 'iscsi -a mod -t port -r 1 -p 2 -s "port=enable"')
    SendCmd(c, 'iscsi -a mod -t port -r 2 -p 1 -s "port=enable"')
    SendCmd(c, 'iscsi -a mod -t port -r 2 -p 2 -s "port=enable"')

    # to create trunk uses for to create trunk type iscsi portal

    result = SendCmd(c, 'trunk')

    if 'Error (' not in result and 'No iSCSI trunks are available' in result:
        PortalID = []
        # del portal and add trunk
        result = SendCmd(c, 'iscsi -t portal')

        if 'No portal in the subsystem' not in result and 'Error (' not in result:
            row = result.split('\r\n')

            for x in range(4, (len(row) - 2)):
                element = row[x].split()
                PortalID.append(element[0])

        for i in PortalID:
            if 'Error (' in SendCmd(c, 'iscsi -a del -t portal -i ' + i):
                tolog(' To delete portal is failed ')

        if 'Error (' in SendCmd(c, 'trunk -a add -s "ctrlid=2,masterport=1,slaveport=2"'):
            tolog(' To add the type trunk portal is failed')

        if 'No iSCSI trunks are available' not in SendCmd(c, 'trunk'):
            checkTrunk = True

    if checkTrunk:
        tolog(' To verify add the type trunk portal  ')
        trunkID = []

        trunkinfo = SendCmd(c, 'trunk')

        if 'No portal in the subsystem' not in trunkinfo:
            for r in range(4, (len(trunkinfo.split('\r\n')) - 2)):
                element = trunkinfo.split('\r\n')[r].split()

                if element[0] != 'N/A':
                    trunkID.append(element[0])

        result = SendCmd(c, 'iscsi -a add -t portal -m trunk -s "trunkid=0, dhcp=enable,iptype=4"')

        checkResult = SendCmd(c, 'iscsi -t portal')

        tkportalID = []

        if 'No portal in the subsystem' not in checkResult:
            for r in range(4, (len(checkResult.split('\r\n')) - 2)):
                element = checkResult.split('\r\n')[r].split()

                if element[4] != 'N/A':
                    tkportalID.append(element[0])

        if 'Error (' in result or len(tkportalID) == 0:
            FailFlag = True
            tolog('Fail: iscsi -a add -t portal -m trunk -s "trunkid=0, dhcp=enable,iptype=4"')

    tolog(' del trunk ')
    PortalID = []

    result = SendCmd(c, 'iscsi -t portal')

    if 'No portal in the subsystem' not in result and 'Error (' not in result:
        row = result.split('\r\n')

        for x in range(4, (len(row) - 2)):
            element = row[x].split()
            PortalID.append(element[0])

    for i in PortalID:
        SendCmd(c, 'iscsi -a del -t portal -i ' + i)

    SendCmd(c, 'trunk -a del -i 0')
    SendCmd(c, 'trunk -a del -i 1')

    com = lambda type, setting: 'iscsi -a add -t portal -r 2 -p 1 -m ' + type + setting

    tolog(' To add the type VLAN portal ')
    result = SendCmd(c, com('vlan', ' -s "vlantag=1,iptype=4,dhcp=enable"'))

    checkResult = SendCmd(c, 'iscsi -t portal')

    vlanportalID = []

    if 'No portal in the subsystem' not in checkResult:
        for r in range(4, (len(checkResult.split('\r\n')) - 2)):
            element = checkResult.split('\r\n')[r].split()

            if element[3] != 'N/A':
                vlanportalID.append(element[0])

    if 'Error (' in result or len(vlanportalID) == 0:
        FailFlag = True
        tolog('Fail: ' + com('vlan', ' -s "iptype=4,dhcp=enable"') + ' ')

    tolog(' To add the type phy portal ')

    result = SendCmd(c, com('phy', ' -s "iptype=4,dhcp=enable"'))

    checkResult = SendCmd(c, 'iscsi -t portal')

    vlanportalID = []

    if 'No portal in the subsystem' not in checkResult:
        for r in range(4, (len(checkResult.split('\r\n')) - 2)):
            element = checkResult.split('\r\n')[r].split()

            if element[3] == 'N/A' and element[4] == 'N/A':
                vlanportalID.append(element[0])

    if 'Error (' in result or len(vlanportalID) == 0:
        FailFlag = True
        tolog('Fail: ' + com('phy', ' -s "iptype=4,dhcp=enable"') + ' ')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify iscsi -add </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
        
    return FailFlag

def verifyIscsiMod(c):
    FailFlag = False
    tolog("Verify to modify target alias")

    result = SendCmd(c, 'iscsi -a mod -t target -i 0 -s "alias=testmod"')

    checkResult = SendCmd(c, 'iscsi -v')

    if 'Error (' in result or 'testmod' not in checkResult:
        FailFlag = True
        tolog('Fail: iscsi -a mod -t target -i 0 -s "alias=testmod"')

    tolog(' Verify to modify option that can be enable or disable')

    optionEnable = [
        '"port=enable,jumboframe=enable"',
        '"headerdigest=enable"',
        '"datadigest=enable"',
        '"unichapauth=enable"',
        '"bichapauth=enable"',
        '"keepalive=enable"',
        '"dhcp=enable"'
    ]

    optionDisable = [
        '"port=disable,jumboframe=disable"',
        '"headerdigest=disable"',
        '"datadigest=disable"',
        '"unichapauth=disable"',
        '"bichapauth=disable"',
        '"keepalive=disable"',
        '"dhcp=disable"'
    ]

    for i in [1, 2]:
        result = SendCmd(c, 'iscsi -a mod -t port -r 2 -p ' + str(i) + ' -s ' + optionEnable[0])
        checkResult = SendCmd(c, 'iscsi -t port -r 2 -p ' + str(i))

        if 'Error (' in result or checkResult.count('JumboFrame: Enabled') != 1 or checkResult.count(
                'PortStatus: Enabled') != 1:
            FailFlag = True
            tolog('Fail: iscsi -a mod -t port -r 2 -p ' + str(i) + ' -s ' + optionEnable[0])

    for i in [1, 2]:
        result = SendCmd(c, 'iscsi -a mod -t port -r 2 -p ' + str(i) + ' -s ' + optionDisable[0])
        checkResult = SendCmd(c, 'iscsi -t port -r 2 -p ' + str(i))

        if 'Error (' in result or checkResult.count('JumboFrame: Disabled') != 1 or checkResult.count(
                'PortStatus: Disabled') != 1:
            FailFlag = True
            tolog('Fail: iscsi -a mod -t port -r 2 -p ' + str(i) + ' -s ' + optionDisable[0])

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify iscsi -mod </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyIscsiDel(c):
    FailFlag = False
    tolog("Verify iscsi -a del -t portal -i")

    PortalID = []

    result = SendCmd(c, 'iscsi -t portal')

    if 'No portal in the subsystem' not in result and 'Error (' not in result:
        row = result.split('\r\n')

        for x in range(4, (len(row) - 2)):
            element = row[x].split()
            PortalID.append(element[0])

    else:
        FailFlag = True
        tolog('Fail: There is no type portal ')

    for i in PortalID:
        result = SendCmd(c, 'iscsi -a del -t portal -i ' + i)

        if 'Error (' in result:
            FailFlag = True
            tolog('Fail: iscsi -a del -t portal -i ' + i)

    checkResult = SendCmd(c, 'iscsi -t portal')

    if 'No portal in the subsystem' not in checkResult:
        FailFlag = True
        tolog('Fail: iscsi -a del -t portal -i ')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify iscsi -a del </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyIscsiSpecifyInexistentId(c):
    FailFlag = False
    tolog("<b> Verify iscsi specify inexistent Id </b>")

    command = [
        'iscsi -t portal -i 65536',
        'iscsi -t port -r 3 -p 2',
        'iscsi -t port -r 2 -p 3',
    ]

    for com in command:
        result = SendCmd(c, com)

        if 'Error (' not in result:
            FailFlag = True
            tolog('<font color="red">Fail: ' + com + '</font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify iscsi specify inexistent Id </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyIscsiInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify iscsi invalid option</b>")

    command = [
        'iscsi -x',
        'iscsi -a list -x',
        'iscsi -a add -x',
        'iscsi -a mod -x',
        'iscsi -a del -x'
    ]

    for com in command:
        tolog('<b> Verify ' + com + '</b>')

        result = SendCmd(c, com)

        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify iscsi invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyIscsiInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify iscsi invalid parameters</b>")

    command = [
        'iscsi test',
        'iscsi -a list test',
        'iscsi -a add test',
        'iscsi -a mod test',
        'iscsi -a del test'
    ]

    for com in command:
        tolog('<b> Verify ' + com + '</b>')

        result = SendCmd(c, com)

        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify iscsi invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyIscsiMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify iscsi missing parameters</b>")

    command = [
        'iscsi -i',
        'iscsi -a list -i',
        'iscsi -a add -t',
        'iscsi -a mod -t',
        'iscsi -a del -t'
    ]

    for com in command:
        tolog('<b> Verify ' + com + '</b>')

        result = SendCmd(c, com)

        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify iscsi missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyIscsi(c)
    verifyIscsiList(c)
    verifyIscsiAdd(c)
    verifyIscsiMod(c)
    verifyIscsiDel(c)
    verifyIscsiSpecifyInexistentId(c)
    verifyIscsiInvalidOption(c)
    verifyIscsiInvalidParameters(c)
    verifyIscsiMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped